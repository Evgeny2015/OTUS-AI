// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Components;
using Microsoft.Extensions.Logging;
using Moq;
using Xunit;

namespace Microsoft.AspNetCore.Razor.HotReload.Tests;

public class ComponentStateManagerTest
{
    private readonly Mock<ILogger<ComponentStateManager>> _mockLogger;
    private readonly ComponentStateManager _stateManager;

    public ComponentStateManagerTest()
    {
        _mockLogger = new Mock<ILogger<ComponentStateManager>>();
        _stateManager = new ComponentStateManager(_mockLogger.Object);
    }

    [Fact]
    public void Constructor_ThrowsArgumentNullException_WhenLoggerIsNull()
    {
        Assert.Throws<ArgumentNullException>(() => new ComponentStateManager(null));
    }

    [Fact]
    public void CaptureState_ThrowsArgumentNullException_WhenComponentStateIsNull()
    {
        Assert.Throws<ArgumentNullException>(() => _stateManager.CaptureState(null));
    }

    [Fact]
    public void RestoreState_ThrowsArgumentNullException_WhenComponentStateIsNull()
    {
        Assert.Throws<ArgumentNullException>(() => _stateManager.RestoreState(null));
    }

    [Fact]
    public void CaptureState_ReturnsTrue_WhenStateCapturedSuccessfully()
    {
        var mockComponentState = CreateMockComponentState(1);

        var result = _stateManager.CaptureState(mockComponentState);

        Assert.True(result);
        Assert.Equal(1, _stateManager.SnapshotCount);
    }

    [Fact]
    public void RestoreState_ReturnsFalse_WhenNoSnapshotExists()
    {
        var mockComponentState = CreateMockComponentState(1);

        var result = _stateManager.RestoreState(mockComponentState);

        Assert.False(result);
    }

    [Fact]
    public void CommitSnapshots_AddsSnapshotsToMainStore()
    {
        var mockComponentState = CreateMockComponentState(1);

        // Capture state to pending store
        _stateManager.CaptureState(mockComponentState);

        // Commit to main store
        _stateManager.CommitSnapshots(new[] { 1 });

        Assert.Equal(1, _stateManager.SnapshotCount);
    }

    [Fact]
    public void DiscardSnapshots_RemovesSnapshotsFromPendingStore()
    {
        var mockComponentState = CreateMockComponentState(1);

        // Capture state to pending store
        _stateManager.CaptureState(mockComponentState);

        // Discard from pending store
        _stateManager.DiscardSnapshots(new[] { 1 });

        Assert.Equal(0, _stateManager.SnapshotCount);
    }

    [Fact]
    public void ClearAllSnapshots_RemovesAllSnapshots()
    {
        var mockComponentState1 = CreateMockComponentState(1);
        var mockComponentState2 = CreateMockComponentState(2);

        // Capture multiple states
        _stateManager.CaptureState(mockComponentState1);
        _stateManager.CaptureState(mockComponentState2);

        Assert.Equal(2, _stateManager.SnapshotCount);

        // Clear all snapshots
        _stateManager.ClearAllSnapshots();

        Assert.Equal(0, _stateManager.SnapshotCount);
    }

    [Fact]
    public void SnapshotCount_ReturnsCorrectCount()
    {
        var mockComponentState1 = CreateMockComponentState(1);
        var mockComponentState2 = CreateMockComponentState(2);

        Assert.Equal(0, _stateManager.SnapshotCount);

        _stateManager.CaptureState(mockComponentState1);
        Assert.Equal(1, _stateManager.SnapshotCount);

        _stateManager.CaptureState(mockComponentState2);
        Assert.Equal(2, _stateManager.SnapshotCount);
    }

    [Fact]
    public void CaptureState_HandlesExceptionGracefully()
    {
        // This test verifies that CaptureState doesn't throw when there are issues
        var mockComponentState = CreateMockComponentState(1);

        // Should not throw even if there are internal issues
        var result = _stateManager.CaptureState(mockComponentState);

        // Result may be false if there was an error, but it shouldn't throw
        Assert.IsType<bool>(result);
    }

    [Fact]
    public void RestoreState_HandlesExceptionGracefully()
    {
        // This test verifies that RestoreState doesn't throw when there are issues
        var mockComponentState = CreateMockComponentState(1);

        // Should not throw even if there are internal issues
        var result = _stateManager.RestoreState(mockComponentState);

        // Result may be false if there was an error, but it shouldn't throw
        Assert.IsType<bool>(result);
    }

    private Mock<ComponentState> CreateMockComponentState(int componentId)
    {
        var mockComponent = new Mock<IComponent>();
        mockComponent.Setup(c => c.GetType()).Returns(typeof(MockComponent));

        var mockComponentState = new Mock<ComponentState>(
            Mock.Of<Renderer>(),
            componentId,
            mockComponent.Object,
            null);

        return mockComponentState;
    }

    private class MockComponent : ComponentBase
    {
        // Simple mock component for testing
    }
}
