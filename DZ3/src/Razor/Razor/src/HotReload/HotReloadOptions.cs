// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;

namespace Microsoft.AspNetCore.Razor.HotReload;

/// <summary>
/// Configuration options for Razor component hot reload functionality.
/// </summary>
public class HotReloadOptions
{
    /// <summary>
    /// Gets or sets a value indicating whether hot reload is enabled.
    /// </summary>
    public bool Enabled { get; set; } = true;

    /// <summary>
    /// Gets or sets the debounce delay in milliseconds to handle rapid successive changes.
    /// </summary>
    public int DebounceDelay { get; set; } = 300; // milliseconds

    /// <summary>
    /// Gets or sets the maximum number of concurrent reload operations.
    /// </summary>
    public int MaxConcurrentReloads { get; set; } = 3;

    /// <summary>
    /// Gets or sets a value indicating whether to preserve component state during reload.
    /// </summary>
    public bool PreserveState { get; set; } = true;

    /// <summary>
    /// Gets or sets a value indicating whether to show visual feedback notifications.
    /// </summary>
    public bool ShowNotifications { get; set; } = true;

    /// <summary>
    /// Gets or sets the compilation timeout.
    /// </summary>
    public TimeSpan CompilationTimeout { get; set; } = TimeSpan.FromSeconds(10);

    /// <summary>
    /// Gets or sets the cache expiration time for compiled components.
    /// </summary>
    public TimeSpan CacheExpirationTime { get; set; } = TimeSpan.FromMinutes(10);

    /// <summary>
    /// Gets or sets the maximum cache size for compiled components.
    /// </summary>
    public int MaxCacheSize { get; set; } = 100;

    /// <summary>
    /// Gets or sets a value indicating whether to enable detailed logging.
    /// </summary>
    public bool EnableDetailedLogging { get; set; } = false;

    /// <summary>
    /// Gets or sets the project path to watch for changes. If null, uses the content root path.
    /// </summary>
    public string? ProjectPath { get; set; }

    /// <summary>
    /// Gets or sets a value indicating whether to enable performance monitoring.
    /// </summary>
    public bool EnablePerformanceMonitoring { get; set; } = true;

    /// <summary>
    /// Gets or sets the interval for performance statistics collection.
    /// </summary>
    public TimeSpan PerformanceMonitoringInterval { get; set; } = TimeSpan.FromMinutes(1);

    /// <summary>
    /// Gets or sets a value indicating whether to enable automatic fallback to full restart on failure.
    /// </summary>
    public bool EnableAutomaticFallback { get; set; } = true;

    /// <summary>
    /// Gets or sets the maximum number of consecutive failures before triggering fallback.
    /// </summary>
    public int MaxConsecutiveFailures { get; set; } = 3;

    /// <summary>
    /// Gets or sets a value indicating whether to validate component syntax before compilation.
    /// </summary>
    public bool EnableSyntaxValidation { get; set; } = true;

    /// <summary>
    /// Gets or sets a value indicating whether to enable incremental compilation.
    /// </summary>
    public bool EnableIncrementalCompilation { get; set; } = true;

    /// <summary>
    /// Gets or sets a value indicating whether to enable dependency analysis for parallel compilation.
    /// </summary>
    public bool EnableDependencyAnalysis { get; set; } = true;

    /// <summary>
    /// Gets or sets the maximum file size (in bytes) for components to be processed by hot reload.
    /// </summary>
    public long MaxComponentFileSize { get; set; } = 1024 * 1024; // 1 MB

    /// <summary>
    /// Gets or sets a value indicating whether to enable error recovery mechanisms.
    /// </summary>
    public bool EnableErrorRecovery { get; set; } = true;

    /// <summary>
    /// Gets or sets the retry count for failed compilation attempts.
    /// </summary>
    public int CompilationRetryCount { get; set; } = 2;

    /// <summary>
    /// Gets or sets the delay between retry attempts.
    /// </summary>
    public TimeSpan RetryDelay { get; set; } = TimeSpan.FromMilliseconds(500);

    /// <summary>
    /// Validates the configuration options.
    /// </summary>
    /// <exception cref="InvalidOperationException">Thrown when configuration is invalid.</exception>
    public void Validate()
    {
        if (DebounceDelay < 0)
        {
            throw new InvalidOperationException("DebounceDelay must be non-negative.");
        }

        if (MaxConcurrentReloads <= 0)
        {
            throw new InvalidOperationException("MaxConcurrentReloads must be greater than zero.");
        }

        if (CompilationTimeout <= TimeSpan.Zero)
        {
            throw new InvalidOperationException("CompilationTimeout must be greater than zero.");
        }

        if (CacheExpirationTime <= TimeSpan.Zero)
        {
            throw new InvalidOperationException("CacheExpirationTime must be greater than zero.");
        }

        if (MaxCacheSize <= 0)
        {
            throw new InvalidOperationException("MaxCacheSize must be greater than zero.");
        }

        if (PerformanceMonitoringInterval <= TimeSpan.Zero)
        {
            throw new InvalidOperationException("PerformanceMonitoringInterval must be greater than zero.");
        }

        if (MaxConsecutiveFailures <= 0)
        {
            throw new InvalidOperationException("MaxConsecutiveFailures must be greater than zero.");
        }

        if (MaxComponentFileSize <= 0)
        {
            throw new InvalidOperationException("MaxComponentFileSize must be greater than zero.");
        }

        if (CompilationRetryCount < 0)
        {
            throw new InvalidOperationException("CompilationRetryCount must be non-negative.");
        }

        if (RetryDelay < TimeSpan.Zero)
        {
            throw new InvalidOperationException("RetryDelay must be non-negative.");
        }
    }
}
