// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.IO;
using Microsoft.Extensions.Logging;

namespace Microsoft.AspNetCore.Razor.HotReload;

/// <summary>
/// Monitors .razor files for changes and triggers hot reload when files are modified.
/// </summary>
public class RazorComponentFileWatcher : IDisposable
{
    private readonly FileSystemWatcher _watcher;
    private readonly ILogger<RazorComponentFileWatcher> _logger;
    private readonly Action<string> _onFileChanged;
    private readonly Action<string, string> _onFileRenamed;
    private readonly Timer _debounceTimer;
    private readonly object _lockObject = new object();
    private readonly HashSet<string> _pendingChanges = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
    private bool _disposed;

    /// <summary>
    /// Initializes a new instance of the <see cref="RazorComponentFileWatcher"/> class.
    /// </summary>
    /// <param name="projectPath">The path to the project directory to watch.</param>
    /// <param name="onFileChanged">Callback invoked when a .razor file is changed.</param>
    /// <param name="onFileRenamed">Callback invoked when a .razor file is renamed.</param>
    /// <param name="logger">The logger for diagnostic information.</param>
    /// <param name="debounceDelay">The debounce delay in milliseconds to handle rapid successive changes.</param>
    public RazorComponentFileWatcher(
        string projectPath,
        Action<string> onFileChanged,
        Action<string, string> onFileRenamed,
        ILogger<RazorComponentFileWatcher> logger,
        int debounceDelay = 300)
    {
        ArgumentNullException.ThrowIfNull(projectPath);
        ArgumentNullException.ThrowIfNull(onFileChanged);
        ArgumentNullException.ThrowIfNull(onFileRenamed);
        ArgumentNullException.ThrowIfNull(logger);

        _logger = logger;
        _onFileChanged = onFileChanged;
        _onFileRenamed = onFileRenamed;

        if (!Directory.Exists(projectPath))
        {
            throw new ArgumentException($"Project path does not exist: {projectPath}", nameof(projectPath));
        }

        _watcher = new FileSystemWatcher(projectPath, "*.razor")
        {
            EnableRaisingEvents = true,
            IncludeSubdirectories = true,
            NotifyFilter = NotifyFilters.LastWrite | NotifyFilters.FileName | NotifyFilters.DirectoryName
        };

        _watcher.Changed += OnFileChanged;
        _watcher.Created += OnFileChanged;
        _watcher.Renamed += OnFileRenamed;
        _watcher.Error += OnWatcherError;

        _debounceTimer = new Timer(OnDebounceTimerElapsed, null, Timeout.Infinite, Timeout.Infinite);
        _debounceDelay = debounceDelay;
    }

    private readonly int _debounceDelay;

    /// <summary>
    /// Starts watching for file changes.
    /// </summary>
    public void StartWatching()
    {
        if (_disposed)
        {
            throw new ObjectDisposedException(nameof(RazorComponentFileWatcher));
        }

        _watcher.EnableRaisingEvents = true;
        _logger.LogInformation("Started watching for .razor file changes in {ProjectPath}", _watcher.Path);
    }

    /// <summary>
    /// Stops watching for file changes.
    /// </summary>
    public void StopWatching()
    {
        if (_disposed)
        {
            throw new ObjectDisposedException(nameof(RazorComponentFileWatcher));
        }

        _watcher.EnableRaisingEvents = false;
        _logger.LogInformation("Stopped watching for .razor file changes");
    }

    private void OnFileChanged(object sender, FileSystemEventArgs e)
    {
        if (_disposed)
        {
            return;
        }

        try
        {
            lock (_lockObject)
            {
                _pendingChanges.Add(e.FullPath);
            }

            _debounceTimer.Change(_debounceDelay, Timeout.Infinite);
            _logger.LogDebug("File change detected: {FilePath}", e.FullPath);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error handling file change for {FilePath}", e.FullPath);
        }
    }

    private void OnFileRenamed(object sender, RenamedEventArgs e)
    {
        if (_disposed)
        {
            return;
        }

        try
        {
            _onFileRenamed?.Invoke(e.OldFullPath, e.FullPath);
            _logger.LogInformation("File renamed: {OldPath} -> {NewPath}", e.OldFullPath, e.FullPath);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error handling file rename from {OldPath} to {NewPath}", e.OldFullPath, e.FullPath);
        }
    }

    private void OnDebounceTimerElapsed(object state)
    {
        if (_disposed)
        {
            return;
        }

        try
        {
            lock (_lockObject)
            {
                foreach (var filePath in _pendingChanges)
                {
                    try
                    {
                        _onFileChanged?.Invoke(filePath);
                    }
                    catch (Exception ex)
                    {
                        _logger.LogError(ex, "Error processing file change for {FilePath}", filePath);
                    }
                }

                _pendingChanges.Clear();
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error in debounce timer callback");
        }
    }

    private void OnWatcherError(object sender, ErrorEventArgs e)
    {
        _logger.LogError(e.GetException(), "File system watcher error occurred");
    }

    /// <summary>
    /// Releases all resources used by the <see cref="RazorComponentFileWatcher"/>.
    /// </summary>
    public void Dispose()
    {
        if (_disposed)
        {
            return;
        }

        _disposed = true;

        _watcher?.Dispose();
        _debounceTimer?.Dispose();

        _logger.LogInformation("Razor component file watcher disposed");
    }
}
