# ASP.NET Core Razor Project Context

## Project Overview

**ASP.NET Core Razor** is a fast, terse, clean, and lightweight markup syntax that combines server-side C# code with HTML to create dynamic web content. This project contains the parser and C# code generator for the Razor syntax, which is a core component of ASP.NET Core.

## Project Structure

### Root Directory (`aspnetcore/src/Razor/`)
- **Build System**: Uses MSBuild with `.slnf` (solution filter) files for project management
- **Target Framework**: .NET 11.0 (based on global.json configuration)
- **Build Tools**: `build.cmd` and `build.sh` for cross-platform builds
- **IDE Support**: Visual Studio Code configuration via `.vsconfig`

### Core Components

#### 1. **Razor Library** (`src/Razor/src/`)
- **Purpose**: Core Razor functionality and TagHelper infrastructure
- **Key Features**:
  - TagHelper system for server-side HTML processing
  - HTML attribute and content manipulation
  - Server-side rendering capabilities
- **Main Classes**:
  - `TagHelper` - Base class for all tag helpers
  - `TagHelperAttribute` - Represents HTML attributes
  - `TagHelperAttributeList` - Collection of tag helper attributes
  - `TagHelperContent` - HTML content manipulation
  - `TagHelperOutput` - Output generation for tag helpers

#### 2. **Razor Runtime** (`src/Razor.Runtime/src/`)
- **Purpose**: Runtime infrastructure for rendering Razor pages and tag helpers
- **Key Features**:
  - Compiled item hosting and loading
  - Tag helper execution context
  - Runtime tag helper processing
- **Main Classes**:
  - `RazorCompiledItem` - Base class for compiled Razor items
  - `TagHelperExecutionContext` - Execution context for tag helpers
  - `TagHelperRunner` - Executes tag helpers
  - `RazorCompiledItemLoader` - Loads compiled Razor items

## Architecture

### TagHelper System
The TagHelper system allows developers to create server-side code that can modify HTML elements during rendering:

```csharp
[HtmlTargetElement("custom-element")]
public class CustomTagHelper : TagHelper
{
    public override void Process(TagHelperContext context, TagHelperOutput output)
    {
        // Modify output HTML
        output.Content.SetContent("Modified content");
    }
}
```

### Compilation Model
- Razor files are compiled into C# classes at build time
- Compiled items implement `RazorCompiledItem` interface
- Runtime loading and execution through `RazorCompiledItemLoader`

### Build Configuration
- **Nullable Context**: Disabled (`<Nullable>disable</Nullable>`)
- **Unsafe Code**: Enabled for HTML encoding optimizations
- **Shared Framework**: Part of Microsoft.AspNetCore.App shared framework
- **Packaging**: Not directly packable (`<IsPackable>false</IsPackable>`)

## Dependencies

### Core Dependencies
- `Microsoft.AspNetCore.Html.Abstractions` - HTML abstraction layer
- `Microsoft.AspNetCore.Razor` - Core Razor functionality (for runtime)

### Testing Framework
- Uses xUnit for unit testing
- Test projects mirror source structure
- Comprehensive test coverage for TagHelper functionality

## Development Workflow

### Building the Project
```bash
# Windows
.\build.cmd

# Linux/macOS
./build.sh
```

### Testing
- Unit tests located in corresponding `test/` directories
- Test files use `xunit.runner.json` configuration
- Tests cover TagHelper functionality, attribute manipulation, and runtime execution

### IDE Integration
- Solution filter: `Razor.slnf` includes all 4 main projects
- Visual Studio Code support via `startvscode.cmd/sh`
- Visual Studio support via `startvs.cmd`

## Key Features

### 1. **TagHelper Infrastructure**
- Extensible system for creating custom HTML element processors
- Attribute-based configuration and targeting
- Content manipulation and transformation
- Support for both synchronous and asynchronous processing

### 2. **HTML Processing**
- Server-side HTML attribute manipulation
- Content modification and replacement
- Element structure modification
- Support for different tag modes (self-closing, normal, etc.)

### 3. **Compilation and Runtime**
- Build-time compilation of Razor syntax to C#
- Runtime loading and execution of compiled items
- Metadata-driven compilation with source checksums
- Extension point system for custom compilation

### 4. **Performance Optimizations**
- Unsafe code blocks for HTML encoding performance
- Copy-on-write dictionary implementations
- Efficient attribute list management
- Optimized string handling for HTML content

## Integration Points

### ASP.NET Core Ecosystem
- Part of the Microsoft.AspNetCore.App shared framework
- Integrates with MVC and Pages frameworks
- Works with dependency injection system
- Supports localization and resource management

### Development Tools
- Razor compiler integration
- IntelliSense support in Visual Studio
- Debugging support for compiled Razor files
- Hot reload capabilities

## Project Management

### Versioning
- Follows ASP.NET Core versioning scheme
- Part of .NET 11.0 development cycle
- Shared framework versioning through `IsAspNetCoreApp=true`

### Quality Assurance
- API baseline management with PublicAPI.Shipped.txt and PublicAPI.Unshipped.txt
- Comprehensive unit testing
- Code analysis and static checking
- Performance benchmarking integration

### Documentation
- API documentation generation enabled
- XML documentation comments throughout codebase
- Integration with ASP.NET Core documentation system

## Technical Notes

### Security Considerations
- HTML encoding built into attribute and content handling
- XSS protection through proper encoding
- Secure by default attribute processing

### Performance Characteristics
- Compile-time processing reduces runtime overhead
- Efficient memory usage through shared string handling
- Optimized for high-throughput web scenarios

### Extensibility
- Plugin architecture for custom tag helpers
- Extension point system for compilation pipeline
- Support for custom HTML encoders and decoders

This project represents a mature, production-ready implementation of server-side HTML processing that forms the foundation for modern ASP.NET Core web development.
