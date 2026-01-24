# VCCode + CLine (ket-coder-pro)
# Project
ASP NET CORE Razor https://github.com/dotnet/aspnetcore.git
# Task Prompts

This document contains the prompts from the completed tasks.

## Task 1: ButtonAccessibilityTagHelper Implementation

**Prompt**:
```
Create a new TagHelper class that processes `<button>` elements and adds accessibility attributes. The TagHelper should:
- Target button elements
- Add aria-label attribute if not present
- Add type="button" if not specified
- Follow the existing code patterns in the project
- Include proper XML documentation
- Add appropriate unit tests
```

## Task 2: ButtonAccessibilityTagHelper Technical Documentation

**Prompt**:
```
Create technical documentation for ButtonAccessibilityTagHelper.

Documentation should include:
- Architecture overview
- Implementation details
- Usage examples
- Troubleshooting guide
- Performance characteristics
- Security considerations

Please:
1. Analyze the component thoroughly
2. Create comprehensive documentation
3. Include diagrams where helpful
4. Provide practical examples
5. Ensure documentation is maintainable
```

## Task 3: Razor Component Hot Reload Implementation

**Prompt**:
```
Implement **Razor Component Hot Reload** for the Razor runtime system.

Requirements:
- Functional Requirements:
  - Detect changes to Razor component files (.razor) during development
  - Automatically recompile and reload components without full application restart
  - Preserve component state during hot reload when possible
  - Provide visual feedback to developers about reload status

- Non-Functional Requirements:
  - Performance: Reload should complete within 2 seconds for typical components
  - Security: Only enable in development environments
  - Compatibility: Work with existing Razor component infrastructure
  - Reliability: Graceful fallback to full restart if hot reload fails

- Compatibility Requirements:
  - Support .NET 11.0 and later
  - Compatible with existing Razor component lifecycle
  - No breaking changes to existing APIs
```

## AI Documentation

This project includes comprehensive AI documentation in the `docs/ai/` directory:

### CONTEXT.md
Provides detailed context about the ASP.NET Core Razor project, including:
- Project overview and architecture
- Core components (Razor Library and Razor Runtime)
- TagHelper system design and implementation
- Build configuration and development workflow
- Integration points with ASP.NET Core ecosystem
- Performance characteristics and extensibility features

### STYLEGUIDE.md
Defines comprehensive coding standards and conventions:
- C# language standards and naming conventions
- Code formatting and documentation requirements
- Architecture patterns for TagHelpers and collections
- Testing standards with xUnit framework
- Performance guidelines and security best practices
- Build and configuration standards
- Code review checklist and quality assurance processes

### TASKS.md
Contains 25+ common development tasks and corresponding prompts:
- Development tasks (TagHelper creation, performance optimization)
- Testing tasks (unit tests, integration tests)
- Architecture and design tasks (refactoring, new features)
- Build and configuration tasks (CI/CD, documentation)
- Debugging and troubleshooting tasks (bug investigation, performance issues)
- Security and compliance tasks (security audits, compliance verification)
- Emergency and hotfix tasks (incident response, hotfix implementation)
- Research and investigation tasks (technology research, best practices)

These AI documentation files serve as comprehensive guides for developers working on the ASP.NET Core Razor project, providing clear standards, common task patterns, and project context to ensure consistent and high-quality development practices.
