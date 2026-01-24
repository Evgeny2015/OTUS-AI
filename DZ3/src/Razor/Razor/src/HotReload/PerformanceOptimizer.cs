// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;

namespace Microsoft.AspNetCore.Razor.HotReload;

/// <summary>
/// Optimizes hot reload performance through caching, parallelization, and resource management.
/// </summary>
public class PerformanceOptimizer
{
    private readonly ILogger<PerformanceOptimizer> _logger;
    private readonly ConcurrentDictionary<string, CompilationCacheEntry> _compilationCache = new();
    private readonly ConcurrentDictionary<string, FileChangeEntry> _fileChangeHistory = new();
    private readonly SemaphoreSlim _compilationSemaphore;
    private readonly int _maxConcurrentCompilations;
    private readonly TimeSpan _cacheExpirationTime;
    private readonly Timer _cacheCleanupTimer;

    /// <summary>
    /// Initializes a new instance of the <see cref="PerformanceOptimizer"/> class.
    /// </summary>
    /// <param name="logger">The logger for diagnostic information.</param>
    /// <param name="options">The performance optimization options.</param>
    public PerformanceOptimizer(ILogger<PerformanceOptimizer> logger, HotReloadOptions options)
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));

        _maxConcurrentCompilations = options.MaxConcurrentReloads;
        _cacheExpirationTime = TimeSpan.FromMinutes(10); // 10 minute cache expiration
        _compilationSemaphore = new SemaphoreSlim(_maxConcurrentCompilations, _maxConcurrentCompilations);

        // Start cache cleanup timer (runs every 5 minutes)
        _cacheCleanupTimer = new Timer(CleanupExpiredCacheEntries, null, TimeSpan.FromMinutes(5), TimeSpan.FromMinutes(5));
    }

    /// <summary>
    /// Gets or sets the compilation timeout.
    /// </summary>
    public TimeSpan CompilationTimeout { get; set; } = TimeSpan.FromSeconds(10);

    /// <summary>
    /// Gets the current cache size.
    /// </summary>
    public int CacheSize => _compilationCache.Count;

    /// <summary>
    /// Gets the current number of active compilations.
    /// </summary>
    public int ActiveCompilations => _maxConcurrentCompilations - _compilationSemaphore.CurrentCount;

    /// <summary>
    /// Executes a compilation task with performance optimizations.
    /// </summary>
    /// <param name="componentPath">The path to the component to compile.</param>
    /// <param name="compilationTask">The compilation task to execute.</param>
    /// <param name="cancellationToken">The cancellation token.</param>
    /// <returns>The compilation result.</returns>
    public async Task<T> ExecuteCompilationAsync<T>(
        string componentPath,
        Func<Task<T>> compilationTask,
        CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrEmpty(componentPath))
        {
            throw new ArgumentException("Component path cannot be null or empty.", nameof(componentPath));
        }

        // Check cache first
        if (_compilationCache.TryGetValue(componentPath, out var cachedEntry))
        {
            if (!cachedEntry.IsExpired)
            {
                _logger.LogDebug("Returning cached compilation result for {ComponentPath}", componentPath);
                return cachedEntry.Result;
            }
            else
            {
                _compilationCache.TryRemove(componentPath, out _);
                _logger.LogDebug("Cache entry expired for {ComponentPath}", componentPath);
            }
        }

        // Track file change history
        var changeEntry = _fileChangeHistory.GetOrAdd(componentPath, _ => new FileChangeEntry());
        changeEntry.LastAccessTime = DateTime.UtcNow;
        changeEntry.AccessCount++;

        // Acquire semaphore for concurrent compilation limit
        await _compilationSemaphore.WaitAsync(cancellationToken);

        try
        {
            var stopwatch = Stopwatch.StartNew();

            using var timeoutCts = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
            timeoutCts.CancelAfter(CompilationTimeout);

            try
            {
                var result = await compilationTask().WaitAsync(timeoutCts.Token);

                stopwatch.Stop();

                // Cache successful results
                if (result is CompilationResult compilationResult && compilationResult.Success)
                {
                    _compilationCache[componentPath] = new CompilationCacheEntry
                    {
                        Result = result,
                        CreatedTime = DateTime.UtcNow,
                        ExpirationTime = DateTime.UtcNow + _cacheExpirationTime
                    };

                    _logger.LogDebug(
                        "Compilation completed and cached for {ComponentPath} in {Duration}ms",
                        componentPath,
                        stopwatch.ElapsedMilliseconds);
                }
                else
                {
                    _logger.LogDebug(
                        "Compilation completed for {ComponentPath} in {Duration}ms (not cached)",
                        componentPath,
                        stopwatch.ElapsedMilliseconds);
                }

                return result;
            }
            catch (OperationCanceledException) when (timeoutCts.IsCancellationRequested)
            {
                stopwatch.Stop();
                _logger.LogWarning(
                    "Compilation timeout after {Timeout}ms for {ComponentPath}",
                    CompilationTimeout.TotalMilliseconds,
                    componentPath);

                throw new TimeoutException($"Compilation timeout after {CompilationTimeout.TotalMilliseconds}ms");
            }
        }
        finally
        {
            _compilationSemaphore.Release();
        }
    }

    /// <summary>
    /// Clears the compilation cache.
    /// </summary>
    public void ClearCache()
    {
        var cacheSize = _compilationCache.Count;
        _compilationCache.Clear();
        _logger.LogInformation("Cleared {CacheSize} compilation cache entries", cacheSize);
    }

    /// <summary>
    /// Gets performance statistics.
    /// </summary>
    /// <returns>Performance statistics.</returns>
    public PerformanceStatistics GetStatistics()
    {
        var totalChanges = _fileChangeHistory.Values.Sum(entry => entry.AccessCount);
        var uniqueFiles = _fileChangeHistory.Count;
        var avgChangesPerFile = uniqueFiles > 0 ? totalChanges / (double)uniqueFiles : 0;

        return new PerformanceStatistics
        {
            CacheSize = _compilationCache.Count,
            ActiveCompilations = ActiveCompilations,
            MaxConcurrentCompilations = _maxConcurrentCompilations,
            TotalFileChanges = totalChanges,
            UniqueFiles = uniqueFiles,
            AverageChangesPerFile = avgChangesPerFile,
            CacheHitRate = CalculateCacheHitRate()
        };
    }

    /// <summary>
    /// Optimizes compilation by analyzing dependencies and compiling in parallel when possible.
    /// </summary>
    /// <param name="componentPaths">The paths of components to compile.</param>
    /// <param name="compilationTaskFactory">Factory function to create compilation tasks.</param>
    /// <param name="cancellationToken">The cancellation token.</param>
    /// <returns>The compilation results.</returns>
    public async Task<IReadOnlyList<T>> OptimizeCompilationAsync<T>(
        IEnumerable<string> componentPaths,
        Func<string, Task<T>> compilationTaskFactory,
        CancellationToken cancellationToken = default)
    {
        if (componentPaths == null)
        {
            throw new ArgumentNullException(nameof(componentPaths));
        }

        var paths = componentPaths.ToList();
        if (paths.Count == 0)
        {
            return Array.Empty<T>();
        }

        var results = new ConcurrentBag<T>();
        var tasks = new List<Task>();

        // Analyze dependencies and group independent components
        var dependencyGroups = AnalyzeDependencies(paths);

        foreach (var group in dependencyGroups)
        {
            var groupTasks = group.Select(async path =>
            {
                try
                {
                    var result = await ExecuteCompilationAsync(
                        path,
                        () => compilationTaskFactory(path),
                        cancellationToken);

                    results.Add(result);
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Failed to compile component {ComponentPath}", path);
                }
            });

            tasks.AddRange(groupTasks);
        }

        // Wait for all compilations to complete
        await Task.WhenAll(tasks);

        return results.ToArray();
    }

    private List<List<string>> AnalyzeDependencies(List<string> componentPaths)
    {
        // This is a simplified dependency analysis.
        // In a real implementation, you would parse component files to determine
        // actual dependencies and group components that can be compiled in parallel.

        // For now, we'll group components by directory to minimize potential conflicts
        var groups = componentPaths
            .GroupBy(path => Path.GetDirectoryName(path))
            .Select(group => group.ToList())
            .ToList();

        return groups;
    }

    private double CalculateCacheHitRate()
    {
        var totalAccesses = _fileChangeHistory.Values.Sum(entry => entry.AccessCount);
        var cachedFiles = _compilationCache.Count;

        if (totalAccesses == 0)
        {
            return 0.0;
        }

        // Estimate cache hit rate based on cached files vs total accesses
        // This is a rough approximation since we don't track individual cache hits
        return Math.Min(1.0, cachedFiles / (double)totalAccesses);
    }

    private void CleanupExpiredCacheEntries(object state)
    {
        try
        {
            var now = DateTime.UtcNow;
            var expiredKeys = _compilationCache
                .Where(kvp => kvp.Value.IsExpired)
                .Select(kvp => kvp.Key)
                .ToList();

            foreach (var key in expiredKeys)
            {
                _compilationCache.TryRemove(key, out _);
            }

            if (expiredKeys.Count > 0)
            {
                _logger.LogDebug("Cleaned up {ExpiredCount} expired cache entries", expiredKeys.Count);
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error during cache cleanup");
        }
    }

    /// <summary>
    /// Disposes resources used by the performance optimizer.
    /// </summary>
    public void Dispose()
    {
        _compilationSemaphore?.Dispose();
        _cacheCleanupTimer?.Dispose();
    }
}

/// <summary>
/// Represents a cached compilation result.
/// </summary>
internal class CompilationCacheEntry
{
    public object Result { get; set; }
    public DateTime CreatedTime { get; set; }
    public DateTime ExpirationTime { get; set; }

    public bool IsExpired => DateTime.UtcNow > ExpirationTime;
}

/// <summary>
/// Represents file change history for performance analysis.
/// </summary>
internal class FileChangeEntry
{
    public int AccessCount { get; set; }
    public DateTime LastAccessTime { get; set; }
}

/// <summary>
/// Contains performance statistics for hot reload operations.
/// </summary>
public class PerformanceStatistics
{
    /// <summary>
    /// Gets the current cache size.
    /// </summary>
    public int CacheSize { get; set; }

    /// <summary>
    /// Gets the number of active compilations.
    /// </summary>
    public int ActiveCompilations { get; set; }

    /// <summary>
    /// Gets the maximum number of concurrent compilations.
    /// </summary>
    public int MaxConcurrentCompilations { get; set; }

    /// <summary>
    /// Gets the total number of file changes.
    /// </summary>
    public int TotalFileChanges { get; set; }

    /// <summary>
    /// Gets the number of unique files that have been changed.
    /// </summary>
    public int UniqueFiles { get; set; }

    /// <summary>
    /// Gets the average number of changes per file.
    /// </summary>
    public double AverageChangesPerFile { get; set; }

    /// <summary>
    /// Gets the estimated cache hit rate.
    /// </summary>
    public double CacheHitRate { get; set; }
}
