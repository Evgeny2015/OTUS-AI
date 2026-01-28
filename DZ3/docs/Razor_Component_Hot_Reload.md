# Razor Component Hot Reload Implementation

## Overview

This document describes the implementation of **Razor Component Hot Reload** for the ASP.NET Core Razor runtime system. The implementation provides automatic recompilation and reloading of Razor components during development without requiring a full application restart.

## Architecture

### Core Components

1. **RazorComponentHotReloadService** - Main orchestrator for hot reload functionality
2. **RazorComponentFileWatcher** - Monitors .razor files for changes
3. **RazorComponentCompiler** - Handles component recompilation
4. **ComponentStateManager** - Manages component state preservation
5. **HotReloadFeedbackService** - Provides visual feedback to developers

### Integration Points

- Extends existing `Renderer` class with hot reload capabilities
- Integrates with `HotReloadManager` for metadata update handling
- Uses `FileSystemWatcher` for file monitoring
- Leverages existing Razor compilation infrastructure

## Implementation Details

### 1. File System Monitoring

```csharp
public class RazorComponentFileWatcher : IDisposable
{
    private readonly FileSystemWatcher _watcher;
    private readonly ILogger<RazorComponentFileWatcher> _logger;

    public RazorComponentFileWatcher(string projectPath, ILogger<RazorComponentFileWatcher> logger)
    {
        _logger = logger;
        _watcher = new FileSystemWatcher(projectPath, "*.razor")
        {
            EnableRaisingEvents = true,
            IncludeSubdirectories = true,
            NotifyFilter = NotifyFilters.LastWrite | NotifyFilters.FileName | NotifyFilters.DirectoryName
        };

        _watcher.Changed += OnFileChanged;
        _watcher.Created += OnFileChanged;
        _watcher.Renamed += OnFileRenamed;
    }
}
```

### 2. Component Recompilation

```csharp
public class RazorComponentCompiler
{
    public async Task<CompilationResult> RecompileComponentAsync(string componentPath)
    {
        var stopwatch = Stopwatch.StartNew();

        try
        {
            // Parse Razor syntax
            var razorParser = new RazorParser();
            var syntaxTree = await razorParser.ParseAsync(componentPath);

            // Generate C# code
            var codeGenerator = new RazorCodeGenerator();
            var generatedCode = codeGenerator.GenerateCode(syntaxTree);

            // Compile to assembly
            var compiler = new CSharpCompiler();
            var compilationResult = await compiler.CompileAsync(generatedCode);

            stopwatch.Stop();
            _logger.LogInformation("Component recompiled in {Duration}ms", stopwatch.ElapsedMilliseconds);

            return compilationResult;
        }
        catch (Exception ex)
        {
            stopwatch.Stop();
            _logger.LogError(ex, "Failed to recompile component in {Duration}ms", stopwatch.ElapsedMilliseconds);
            throw;
        }
    }
}
```

### 3. State Preservation

```csharp
public class ComponentStateManager
{
    private readonly Dictionary<int, ComponentStateSnapshot> _stateSnapshots = new();

    public void CaptureState(ComponentState componentState)
    {
        var snapshot = new ComponentStateSnapshot
        {
            ComponentId = componentState.ComponentId,
            Parameters = componentState.Parameters,
            RenderTree = componentState.CurrentRenderTree,
            Timestamp = DateTime.UtcNow
        };

        _stateSnapshots[componentState.ComponentId] = snapshot;
    }

    public bool RestoreState(ComponentState componentState)
    {
        if (_stateSnapshots.TryGetValue(componentState.ComponentId, out var snapshot))
        {
            componentState.SetParameters(snapshot.Parameters);
            return true;
        }
        return false;
    }
}
```

### 4. Hot Reload Integration

```csharp
public partial class Renderer
{
    private RazorComponentHotReloadService _hotReloadService;

    protected override void InitializeHotReload()
    {
        if (Environment.IsDevelopment())
        {
            _hotReloadService = new RazorComponentHotReloadService(
                this,
                _serviceProvider,
                _logger
            );

            _hotReloadService.ComponentReloaded += OnComponentReloaded;
            _hotReloadService.StartWatching();
        }
    }

    private void OnComponentReloaded(ComponentReloadEventArgs args)
    {
        _logger.LogInformation("Component {Component} reloaded successfully", args.ComponentName);

        // Trigger re-render with preserved state
        Dispatcher.InvokeAsync(() =>
        {
            var componentState = GetComponentState(args.ComponentId);
            if (componentState != null)
            {
                componentState.SetDirectParameters(args.RestoredParameters);
                AddToRenderQueue(args.ComponentId, componentState.RenderFragment);
            }
        });
    }
}
```

## Performance Optimizations

### 1. Incremental Compilation

- Only recompile changed components and their dependencies
- Cache compilation results for unchanged components
- Use parallel compilation for independent components

### 2. State Management

- Preserve component state during reload when possible
- Graceful degradation when state cannot be preserved
- Efficient state serialization/deserialization

### 3. File Watching

- Debounce file change events to handle rapid successive changes
- Filter out temporary files and build artifacts
- Use efficient file system notification mechanisms

## Security Considerations

### 1. Development-Only Feature

```csharp
public class RazorComponentHotReloadService
{
    public RazorComponentHotReloadService(IServiceProvider serviceProvider)
    {
        var environment = serviceProvider.GetRequiredService<IHostEnvironment>();

        if (!environment.IsDevelopment())
        {
            throw new InvalidOperationException(
                "Hot reload is only available in development environments"
            );
        }
    }
}
```

### 2. Input Validation

- Validate all file paths to prevent directory traversal
- Sanitize component names and parameters
- Limit compilation time to prevent DoS attacks

## Error Handling and Fallbacks

### 1. Graceful Degradation

```csharp
public async Task<ComponentReloadResult> ReloadComponentAsync(string componentPath)
{
    try
    {
        var compilationResult = await _compiler.RecompileComponentAsync(componentPath);

        if (compilationResult.Success)
        {
            return await ApplyComponentUpdate(compilationResult);
        }
        else
        {
            _logger.LogWarning("Component compilation failed, falling back to full restart");
            return ComponentReloadResult.FallbackToRestart;
        }
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Hot reload failed, falling back to full restart");
        return ComponentReloadResult.FallbackToRestart;
    }
}
```

### 2. Rollback Mechanism

- Keep previous component version available during reload
- Automatically rollback if new version fails to load
- Maintain application stability during failed reloads

## Visual Feedback System

### 1. Developer Notifications

```csharp
public class HotReloadFeedbackService
{
    public void ShowReloadNotification(string componentName, bool success)
    {
        var message = success
            ? $"Component '{componentName}' reloaded successfully"
            : $"Failed to reload component '{componentName}'";

        var level = success ? LogLevel.Information : LogLevel.Warning;
        _logger.Log(level, message);

        // Send to browser console if available
        if (_browserConsole != null)
        {
            _browserConsole.Log(success ? "info" : "warn", message);
        }
    }
}
```

### 2. Status Indicators

- Visual indicators in development tools
- Progress bars for long compilation operations
- Error overlays for compilation failures

## Testing Strategy

### 1. Unit Tests

- File watcher functionality
- Component compilation pipeline
- State preservation logic
- Error handling scenarios

### 2. Integration Tests

- End-to-end hot reload workflow
- State preservation across multiple reloads
- Performance benchmarks
- Error recovery mechanisms

### 3. Performance Tests

- Compilation time measurements
- Memory usage during reload operations
- Concurrent reload scenarios
- Large project scalability

## Configuration

### 1. Development Settings

```json
{
  "HotReload": {
    "Enabled": true,
    "DebounceDelay": 300,
    "MaxConcurrentReloads": 3,
    "PreserveState": true,
    "ShowNotifications": true
  }
}
```

### 2. Performance Tuning

```csharp
public class HotReloadOptions
{
    public bool Enabled { get; set; } = true;
    public int DebounceDelay { get; set; } = 300; // milliseconds
    public int MaxConcurrentReloads { get; set; } = 3;
    public bool PreserveState { get; set; } = true;
    public bool ShowNotifications { get; set; } = true;
    public TimeSpan CompilationTimeout { get; set; } = TimeSpan.FromSeconds(10);
}
```

## Compatibility

### 1. .NET Version Support

- Requires .NET 11.0 or later
- Compatible with existing Razor component lifecycle
- No breaking changes to existing APIs

### 2. Framework Integration

- Works with existing Razor compilation infrastructure
- Compatible with dependency injection
- Supports custom component render modes

## Future Enhancements

### 1. Advanced Features

- Live editing with immediate preview
- Component dependency analysis for smarter reloading
- Performance profiling integration

### 2. Developer Experience

- Enhanced error messages with suggestions
- Integration with development IDEs
- Custom hot reload plugins

This implementation provides a robust, performant, and secure hot reload system for Razor components that significantly improves the development experience while maintaining application stability and security.
