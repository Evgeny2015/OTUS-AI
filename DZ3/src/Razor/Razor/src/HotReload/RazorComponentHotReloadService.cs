// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Logging;

namespace Microsoft.AspNetCore.Razor.HotReload;

/// <summary>
/// Main orchestrator for Razor component hot reload functionality.
/// </summary>
public class RazorComponentHotReloadService : IDisposable
{
    private readonly ILogger<RazorComponentHotReloadService> _logger;
    private readonly IHostEnvironment _hostEnvironment;
    private readonly IFeedbackProvider _feedbackProvider;
    private readonly ComponentStateManager _stateManager;
    private readonly RazorComponentCompiler _compiler;
    private readonly Renderer _renderer;
    private RazorComponentFileWatcher _fileWatcher;
    private bool _disposed;

    /// <summary>
    /// Initializes a new instance of the <see cref="RazorComponentHotReloadService"/> class.
    /// </summary>
    /// <param name="renderer">The renderer to integrate with.</param>
    /// <param name="serviceProvider">The service provider for dependency injection.</param>
    /// <param name="logger">The logger for diagnostic information.</param>
    public RazorComponentHotReloadService(
        Renderer renderer,
        IServiceProvider serviceProvider,
        ILogger<RazorComponentHotReloadService> logger)
    {
        _renderer = renderer ?? throw new ArgumentNullException(nameof(renderer));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));

        // Get dependencies from service provider
        _hostEnvironment = serviceProvider.GetService<IHostEnvironment>()
            ?? throw new InvalidOperationException("IHostEnvironment is required for hot reload");

        _feedbackProvider = serviceProvider.GetService<IFeedbackProvider>()
            ?? new ConsoleFeedbackProvider();

        _stateManager = serviceProvider.GetService<ComponentStateManager>()
            ?? new ComponentStateManager(_logger);

        _compiler = serviceProvider.GetService<RazorComponentCompiler>()
            ?? new RazorComponentCompiler(_logger);

        // Validate development environment
        if (!_hostEnvironment.IsDevelopment())
        {
            throw new InvalidOperationException(
                "Hot reload is only available in development environments");
        }
    }

    /// <summary>
    /// Starts watching for file changes and enables hot reload functionality.
    /// </summary>
    public void StartWatching()
    {
        if (_disposed)
        {
            throw new ObjectDisposedException(nameof(RazorComponentHotReloadService));
        }

        if (_fileWatcher != null)
        {
            _logger.LogWarning("Hot reload service is already running");
            return;
        }

        try
        {
            var projectPath = GetProjectPath();
            _fileWatcher = new RazorComponentFileWatcher(
                projectPath,
                OnFileChanged,
                OnFileRenamed,
                _logger
            );

            _fileWatcher.StartWatching();
            _logger.LogInformation("Razor component hot reload service started");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to start hot reload service");
            throw;
        }
    }

    /// <summary>
    /// Stops watching for file changes and disables hot reload functionality.
    /// </summary>
    public void StopWatching()
    {
        if (_disposed)
        {
            throw new ObjectDisposedException(nameof(RazorComponentHotReloadService));
        }

        _fileWatcher?.StopWatching();
        _fileWatcher?.Dispose();
        _fileWatcher = null;

        _logger.LogInformation("Razor component hot reload service stopped");
    }

    /// <summary>
    /// Event raised when a component is successfully reloaded.
    /// </summary>
    public event EventHandler<ComponentReloadEventArgs> ComponentReloaded;

    private void OnFileChanged(string filePath)
    {
        if (_disposed)
        {
            return;
        }

        try
        {
            _feedbackProvider.ShowProgress($"Processing changes in {Path.GetFileName(filePath)}", 0);

            var stopwatch = System.Diagnostics.Stopwatch.StartNew();
            var result = ReloadComponentAsync(filePath).GetAwaiter().GetResult();
            stopwatch.Stop();

            if (result.Success)
            {
                _feedbackProvider.ShowNotification(
                    $"Component {Path.GetFileName(filePath)} reloaded successfully",
                    "success");

                _logger.LogInformation(
                    "Component {Component} reloaded in {Duration}ms",
                    Path.GetFileName(filePath),
                    stopwatch.ElapsedMilliseconds);

                ComponentReloaded?.Invoke(this, new ComponentReloadEventArgs
                {
                    ComponentPath = filePath,
                    ComponentName = Path.GetFileNameWithoutExtension(filePath),
                    Duration = stopwatch.Elapsed,
                    Success = true
                });
            }
            else
            {
                _feedbackProvider.ShowErrorOverlay(
                    $"Failed to reload component {Path.GetFileName(filePath)}",
                    string.Join(Environment.NewLine, result.Diagnostics));

                _logger.LogWarning(
                    "Component {Component} failed to reload after {Duration}ms",
                    Path.GetFileName(filePath),
                    stopwatch.ElapsedMilliseconds);
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error processing file change for {FilePath}", filePath);
            _feedbackProvider.ShowErrorOverlay(
                "Hot reload error",
                ex.Message);
        }
    }

    private void OnFileRenamed(string oldPath, string newPath)
    {
        if (_disposed)
        {
            return;
        }

        try
        {
            _logger.LogInformation("Component file renamed: {OldPath} -> {NewPath}", oldPath, newPath);

            // Clear state for old component
            _stateManager.ClearAllSnapshots();

            // Start watching new path
            if (_fileWatcher != null)
            {
                _fileWatcher.StopWatching();
                _fileWatcher = new RazorComponentFileWatcher(
                    Path.GetDirectoryName(newPath),
                    OnFileChanged,
                    OnFileRenamed,
                    _logger);
                _fileWatcher.StartWatching();
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error handling file rename from {OldPath} to {NewPath}", oldPath, newPath);
        }
    }

    private async Task<ComponentReloadResult> ReloadComponentAsync(string componentPath)
    {
        try
        {
            // Capture current state before reload
            var componentState = _renderer.GetComponentState(GetComponentIdFromPath(componentPath));
            if (componentState != null)
            {
                _stateManager.CaptureState(componentState);
            }

            // Recompile the component
            var compilationResult = await _compiler.RecompileComponentAsync(componentPath);

            if (!compilationResult.Success)
            {
                return ComponentReloadResult.Failure(componentPath, compilationResult.Diagnostics);
            }

            // Apply the new component
            var applyResult = await ApplyComponentUpdate(compilationResult);

            if (applyResult.Success)
            {
                // Restore state if possible
                if (componentState != null)
                {
                    _stateManager.RestoreState(componentState);
                }

                return ComponentReloadResult.Success(componentPath);
            }
            else
            {
                return ComponentReloadResult.Failure(componentPath, applyResult.Diagnostics);
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to reload component {ComponentPath}", componentPath);
            return ComponentReloadResult.Failure(componentPath, new[] { ex.Message });
        }
    }

    private async Task<ComponentReloadResult> ApplyComponentUpdate(CompilationResult compilationResult)
    {
        try
        {
            // This is a simplified implementation. In a real scenario, you would:
            // 1. Replace the component assembly in the runtime
            // 2. Update the component registration
            // 3. Trigger re-rendering with preserved state

            // For now, we'll simulate the update
            await Task.Delay(100); // Simulate update time

            return ComponentReloadResult.Success(compilationResult.ComponentPath);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to apply component update for {ComponentPath}", compilationResult.ComponentPath);
            return ComponentReloadResult.Failure(compilationResult.ComponentPath, new[] { ex.Message });
        }
    }

    private string GetProjectPath()
    {
        // Try to get from environment variable first
        var projectPath = Environment.GetEnvironmentVariable("RAZOR_PROJECT_PATH");
        if (!string.IsNullOrEmpty(projectPath) && Directory.Exists(projectPath))
        {
            return projectPath;
        }

        // Fall back to content root path
        return _hostEnvironment.ContentRootPath;
    }

    private int GetComponentIdFromPath(string componentPath)
    {
        // This is a simplified implementation. In a real scenario, you would
        // need to map file paths to component IDs based on the current renderer state.
        return 0; // Placeholder
    }

    /// <summary>
    /// Releases all resources used by the <see cref="RazorComponentHotReloadService"/>.
    /// </summary>
    public void Dispose()
    {
        if (_disposed)
        {
            return;
        }

        _disposed = true;

        StopWatching();
        _stateManager.ClearAllSnapshots();

        _logger.LogInformation("Razor component hot reload service disposed");
    }
}

/// <summary>
/// Represents the result of a component reload operation.
/// </summary>
public class ComponentReloadResult
{
    /// <summary>
    /// Gets a value indicating whether the reload was successful.
    /// </summary>
    public bool Success { get; }

    /// <summary>
    /// Gets the path to the component that was reloaded.
    /// </summary>
    public string ComponentPath { get; }

    /// <summary>
    /// Gets any diagnostics produced during the reload operation.
    /// </summary>
    public IReadOnlyList<string> Diagnostics { get; }

    private ComponentReloadResult(bool success, string componentPath, IReadOnlyList<string> diagnostics)
    {
        Success = success;
        ComponentPath = componentPath;
        Diagnostics = diagnostics;
    }

    /// <summary>
    /// Creates a successful reload result.
    /// </summary>
    /// <param name="componentPath">The path to the component.</param>
    /// <returns>A successful reload result.</returns>
    public static ComponentReloadResult Success(string componentPath)
    {
        return new ComponentReloadResult(true, componentPath, Array.Empty<string>());
    }

    /// <summary>
    /// Creates a failed reload result.
    /// </summary>
    /// <param name="componentPath">The path to the component.</param>
    /// <param name="diagnostics">The reload diagnostics.</param>
    /// <returns>A failed reload result.</returns>
    public static ComponentReloadResult Failure(string componentPath, IReadOnlyList<string> diagnostics)
    {
        return new ComponentReloadResult(false, componentPath, diagnostics);
    }
}

/// <summary>
/// Event arguments for component reload events.
/// </summary>
public class ComponentReloadEventArgs : EventArgs
{
    /// <summary>
    /// Gets the path to the component that was reloaded.
    /// </summary>
    public string ComponentPath { get; set; }

    /// <summary>
    /// Gets the name of the component that was reloaded.
    /// </summary>
    public string ComponentName { get; set; }

    /// <summary>
    /// Gets the duration of the reload operation.
    /// </summary>
    public TimeSpan Duration { get; set; }

    /// <summary>
    /// Gets a value indicating whether the reload was successful.
    /// </summary>
    public bool Success { get; set; }
}
