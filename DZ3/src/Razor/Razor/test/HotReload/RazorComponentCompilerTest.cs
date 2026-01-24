// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Razor.Language;
using Microsoft.Extensions.Logging;
using Moq;
using Xunit;

namespace Microsoft.AspNetCore.Razor.HotReload.Tests;

public class RazorComponentCompilerTest
{
    private readonly Mock<ILogger<RazorComponentCompiler>> _mockLogger;
    private readonly RazorComponentCompiler _compiler;

    public RazorComponentCompilerTest()
    {
        _mockLogger = new Mock<ILogger<RazorComponentCompiler>>();
        _compiler = new RazorComponentCompiler(_mockLogger.Object);
    }

    [Fact]
    public void Constructor_ThrowsArgumentNullException_WhenLoggerIsNull()
    {
        Assert.Throws<ArgumentNullException>(() => new RazorComponentCompiler(null));
    }

    [Fact]
    public async Task RecompileComponentAsync_ThrowsArgumentException_WhenComponentPathIsNull()
    {
        await Assert.ThrowsAsync<ArgumentException>(() =>
            _compiler.RecompileComponentAsync(null));
    }

    [Fact]
    public async Task RecompileComponentAsync_ThrowsArgumentException_WhenComponentPathIsEmpty()
    {
        await Assert.ThrowsAsync<ArgumentException>(() =>
            _compiler.RecompileComponentAsync(string.Empty));
    }

    [Fact]
    public async Task RecompileComponentAsync_ThrowsFileNotFoundException_WhenComponentFileDoesNotExist()
    {
        var nonExistentPath = Path.Combine(Path.GetTempPath(), "NonExistent.razor");

        await Assert.ThrowsAsync<FileNotFoundException>(() =>
            _compiler.RecompileComponentAsync(nonExistentPath));
    }

    [Fact]
    public async Task RecompileComponentAsync_ReturnsFailureResult_WhenComponentHasSyntaxErrors()
    {
        var testDirectory = Path.Combine(Path.GetTempPath(), "RazorCompilerTest_" + Guid.NewGuid().ToString());
        Directory.CreateDirectory(testDirectory);

        try
        {
            var testFile = Path.Combine(testDirectory, "InvalidComponent.razor");
            File.WriteAllText(testFile, "<h1>Invalid Razor Syntax @</h1>"); // Invalid syntax

            var result = await _compiler.RecompileComponentAsync(testFile);

            Assert.False(result.Success);
            Assert.NotNull(result.Diagnostics);
            Assert.NotEmpty(result.Diagnostics);
        }
        finally
        {
            if (Directory.Exists(testDirectory))
            {
                Directory.Delete(testDirectory, true);
            }
        }
    }

    [Fact]
    public async Task RecompileComponentAsync_ReturnsSuccessResult_WhenComponentIsValid()
    {
        var testDirectory = Path.Combine(Path.GetTempPath(), "RazorCompilerTest_" + Guid.NewGuid().ToString());
        Directory.CreateDirectory(testDirectory);

        try
        {
            var testFile = Path.Combine(testDirectory, "ValidComponent.razor");
            File.WriteAllText(testFile, "<h1>Hello World</h1>");

            var result = await _compiler.RecompileComponentAsync(testFile);

            Assert.True(result.Success);
            Assert.NotNull(result.CompiledAssembly);
            Assert.NotNull(result.GeneratedCode);
            Assert.Empty(result.Diagnostics);
        }
        finally
        {
            if (Directory.Exists(testDirectory))
            {
                Directory.Delete(testDirectory, true);
            }
        }
    }

    [Fact]
    public async Task GetCachedResult_ReturnsNull_WhenComponentNotCached()
    {
        var testFile = Path.Combine(Path.GetTempPath(), "NotCached.razor");

        var result = _compiler.GetCachedResult(testFile);

        Assert.Null(result);
    }

    [Fact]
    public async Task ClearCache_RemovesAllCachedResults()
    {
        var testDirectory = Path.Combine(Path.GetTempPath(), "RazorCompilerTest_" + Guid.NewGuid().ToString());
        Directory.CreateDirectory(testDirectory);

        try
        {
            var testFile1 = Path.Combine(testDirectory, "Component1.razor");
            var testFile2 = Path.Combine(testDirectory, "Component2.razor");

            File.WriteAllText(testFile1, "<h1>Component 1</h1>");
            File.WriteAllText(testFile2, "<h1>Component 2</h1>");

            // Compile components to populate cache
            await _compiler.RecompileComponentAsync(testFile1);
            await _compiler.RecompileComponentAsync(testFile2);

            // Verify cache has entries
            Assert.NotNull(_compiler.GetCachedResult(testFile1));
            Assert.NotNull(_compiler.GetCachedResult(testFile2));

            // Clear cache
            _compiler.ClearCache();

            // Verify cache is empty
            Assert.Null(_compiler.GetCachedResult(testFile1));
            Assert.Null(_compiler.GetCachedResult(testFile2));
        }
        finally
        {
            if (Directory.Exists(testDirectory))
            {
                Directory.Delete(testDirectory, true);
            }
        }
    }

    [Fact]
    public async Task RecompileComponentAsync_HandlesExceptionGracefully()
    {
        var testDirectory = Path.Combine(Path.GetTempPath(), "RazorCompilerTest_" + Guid.NewGuid().ToString());
        Directory.CreateDirectory(testDirectory);

        try
        {
            var testFile = Path.Combine(testDirectory, "TestComponent.razor");
            File.WriteAllText(testFile, "<h1>Test Component</h1>");

            // This should not throw an exception, but return a failure result
            var result = await _compiler.RecompileComponentAsync(testFile);

            // The result should indicate success or failure, but not throw
            Assert.NotNull(result);
            Assert.Equal(testFile, result.ComponentPath);
        }
        finally
        {
            if (Directory.Exists(testDirectory))
            {
                Directory.Delete(testDirectory, true);
            }
        }
    }
}
