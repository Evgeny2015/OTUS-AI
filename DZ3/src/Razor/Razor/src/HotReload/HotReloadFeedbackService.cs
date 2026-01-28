// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using Microsoft.Extensions.Logging;

namespace Microsoft.AspNetCore.Razor.HotReload;

/// <summary>
/// Provides visual feedback to developers about hot reload operations.
/// </summary>
public class HotReloadFeedbackService
{
    private readonly ILogger<HotReloadFeedbackService> _logger;
    private readonly IFeedbackProvider _feedbackProvider;

    /// <summary>
    /// Initializes a new instance of the <see cref="HotReloadFeedbackService"/> class.
    /// </summary>
    /// <param name="logger">The logger for diagnostic information.</param>
    /// <param name="feedbackProvider">The feedback provider for visual notifications.</param>
    public HotReloadFeedbackService(ILogger<HotReloadFeedbackService> logger, IFeedbackProvider feedbackProvider)
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _feedbackProvider = feedbackProvider ?? throw new ArgumentNullException(nameof(feedbackProvider));
    }

    /// <summary>
    /// Shows a reload notification to the developer.
    /// </summary>
    /// <param name="componentName">The name of the component being reloaded.</param>
    /// <param name="success">Whether the reload was successful.</param>
    /// <param name="duration">The duration of the reload operation.</param>
    public void ShowReloadNotification(string componentName, bool success, TimeSpan? duration = null)
    {
        if (string.IsNullOrEmpty(componentName))
        {
            throw new ArgumentException("Component name cannot be null or empty.", nameof(componentName));
        }

        var message = success
            ? $"Component '{componentName}' reloaded successfully"
            : $"Failed to reload component '{componentName}'";

        if (duration.HasValue)
        {
            message += $" in {duration.Value.TotalMilliseconds:F0}ms";
        }

        var level = success ? LogLevel.Information : LogLevel.Warning;
        _logger.Log(level, message);

        // Send to browser console if available
        try
        {
            _feedbackProvider.ShowNotification(message, success ? "success" : "error");
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Failed to show visual feedback for component reload");
        }
    }

    /// <summary>
    /// Shows a progress indicator for long-running reload operations.
    /// </summary>
    /// <param name="componentName">The name of the component being reloaded.</param>
    /// <param name="progress">The progress percentage (0-100).</param>
    public void ShowProgress(string componentName, int progress)
    {
        if (string.IsNullOrEmpty(componentName))
        {
            throw new ArgumentException("Component name cannot be null or empty.", nameof(componentName));
        }

        if (progress < 0 || progress > 100)
        {
            throw new ArgumentOutOfRangeException(nameof(progress), "Progress must be between 0 and 100");
        }

        var message = $"Reloading component '{componentName}': {progress}%";
        _logger.LogDebug(message);

        try
        {
            _feedbackProvider.ShowProgress(message, progress);
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Failed to show progress indicator for component reload");
        }
    }

    /// <summary>
    /// Shows an error overlay for compilation failures.
    /// </summary>
    /// <param name="componentName">The name of the component with compilation errors.</param>
    /// <param name="errorDetails">Detailed error information.</param>
    public void ShowErrorOverlay(string componentName, string errorDetails)
    {
        if (string.IsNullOrEmpty(componentName))
        {
            throw new ArgumentException("Component name cannot be null or empty.", nameof(componentName));
        }

        if (string.IsNullOrEmpty(errorDetails))
        {
            throw new ArgumentException("Error details cannot be null or empty.", nameof(errorDetails));
        }

        var message = $"Compilation error in component '{componentName}'";
        _logger.LogError(message + ": " + errorDetails);

        try
        {
            _feedbackProvider.ShowErrorOverlay(message, errorDetails);
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Failed to show error overlay for component compilation failure");
        }
    }

    /// <summary>
    /// Clears any active feedback indicators.
    /// </summary>
    public void ClearFeedback()
    {
        try
        {
            _feedbackProvider.Clear();
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Failed to clear feedback indicators");
        }
    }
}

/// <summary>
/// Provides visual feedback to developers during hot reload operations.
/// </summary>
public interface IFeedbackProvider
{
    /// <summary>
    /// Shows a notification message.
    /// </summary>
    /// <param name="message">The message to display.</param>
    /// <param name="type">The type of notification (success, error, warning, info).</param>
    void ShowNotification(string message, string type);

    /// <summary>
    /// Shows a progress indicator.
    /// </summary>
    /// <param name="message">The progress message.</param>
    /// <param name="percentage">The progress percentage (0-100).</param>
    void ShowProgress(string message, int percentage);

    /// <summary>
    /// Shows an error overlay with detailed information.
    /// </summary>
    /// <param name="title">The title of the error.</param>
    /// <param name="details">Detailed error information.</param>
    void ShowErrorOverlay(string title, string details);

    /// <summary>
    /// Clears all active feedback indicators.
    /// </summary>
    void Clear();
}

/// <summary>
/// A feedback provider that logs messages to the console.
/// </summary>
public class ConsoleFeedbackProvider : IFeedbackProvider
{
    public void ShowNotification(string message, string type)
    {
        Console.WriteLine($"[{type.ToUpper()}] {message}");
    }

    public void ShowProgress(string message, int percentage)
    {
        Console.WriteLine($"[PROGRESS] {message} ({percentage}%)");
    }

    public void ShowErrorOverlay(string title, string details)
    {
        Console.WriteLine($"[ERROR] {title}");
        Console.WriteLine($"Details: {details}");
    }

    public void Clear()
    {
        // Console feedback is transient, so clearing is a no-op
    }
}
