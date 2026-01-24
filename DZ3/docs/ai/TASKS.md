
# ASP.NET Core Razor Project - Typical Tasks and Prompts
This document contains common tasks and corresponding prompts for working with the ASP.NET Core Razor project.

## Development Tasks

### 1. Creating New TagHelpers

**Task**: Create a new custom TagHelper for specific HTML element processing

**Prompt**:
```
Create a new TagHelper class that processes [specific HTML element] and [specific functionality].
The TagHelper should:
- Target the [element name] HTML element
- [List specific behaviors, e.g., "add CSS classes", "modify attributes", "transform content"]
- Follow the existing code patterns in the project
- Include proper XML documentation
- Add appropriate unit tests

Please provide:
1. The TagHelper class implementation
2. Example usage in Razor syntax
3. Unit tests following the existing test patterns
4. Any necessary configuration or registration code
```

**Example**:
```
Create a new TagHelper class that processes <button> elements and adds accessibility attributes.
The TagHelper should:
- Target button elements
- Add aria-label attribute if not present
- Add type="button" if not specified
- Follow the existing code patterns in the project
- Include proper XML documentation
- Add appropriate unit tests
```

### 2. Modifying Existing TagHelpers

**Task**: Enhance or fix an existing TagHelper

**Prompt**:
```
[Describe the specific change needed for the TagHelper]
- Current behavior: [describe current behavior]
- Expected behavior: [describe desired behavior]
- Affected TagHelper: [name of TagHelper class]

Please:
1. Analyze the current implementation
2. Identify the root cause of the issue
3. Implement the fix following project patterns
4. Add or update unit tests
5. Verify the change doesn't break existing functionality
```

### 3. Performance Optimization

**Task**: Optimize TagHelper performance

**Prompt**:
```
Analyze the [specific TagHelper or component] for performance bottlenecks and optimize it.

Focus on:
- Memory allocation patterns
- String manipulation efficiency
- Collection operations
- HTML encoding performance
- Async vs sync processing

Please:
1. Profile the current implementation
2. Identify performance issues
3. Implement optimizations
4. Add performance benchmarks if applicable
5. Ensure functionality remains unchanged
```

## Testing Tasks

### 4. Adding Unit Tests

**Task**: Add comprehensive unit tests for a component

**Prompt**:
```
Add comprehensive unit tests for [specific class or component].

Test coverage should include:
- Happy path scenarios
- Edge cases and boundary conditions
- Error conditions and exception handling
- Input validation
- State transitions (if applicable)

Follow the existing test patterns:
- Use xUnit framework
- Follow naming conventions
- Use appropriate test data and fixtures
- Mock dependencies appropriately
- Test both synchronous and asynchronous methods

Please provide:
1. Complete test class implementation
2. Test data setup and teardown
3. Mock configurations
4. Assertion patterns that match existing tests
```

### 5. Integration Testing

**Task**: Create integration tests for TagHelper functionality

**Prompt**:
```
Create integration tests for [specific TagHelper or feature] that test the complete rendering pipeline.

Tests should verify:
- End-to-end HTML generation
- TagHelper interaction with other components
- Runtime behavior in realistic scenarios
- Error handling in integration context

Please:
1. Set up appropriate test infrastructure
2. Create realistic test scenarios
3. Verify HTML output matches expectations
4. Test error conditions and edge cases
5. Ensure tests are maintainable and fast
```

## Architecture and Design Tasks

### 6. Refactoring Legacy Code

**Task**: Refactor existing code to improve maintainability

**Prompt**:
```
Refactor the [specific class or module] to improve code quality and maintainability.

Focus on:
- Reducing cyclomatic complexity
- Improving separation of concerns
- Enhancing readability and documentation
- Following SOLID principles
- Removing code duplication

Please:
1. Analyze the current implementation
2. Identify refactoring opportunities
3. Create a refactoring plan
4. Implement changes incrementally
5. Ensure all tests pass after refactoring
6. Update documentation as needed
```

### 7. Adding New Features

**Task**: Implement a new feature for the Razor runtime

**Prompt**:
```
Implement [specific feature] for the Razor runtime system.

Requirements:
- [List functional requirements]
- [List non-functional requirements like performance, security]
- [List compatibility requirements]

Design considerations:
- Integration with existing architecture
- Backward compatibility
- Performance impact
- Security implications

Please provide:
1. Technical design document
2. Implementation plan
3. Code implementation
4. Test strategy
5. Documentation updates
```

## Build and Configuration Tasks

### 8. Build System Improvements

**Task**: Improve the build system or CI/CD pipeline

**Prompt**:
```
Analyze and improve the build system for the Razor project.

Areas to consider:
- Build performance optimization
- Dependency management
- Package publishing
- Testing automation
- Code analysis integration

Please:
1. Audit current build configuration
2. Identify improvement opportunities
3. Propose specific changes
4. Implement selected improvements
5. Verify changes don't break existing functionality
```

### 9. Documentation Updates

**Task**: Update or create documentation

**Prompt**:
```
Create or update documentation for [specific feature or component].

Documentation should include:
- API reference documentation
- Usage examples and tutorials
- Architecture diagrams (if applicable)
- Migration guides (if applicable)
- Best practices

Please:
1. Analyze existing documentation
2. Identify gaps or outdated content
3. Create comprehensive documentation
4. Ensure consistency with project style
5. Include code examples where appropriate
```

## Debugging and Troubleshooting Tasks

### 10. Bug Investigation

**Task**: Investigate and fix a specific bug

**Prompt**:
```
Investigate the bug described in [issue/bug report].

Symptoms:
- [List observed symptoms]
- [List reproduction steps]
- [List affected environments]

Expected behavior:
- [Describe what should happen]

Please:
1. Reproduce the issue locally
2. Analyze the root cause
3. Identify the problematic code
4. Implement a fix
5. Add regression tests
6. Verify the fix resolves the issue
```

### 11. Performance Investigation

**Task**: Investigate performance issues

**Prompt**:
```
Investigate performance issues with [specific component or scenario].

Symptoms:
- [Describe performance problems]
- [List affected operations]
- [Include any metrics or benchmarks]

Expected performance:
- [Describe acceptable performance levels]

Please:
1. Profile the problematic code
2. Identify bottlenecks
3. Analyze resource usage patterns
4. Propose optimization strategies
5. Implement and test improvements
6. Verify performance meets requirements
```

## Code Review and Quality Tasks

### 12. Code Review Preparation

**Task**: Prepare code for review

**Prompt**:
```
Review the following code changes for [specific feature or fix]:

[Include code changes or describe the changes]

Please verify:
1. Code follows project conventions and style
2. Implementation is correct and complete
3. Tests are comprehensive and passing
4. Documentation is up to date
5. No security vulnerabilities introduced
6. Performance impact is acceptable
7. Backward compatibility is maintained

Provide feedback on:
- Code quality and readability
- Test coverage
- Documentation completeness
- Potential issues or improvements
```

### 13. API Design Review

**Task**: Review API design for new features

**Prompt**:
```
Review the API design for [new feature or component].

API specification:
[Include API design or describe the interface]

Please evaluate:
1. API consistency with existing patterns
2. Usability and developer experience
3. Extensibility and maintainability
4. Performance implications
5. Security considerations
6. Error handling strategy

Provide recommendations for:
- API improvements
- Naming conventions
- Documentation needs
- Testing strategy
```

## Migration and Compatibility Tasks

### 14. Version Migration

**Task**: Migrate code to new framework version

**Prompt**:
```
Migrate the [specific component or project] to work with [new version].

Changes required:
- [List breaking changes that affect the code]
- [List new features to leverage]
- [List deprecated features to replace]

Please:
1. Analyze impact of version changes
2. Create migration plan
3. Implement necessary changes
4. Update dependencies
5. Test compatibility
6. Update documentation
```

### 15. Cross-Platform Compatibility

**Task**: Ensure cross-platform compatibility

**Prompt**:
```
Verify and improve cross-platform compatibility for [specific feature].

Platforms to support:
- Windows
- Linux
- macOS

Areas to verify:
- File system operations
- Path handling
- Encoding differences
- Platform-specific APIs
- Performance characteristics

Please:
1. Test on all target platforms
2. Identify platform-specific issues
3. Implement platform-agnostic solutions
4. Add platform-specific optimizations where needed
5. Update build configuration if required
```

## Security and Compliance Tasks

### 16. Security Audit

**Task**: Perform security audit of code

**Prompt**:
```
Perform a security audit of [specific component or feature].

Security aspects to review:
- Input validation and sanitization
- Output encoding
- Authentication and authorization
- Data protection
- Error handling (information disclosure)
- Dependency security

Please:
1. Review code for security vulnerabilities
2. Check for common security issues
3. Verify secure coding practices
4. Assess dependency security
5. Provide security recommendations
6. Document any security fixes needed
```

### 17. Compliance Verification

**Task**: Verify compliance with standards

**Prompt**:
```
Verify compliance of [specific component] with [specific standard or requirement].

Standards to verify:
- [List applicable standards, e.g., accessibility, data protection]
- [List internal coding standards]
- [List regulatory requirements]

Please:
1. Review code against standards
2. Identify compliance gaps
3. Implement necessary changes
4. Add compliance documentation
5. Create compliance test cases
```

## Performance and Monitoring Tasks

### 18. Benchmarking and Profiling

**Task**: Create performance benchmarks

**Prompt**:
```
Create performance benchmarks for [specific component or operation].

Benchmark requirements:
- [List operations to benchmark]
- [List performance metrics to measure]
- [List test scenarios]

Please:
1. Design appropriate benchmarks
2. Implement benchmark code
3. Establish baseline measurements
4. Create performance regression tests
5. Document performance characteristics
```

### 19. Monitoring and Observability

**Task**: Add monitoring and observability

**Prompt**:
```
Add monitoring and observability features to [specific component].

Monitoring requirements:
- [List metrics to track]
- [List logs to generate]
- [List events to emit]
- [List alerts to configure]

Please:
1. Design monitoring strategy
2. Implement telemetry collection
3. Add appropriate logging
4. Create dashboards or reports
5. Configure alerting if needed
```

## Collaboration and Communication Tasks

### 20. Technical Documentation

**Task**: Create technical documentation

**Prompt**:
```
Create technical documentation for [specific feature or component].

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

### 21. Knowledge Transfer

**Task**: Prepare knowledge transfer materials

**Prompt**:
```
Prepare knowledge transfer materials for [specific topic or component].

Materials should include:
- Overview presentation
- Detailed technical documentation
- Code walkthrough
- Common troubleshooting scenarios
- Best practices guide

Please:
1. Identify key concepts to transfer
2. Create structured learning materials
3. Include practical examples
4. Prepare Q&A documentation
5. Ensure materials are up-to-date and accurate
```

## Emergency and Hotfix Tasks

### 22. Hotfix Implementation

**Task**: Implement emergency hotfix

**Prompt**:
```
Implement a hotfix for [critical issue].

Issue details:
- [Describe the critical issue]
- [List affected users/systems]
- [List urgency and impact]

Requirements:
- Minimal code changes
- Maximum compatibility
- Thorough testing
- Clear rollback plan

Please:
1. Analyze the issue quickly but thoroughly
2. Design minimal impact fix
3. Implement and test the fix
4. Prepare deployment instructions
5. Document rollback procedure
```

### 23. Incident Response

**Task**: Respond to production incident

**Prompt**:
```
Respond to production incident affecting [specific component].

Incident details:
- [Describe the incident]
- [List affected systems]
- [List user impact]

Response requirements:
- Quick diagnosis
- Effective communication
- Minimal disruption
- Root cause analysis
- Preventive measures

Please:
1. Diagnose the issue
2. Implement immediate fix if possible
3. Communicate status to stakeholders
4. Perform root cause analysis
5. Implement preventive measures
```

## Research and Investigation Tasks

### 24. Technology Research

**Task**: Research new technologies or approaches

**Prompt**:
```
Research [specific technology or approach] for potential use in the Razor project.

Research should cover:
- Technology overview and capabilities
- Integration possibilities
- Performance characteristics
- Security implications
- Community and ecosystem
- Migration path if applicable

Please:
1. Conduct thorough research
2. Evaluate pros and cons
3. Assess fit with project goals
4. Create recommendation report
5. Provide implementation guidance if positive recommendation
```

### 25. Best Practices Analysis

**Task**: Analyze and improve development practices

**Prompt**:
```
Analyze current development practices for [specific area] and propose improvements.

Areas to analyze:
- [List specific practices to review]
- [List metrics to consider]
- [List goals for improvement]

Please:
1. Assess current practices
2. Identify improvement opportunities
3. Research industry best practices
4. Propose specific improvements
5. Create implementation plan
```

## Template Usage Notes

- Replace bracketed placeholders `[...]` with specific details
- Customize prompts based on project context and requirements
- Use multiple prompts for complex tasks that require different approaches
- Adapt task descriptions based on urgency and complexity
- Consider combining related tasks for efficiency
- Always include relevant context and constraints
