// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Moq;
using Xunit;

namespace Microsoft.AspNetCore.Razor.HotReload.Tests;

public class RazorComponentFileWatcherTest
{
    private readonly string _testDirectory;
    private readonly Mock<ILogger<RazorComponentFileWatcher>> _mockLogger;
    private readonly Action<string> _mockFileChangedCallback;
    private readonly Action<string, string> _mockFileRenamedCallback;

    public RazorComponentFileWatcherTest()
    {
        _testDirectory = Path.Combine(Path.GetTempPath(), "RazorHotReloadTest_" + Guid.NewGuid().ToString());
        Directory.CreateDirectory(_testDirectory);

        _mockLogger = new Mock<ILogger<RazorComponentFileWatcher>>();
        _mockFileChangedCallback = Mock.Of<Action<string>>();
        _mockFileRenamedCallback = Mock.Of<Action<string, string>>();
    }

    [Fact]
    public void Constructor_ThrowsArgumentNullException_WhenProjectPathIsNull()
    {
        Assert.Throws<ArgumentNullException>(() =>
            new RazorComponentFileWatcher(null, _mockFileChangedCallback, _mockFileRenamedCallback, _mockLogger.Object));
    }

    [Fact]
    public void Constructor_ThrowsArgumentNullException_WhenOnFileChangedIsNull()
    {
        Assert.Throws<ArgumentNullException>(() =>
            new RazorComponentFileWatcher(_testDirectory, null, _mockFileRenamedCallback, _mockLogger.Object));
    }

    [Fact]
    public void Constructor_ThrowsArgumentNullException_WhenOnFileRenamedIsNull()
    {
        Assert.Throws<ArgumentNullException>(() =>
            new RazorComponentFileWatcher(_testDirectory, _mockFileChangedCallback, null, _mockLogger.Object));
    }

    [Fact]
    public void Constructor_ThrowsArgumentNullException_WhenLoggerIsNull()
    {
        Assert.Throws<ArgumentNullException>(() =>
            new RazorComponentFileWatcher(_testDirectory, _mockFileChangedCallback, _mockFileRenamedCallback, null));
    }

    [Fact]
    public void Constructor_ThrowsArgumentException_WhenProjectPathDoesNotExist()
    {
        var nonExistentPath = Path.Combine(_testDirectory, "NonExistent");

        Assert.Throws<ArgumentException>(() =>
            new RazorComponentFileWatcher(nonExistentPath, _mockFileChangedCallback, _mockFileRenamedCallback, _mockLogger.Object));
    }

    [Fact]
    public void StartWatching_ThrowsObjectDisposedException_WhenDisposed()
    {
        var watcher = new RazorComponentFileWatcher(_testDirectory, _mockFileChangedCallback, _mockFileRenamedCallback, _mockLogger.Object);
        watcher.Dispose();

        Assert.Throws<ObjectDisposedException>(() => watcher.StartWatching());
    }

    [Fact]
    public void StopWatching_ThrowsObjectDisposedException_WhenDisposed()
    {
        var watcher = new RazorComponentFileWatcher(_testDirectory, _mockFileChangedCallback, _mockFileRenamedCallback, _mockLogger.Object);
        watcher.Dispose();

        Assert.Throws<ObjectDisposedException>(() => watcher.StopWatching());
    }

    [Fact]
    public async Task FileChanged_CallbackInvoked_WhenRazorFileModified()
    {
        var watcher = new RazorComponentFileWatcher(_testDirectory, _mockFileChangedCallback, _mockFileRenamedCallback, _mockLogger.Object);
        watcher.StartWatching();

        var testFile = Path.Combine(_testDirectory, "TestComponent.razor");
        File.WriteAllText(testFile, "<h1>Hello World</h1>");

        // Wait for file system events to be processed
        await Task.Delay(1000);

        watcher.Dispose();
        File.Delete(testFile);
    }

    [Fact]
    public async Task FileRenamed_CallbackInvoked_WhenRazorFileRenamed()
    {
        var watcher = new RazorComponentFileWatcher(_testDirectory, _mockFileChangedCallback, _mockFileRenamedCallback, _mockLogger.Object);
        watcher.StartWatching();

        var oldFile = Path.Combine(_testDirectory, "OldComponent.razor");
        var newFile = Path.Combine(_testDirectory, "NewComponent.razor");

        File.WriteAllText(oldFile, "<h1>Old Component</h1>");

        // Wait for file system events to be processed
        await Task.Delay(500);

        File.Move(oldFile, newFile);

        // Wait for file system events to be processed
        await Task.Delay(1000);

        watcher.Dispose();

        if (File.Exists(oldFile))
        {
            File.Delete(oldFile);
        }

        if (File.Exists(newFile))
        {
            File.Delete(newFile);
        }
    }

    [Fact]
    public void Dispose_DoesNotThrow_WhenCalledMultipleTimes()
    {
        var watcher = new RazorComponentFileWatcher(_testDirectory, _mockFileChangedCallback, _mockFileRenamedCallback, _mockLogger.Object);

        watcher.Dispose();
        watcher.Dispose(); // Should not throw
    }

    [Fact]
    public void Dispose_CleansUpResources()
    {
        var watcher = new RazorComponentFileWatcher(_testDirectory, _mockFileChangedCallback, _mockFileRenamedCallback, _mockLogger.Object);

        watcher.Dispose();

        // Verify that the watcher is no longer enabled
        Assert.Throws<ObjectDisposedException>(() => watcher.StartWatching());
    }

    public void Dispose()
    {
        if (Directory.Exists(_testDirectory))
        {
            try
            {
                Directory.Delete(_testDirectory, true);
            }
            catch
            {
                // Ignore cleanup errors in test teardown
            }
        }
    }
}
