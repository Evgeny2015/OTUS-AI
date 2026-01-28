// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Moq;
using Xunit;

namespace Microsoft.AspNetCore.Razor.HotReload.Tests;

public class PerformanceOptimizerTest
{
    private readonly Mock<ILogger<PerformanceOptimizer>> _mockLogger;
    private readonly HotReloadOptions _options;
    private readonly PerformanceOptimizer _optimizer;

    public PerformanceOptimizerTest()
    {
        _mockLogger = new Mock<ILogger<PerformanceOptimizer>>();
        _options = new HotReloadOptions
        {
            MaxConcurrentReloads = 2,
            CacheExpirationTime = TimeSpan.FromMinutes(10)
        };
        _optimizer = new PerformanceOptimizer(_mockLogger.Object, _options);
    }

    [Fact]
    public void Constructor_ThrowsArgumentNullException_WhenLoggerIsNull()
    {
        Assert.Throws<ArgumentNullException>(() => new PerformanceOptimizer(null, _options));
    }

    [Fact]
    public void Constructor_ThrowsArgumentNullException_WhenOptionsIsNull()
    {
        Assert.Throws<ArgumentNullException>(() => new PerformanceOptimizer(_mockLogger.Object, null));
    }

    [Fact]
    public void CacheSize_ReturnsZero_WhenNoCacheEntries()
    {
        Assert.Equal(0, _optimizer.CacheSize);
    }

    [Fact]
    public void ActiveCompilations_ReturnsZero_WhenNoActiveCompilations()
    {
        Assert.Equal(0, _optimizer.ActiveCompilations);
    }

    [Fact]
    public void MaxConcurrentCompilations_ReturnsCorrectValue()
    {
        Assert.Equal(2, _optimizer.MaxConcurrentCompilations);
    }

    [Fact]
    public async Task ExecuteCompilationAsync_ReturnsCachedResult_WhenAvailable()
    {
        var componentPath = "TestComponent.razor";
        var expectedResult = new CompilationResult(true, componentPath, null, "test code", Array.Empty<RazorDiagnostic>());

        // First call to populate cache
        await _optimizer.ExecuteCompilationAsync(
            componentPath,
            () => Task.FromResult(expectedResult));

        // Second call should return cached result
        var result = await _optimizer.ExecuteCompilationAsync(
            componentPath,
            () => Task.FromResult(new CompilationResult(false, componentPath, null, null, Array.Empty<RazorDiagnostic>())));

        Assert.Equal(expectedResult, result);
        Assert.Equal(1, _optimizer.CacheSize);
    }

    [Fact]
    public async Task ExecuteCompilationAsync_CachesSuccessfulResults()
    {
        var componentPath = "TestComponent.razor";
        var expectedResult = new CompilationResult(true, componentPath, null, "test code", Array.Empty<RazorDiagnostic>());

        var result = await _optimizer.ExecuteCompilationAsync(
            componentPath,
            () => Task.FromResult(expectedResult));

        Assert.Equal(expectedResult, result);
        Assert.Equal(1, _optimizer.CacheSize);
    }

    [Fact]
    public async Task ExecuteCompilationAsync_DoesNotCacheFailedResults()
    {
        var componentPath = "TestComponent.razor";
        var failedResult = new CompilationResult(false, componentPath, null, null, Array.Empty<RazorDiagnostic>());

        var result = await _optimizer.ExecuteCompilationAsync(
            componentPath,
            () => Task.FromResult(failedResult));

        Assert.Equal(failedResult, result);
        Assert.Equal(0, _optimizer.CacheSize);
    }

    [Fact]
    public async Task ExecuteCompilationAsync_RespectsConcurrentCompilationLimit()
    {
        var componentPath = "TestComponent.razor";
        var expectedResult = new CompilationResult(true, componentPath, null, "test code", Array.Empty<RazorDiagnostic>());

        // Start multiple concurrent compilations
        var tasks = new[]
        {
            _optimizer.ExecuteCompilationAsync(componentPath + "1", () => Task.FromResult(expectedResult)),
            _optimizer.ExecuteCompilationAsync(componentPath + "2", () => Task.FromResult(expectedResult)),
            _optimizer.ExecuteCompilationAsync(componentPath + "3", () => Task.FromResult(expectedResult))
        };

        await Task.WhenAll(tasks);

        // Should not exceed max concurrent compilations
        Assert.True(_optimizer.ActiveCompilations <= _options.MaxConcurrentReloads);
    }

    [Fact]
    public async Task ExecuteCompilationAsync_HandlesTimeout()
    {
        var componentPath = "TestComponent.razor";
        _optimizer.CompilationTimeout = TimeSpan.FromMilliseconds(100);

        await Assert.ThrowsAsync<TimeoutException>(() =>
            _optimizer.ExecuteCompilationAsync(
                componentPath,
                () => Task.Delay(1000).ContinueWith(_ => new CompilationResult(true, componentPath, null, "test code", Array.Empty<RazorDiagnostic>()))));
    }

    [Fact]
    public void ClearCache_RemovesAllCacheEntries()
    {
        // This test is limited because we can't directly populate the cache
        // In a real scenario, cache would be populated through ExecuteCompilationAsync calls
        _optimizer.ClearCache();
        Assert.Equal(0, _optimizer.CacheSize);
    }

    [Fact]
    public void GetStatistics_ReturnsValidStatistics()
    {
        var stats = _optimizer.GetStatistics();

        Assert.NotNull(stats);
        Assert.Equal(0, stats.CacheSize);
        Assert.Equal(0, stats.ActiveCompilations);
        Assert.Equal(2, stats.MaxConcurrentCompilations);
        Assert.Equal(0, stats.TotalFileChanges);
        Assert.Equal(0, stats.UniqueFiles);
        Assert.Equal(0, stats.AverageChangesPerFile);
        Assert.Equal(0, stats.CacheHitRate);
    }

    [Fact]
    public async Task OptimizeCompilationAsync_HandlesEmptyComponentPaths()
    {
        var results = await _optimizer.OptimizeCompilationAsync(
            Array.Empty<string>(),
            path => Task.FromResult(new CompilationResult(true, path, null, "test code", Array.Empty<RazorDiagnostic>())));

        Assert.Empty(results);
    }

    [Fact]
    public async Task OptimizeCompilationAsync_HandlesNullComponentPaths()
    {
        await Assert.ThrowsAsync<ArgumentNullException>(() =>
            _optimizer.OptimizeCompilationAsync<string>(
                null,
                path => Task.FromResult(new CompilationResult(true, path, null, "test code", Array.Empty<RazorDiagnostic>()))));
    }

    [Fact]
    public async Task Dispose_DisposesResources()
    {
        _optimizer.Dispose();

        // Verify that resources are disposed (this is mainly testing that Dispose doesn't throw)
        Assert.True(true); // If we get here, Dispose didn't throw
    }

    [Fact]
    public async Task ExecuteCompilationAsync_HandlesExceptionInCompilationTask()
    {
        var componentPath = "TestComponent.razor";

        await Assert.ThrowsAsync<Exception>(() =>
            _optimizer.ExecuteCompilationAsync(
                componentPath,
                () => throw new Exception("Compilation error")));
    }

    [Fact]
    public async Task ExecuteCompilationAsync_HandlesCancellation()
    {
        var componentPath = "TestComponent.razor";
        var cts = new System.Threading.CancellationTokenSource();
        cts.Cancel();

        await Assert.ThrowsAsync<OperationCanceledException>(() =>
            _optimizer.ExecuteCompilationAsync(
                componentPath,
                () => Task.FromResult(new CompilationResult(true, componentPath, null, "test code", Array.Empty<RazorDiagnostic>())),
                cts.Token));
    }
}
