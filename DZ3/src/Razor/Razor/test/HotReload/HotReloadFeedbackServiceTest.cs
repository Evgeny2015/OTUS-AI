// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using Microsoft.Extensions.Logging;
using Moq;
using Xunit;

namespace Microsoft.AspNetCore.Razor.HotReload.Tests;

public class HotReloadFeedbackServiceTest
{
    private readonly Mock<ILogger<HotReloadFeedbackService>> _mockLogger;
    private readonly Mock<IFeedbackProvider> _mockFeedbackProvider;
    private readonly HotReloadFeedbackService _feedbackService;

    public HotReloadFeedbackServiceTest()
    {
        _mockLogger = new Mock<ILogger<HotReloadFeedbackService>>();
        _mockFeedbackProvider = new Mock<IFeedbackProvider>();
        _feedbackService = new HotReloadFeedbackService(_mockLogger.Object, _mockFeedbackProvider.Object);
    }

    [Fact]
    public void Constructor_ThrowsArgumentNullException_WhenLoggerIsNull()
    {
        Assert.Throws<ArgumentNullException>(() => new HotReloadFeedbackService(null, _mockFeedbackProvider.Object));
    }

    [Fact]
    public void Constructor_ThrowsArgumentNullException_WhenFeedbackProviderIsNull()
    {
        Assert.Throws<ArgumentNullException>(() => new HotReloadFeedbackService(_mockLogger.Object, null));
    }

    [Fact]
    public void ShowReloadNotification_ThrowsArgumentException_WhenComponentNameIsNull()
    {
        Assert.Throws<ArgumentException>(() =>
            _feedbackService.ShowReloadNotification(null, true));
    }

    [Fact]
    public void ShowReloadNotification_ThrowsArgumentException_WhenComponentNameIsEmpty()
    {
        Assert.Throws<ArgumentException>(() =>
            _feedbackService.ShowReloadNotification(string.Empty, true));
    }

    [Fact]
    public void ShowReloadNotification_CallsLoggerAndFeedbackProvider_WhenSuccessful()
    {
        _feedbackService.ShowReloadNotification("TestComponent", true);

        _mockLogger.Verify(
            logger => logger.Log(
                LogLevel.Information,
                It.IsAny<EventId>(),
                It.Is<It.IsAnyType>((v, t) => v.ToString().Contains("TestComponent reloaded successfully")),
                null,
                It.IsAny<Func<It.IsAnyType, Exception, string>>()),
            Times.Once);

        _mockFeedbackProvider.Verify(
            provider => provider.ShowNotification(
                It.Is<string>(s => s.Contains("TestComponent")),
                "success"),
            Times.Once);
    }

    [Fact]
    public void ShowReloadNotification_CallsLoggerAndFeedbackProvider_WhenFailed()
    {
        _feedbackService.ShowReloadNotification("TestComponent", false);

        _mockLogger.Verify(
            logger => logger.Log(
                LogLevel.Warning,
                It.IsAny<EventId>(),
                It.Is<It.IsAnyType>((v, t) => v.ToString().Contains("Failed to reload component")),
                null,
                It.IsAny<Func<It.IsAnyType, Exception, string>>()),
            Times.Once);

        _mockFeedbackProvider.Verify(
            provider => provider.ShowNotification(
                It.Is<string>(s => s.Contains("TestComponent")),
                "error"),
            Times.Once);
    }

    [Fact]
    public void ShowReloadNotification_IncludesDuration_WhenProvided()
    {
        var duration = TimeSpan.FromMilliseconds(500);
        _feedbackService.ShowReloadNotification("TestComponent", true, duration);

        _mockLogger.Verify(
            logger => logger.Log(
                LogLevel.Information,
                It.IsAny<EventId>(),
                It.Is<It.IsAnyType>((v, t) => v.ToString().Contains("500")),
                null,
                It.IsAny<Func<It.IsAnyType, Exception, string>>()),
            Times.Once);
    }

    [Fact]
    public void ShowProgress_ThrowsArgumentException_WhenComponentNameIsNull()
    {
        Assert.Throws<ArgumentException>(() =>
            _feedbackService.ShowProgress(null, 50));
    }

    [Fact]
    public void ShowProgress_ThrowsArgumentException_WhenComponentNameIsEmpty()
    {
        Assert.Throws<ArgumentException>(() =>
            _feedbackService.ShowProgress(string.Empty, 50));
    }

    [Fact]
    public void ShowProgress_ThrowsArgumentOutOfRangeException_WhenProgressIsNegative()
    {
        Assert.Throws<ArgumentOutOfRangeException>(() =>
            _feedbackService.ShowProgress("TestComponent", -1));
    }

    [Fact]
    public void ShowProgress_ThrowsArgumentOutOfRangeException_WhenProgressIsGreaterThan100()
    {
        Assert.Throws<ArgumentOutOfRangeException>(() =>
            _feedbackService.ShowProgress("TestComponent", 101));
    }

    [Fact]
    public void ShowProgress_CallsFeedbackProvider_WhenValid()
    {
        _feedbackService.ShowProgress("TestComponent", 75);

        _mockFeedbackProvider.Verify(
            provider => provider.ShowProgress(
                It.Is<string>(s => s.Contains("TestComponent") && s.Contains("75")),
                75),
            Times.Once);
    }

    [Fact]
    public void ShowErrorOverlay_ThrowsArgumentException_WhenComponentNameIsNull()
    {
        Assert.Throws<ArgumentException>(() =>
            _feedbackService.ShowErrorOverlay(null, "Error details"));
    }

    [Fact]
    public void ShowErrorOverlay_ThrowsArgumentException_WhenComponentNameIsEmpty()
    {
        Assert.Throws<ArgumentException>(() =>
            _feedbackService.ShowErrorOverlay(string.Empty, "Error details"));
    }

    [Fact]
    public void ShowErrorOverlay_ThrowsArgumentException_WhenErrorDetailsIsNull()
    {
        Assert.Throws<ArgumentException>(() =>
            _feedbackService.ShowErrorOverlay("TestComponent", null));
    }

    [Fact]
    public void ShowErrorOverlay_ThrowsArgumentException_WhenErrorDetailsIsEmpty()
    {
        Assert.Throws<ArgumentException>(() =>
            _feedbackService.ShowErrorOverlay("TestComponent", string.Empty));
    }

    [Fact]
    public void ShowErrorOverlay_CallsLoggerAndFeedbackProvider()
    {
        _feedbackService.ShowErrorOverlay("TestComponent", "Compilation error");

        _mockLogger.Verify(
            logger => logger.Log(
                LogLevel.Error,
                It.IsAny<EventId>(),
                It.Is<It.IsAnyType>((v, t) => v.ToString().Contains("Compilation error")),
                null,
                It.IsAny<Func<It.IsAnyType, Exception, string>>()),
            Times.Once);

        _mockFeedbackProvider.Verify(
            provider => provider.ShowErrorOverlay(
                It.Is<string>(s => s.Contains("TestComponent")),
                "Compilation error"),
            Times.Once);
    }

    [Fact]
    public void ClearFeedback_CallsFeedbackProvider()
    {
        _feedbackService.ClearFeedback();

        _mockFeedbackProvider.Verify(provider => provider.Clear(), Times.Once);
    }

    [Fact]
    public void ShowReloadNotification_HandlesFeedbackProviderException()
    {
        _mockFeedbackProvider
            .Setup(provider => provider.ShowNotification(It.IsAny<string>(), It.IsAny<string>()))
            .Throws(new Exception("Feedback provider error"));

        // Should not throw, but should log warning
        _feedbackService.ShowReloadNotification("TestComponent", true);

        _mockLogger.Verify(
            logger => logger.Log(
                LogLevel.Warning,
                It.IsAny<EventId>(),
                It.Is<It.IsAnyType>((v, t) => v.ToString().Contains("Failed to show visual feedback")),
                It.IsAny<Exception>(),
                It.IsAny<Func<It.IsAnyType, Exception, string>>()),
            Times.Once);
    }

    [Fact]
    public void ShowProgress_HandlesFeedbackProviderException()
    {
        _mockFeedbackProvider
            .Setup(provider => provider.ShowProgress(It.IsAny<string>(), It.IsAny<int>()))
            .Throws(new Exception("Feedback provider error"));

        // Should not throw, but should log warning
        _feedbackService.ShowProgress("TestComponent", 50);

        _mockLogger.Verify(
            logger => logger.Log(
                LogLevel.Warning,
                It.IsAny<EventId>(),
                It.Is<It.IsAnyType>((v, t) => v.ToString().Contains("Failed to show progress indicator")),
                It.IsAny<Exception>(),
                It.IsAny<Func<It.IsAnyType, Exception, string>>()),
            Times.Once);
    }

    [Fact]
    public void ShowErrorOverlay_HandlesFeedbackProviderException()
    {
        _mockFeedbackProvider
            .Setup(provider => provider.ShowErrorOverlay(It.IsAny<string>(), It.IsAny<string>()))
            .Throws(new Exception("Feedback provider error"));

        // Should not throw, but should log warning
        _feedbackService.ShowErrorOverlay("TestComponent", "Error details");

        _mockLogger.Verify(
            logger => logger.Log(
                LogLevel.Warning,
                It.IsAny<EventId>(),
                It.Is<It.IsAnyType>((v, t) => v.ToString().Contains("Failed to show error overlay")),
                It.IsAny<Exception>(),
                It.IsAny<Func<It.IsAnyType, Exception, string>>()),
            Times.Once);
    }

    [Fact]
    public void ClearFeedback_HandlesFeedbackProviderException()
    {
        _mockFeedbackProvider
            .Setup(provider => provider.Clear())
            .Throws(new Exception("Feedback provider error"));

        // Should not throw, but should log warning
        _feedbackService.ClearFeedback();

        _mockLogger.Verify(
            logger => logger.Log(
                LogLevel.Warning,
                It.IsAny<EventId>(),
                It.Is<It.IsAnyType>((v, t) => v.ToString().Contains("Failed to clear feedback indicators")),
                It.IsAny<Exception>(),
                It.IsAny<Func<It.IsAnyType, Exception, string>>()),
            Times.Once);
    }
}
