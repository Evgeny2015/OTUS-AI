# ASP.NET Core Razor Project - Style Guide

This document defines the coding standards, conventions, and requirements for the ASP.NET Core Razor project.

## Code Style Standards

### C# Language Standards

#### 1. **Language Version and Features**
- **Target Framework**: .NET 11.0
- **Nullable Context**: Disabled (`<Nullable>disable</Nullable>`)
- **Unsafe Code**: Enabled for HTML encoding optimizations
- **C# Language Version**: Latest supported by .NET 11.0

#### 2. **Naming Conventions**

**Classes and Interfaces**
```csharp
// PascalCase for all types
public class TagHelper
public interface ITagHelper
public class DefaultTagHelperContent
public class TagHelperAttributeList
```

**Methods and Properties**
```csharp
// PascalCase for public members
public void Process(TagHelperContext context, TagHelperOutput output)
public virtual int Order { get; }
public string Identifier { get; }
```

**Private Fields and Variables**
```csharp
// camelCase for private members
private readonly IHtmlEncoder _htmlEncoder;
private string _content;
```

**Constants and Static Members**
```csharp
// PascalCase for constants
private const string DefaultTagName = "div";
public static readonly AuthenticationEventSource Log = new AuthenticationEventSource();
```

#### 3. **Code Formatting**

**Indentation and Spacing**
```csharp
// Use 4 spaces for indentation (no tabs)
public class TagHelper : ITagHelper
{
    public virtual int Order { get; }

    public virtual void Process(TagHelperContext context, TagHelperOutput output)
    {
        // Implementation
    }
}
```

**Brace Style**
```csharp
// Opening braces on same line
public class TagHelper
{
    // Implementation
}

// Control structures
if (condition)
{
    // Implementation
}
else
{
    // Implementation
}
```

**Line Length**
- Maximum line length: 120 characters
- Break long lines at logical points
- Use continuation indentation for multi-line statements

### 4. **Documentation Standards**

**XML Documentation**
```csharp
/// <summary>
/// An abstract base class for <see cref="ITagHelper"/>.
/// </summary>
/// <remarks>
/// When a set of <see cref="ITagHelper"/>s are executed, their <see cref="Init(TagHelperContext)"/>'s
/// are first invoked in the specified <see cref="Order"/>; then their
/// <see cref="ProcessAsync(TagHelperContext, TagHelperOutput)"/>'s are invoked in the specified
/// <see cref="Order"/>. Lower values are executed first.
/// </remarks>
public abstract class TagHelper : ITagHelper
{
    /// <summary>
    /// When a set of <see cref="ITagHelper"/>s are executed, their <paramref name="context"/> and
    /// <paramref name="output"/> are first invoked in the specified <see cref="Order"/>; then their
    /// <see cref="ProcessAsync(TagHelperContext, TagHelperOutput)"/>'s are invoked in the specified
    /// <see cref="Order"/>. Lower values are executed first.
    /// </summary>
    /// <param name="context">Contains information associated with the current HTML tag.</param>
    /// <param name="output">A stateful HTML element used to generate an HTML tag.</param>
    public virtual void Process(TagHelperContext context, TagHelperOutput output)
    {
        // Implementation
    }
}
```

### 5. **Code Organization**

**Using Statements**
```csharp
// Group using statements logically
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

using Microsoft.AspNetCore.Html;
using Microsoft.AspNetCore.Razor.TagHelpers;
```

**Class Structure**
```csharp
public class TagHelper : ITagHelper
{
    // Constants
    private const string DefaultTagName = "div";

    // Fields
    private readonly IHtmlEncoder _htmlEncoder;

    // Properties
    public virtual int Order { get; }

    // Constructors
    public TagHelper()
    {
        // Implementation
    }

    // Public methods
    public virtual void Init(TagHelperContext context)
    {
        // Implementation
    }

    public virtual void Process(TagHelperContext context, TagHelperOutput output)
    {
        // Implementation
    }

    // Protected methods
    protected virtual void OnProcess(TagHelperContext context, TagHelperOutput output)
    {
        // Implementation
    }

    // Private methods
    private void ValidateContext(TagHelperContext context)
    {
        // Implementation
    }
}
```

## Architecture Patterns

### 1. **TagHelper Pattern**

**Base Class Design**
```csharp
/// <summary>
/// An abstract base class for <see cref="ITagHelper"/>.
/// </summary>
public abstract class TagHelper : ITagHelper
{
    /// <summary>
    /// When a set of <see cref="ITagHelper"/>s are executed, their <see cref="Init(TagHelperContext)"/>'s
    /// are first invoked in the specified <see cref="Order"/>; then their
    /// <see cref="ProcessAsync(TagHelperContext, TagHelperOutput)"/>'s are invoked in the specified
    /// <see cref="Order"/>. Lower values are executed first.
    /// </summary>
    /// <remarks>Default order is <c>0</c>.</remarks>
    public virtual int Order { get; }

    /// <summary>
    /// Initializes the <see cref="ITagHelper"/> with the given <paramref name="context"/>. Additions to
    /// <see cref="TagHelperContext.Items"/> should be done within this method to ensure they're added prior to
    /// executing the children.
    /// </summary>
    /// <param name="context">Contains information associated with the current HTML tag.</param>
    /// <remarks>When more than one <see cref="ITagHelper"/> runs on the same element,
    /// <see cref="M:TagHelperOutput.GetChildContentAsync"/> may be invoked prior to <see cref="ProcessAsync"/>. </remarks>
    public virtual void Init(TagHelperContext context)
    {
    }

    /// <summary>
    /// Synchronously executes the <see cref="TagHelper"/> with the given <paramref name="context"/> and
    /// <paramref name="output"/>.
    /// </summary>
    /// <param name="context">Contains information associated with the current HTML tag.</param>
    /// <param name="output">A stateful HTML element used to generate an HTML tag.</param>
    public virtual void Process(TagHelperContext context, TagHelperOutput output)
    {
    }

    /// <summary>
    /// Asynchronously executes the <see cref="TagHelper"/> with the given <paramref name="context"/> and
    /// <paramref name="output"/>.
    /// </summary>
    /// <param name="context">Contains information associated with the current HTML tag.</param>
    /// <param name="output">A stateful HTML element used to generate an HTML tag.</param>
    /// <returns>A <see cref="Task"/> that on completion updates the <paramref name="output"/>.</returns>
    /// <remarks>By default this calls into <see cref="Process"/>.</remarks>.
    public virtual Task ProcessAsync(TagHelperContext context, TagHelperOutput output)
    {
        Process(context, output);
        return Task.CompletedTask;
    }
}
```

**Attribute-Based Configuration**
```csharp
[HtmlTargetElement("custom-element")]
[RestrictChildren("child-element")]
public class CustomTagHelper : TagHelper
{
    [HtmlAttributeName("custom-attribute")]
    public string CustomProperty { get; set; }

    [HtmlAttributeNotBound]
    public string UnboundProperty { get; set; }
}
```

### 2. **Collection Patterns**

**ReadOnly Collections**
```csharp
public class ReadOnlyTagHelperAttributeList : IReadOnlyList<TagHelperAttribute>
{
    private readonly IList<TagHelperAttribute> _attributes;

    public TagHelperAttribute this[int index] => _attributes[index];

    public int Count => _attributes.Count;

    public IEnumerator<TagHelperAttribute> GetEnumerator() => _attributes.GetEnumerator();
}
```

**Mutable Collections**
```csharp
public class TagHelperAttributeList : List<TagHelperAttribute>
{
    public void SetAttribute(string name, object value)
    {
        // Implementation
    }

    public bool RemoveAll(string name)
    {
        // Implementation
    }
}
```

### 3. **Output Generation Pattern**

**TagHelperOutput Design**
```csharp
public class TagHelperOutput
{
    public string TagName { get; set; }
    public TagMode TagMode { get; set; }
    public TagHelperAttributeList Attributes { get; }
    public TagHelperContent Content { get; }

    public void PreContent.SetContent(string content);
    public void PostContent.SetContent(string content);
}
```

## Testing Standards

### 1. **Test Organization**

**Test Class Structure**
```csharp
public class TagHelperAttributeListTest
{
    [Theory]
    [MemberData(nameof(AddData))]
    public void Add_AppendsAttributes(
        IEnumerable<TagHelperAttribute> initialAttributes,
        TagHelperAttribute attributeToAdd,
        IEnumerable<TagHelperAttribute> expectedAttributes)
    {
        // Arrange
        var attributes = new TagHelperAttributeList(initialAttributes);

        // Act
        attributes.Add(attributeToAdd);

        // Assert
        Assert.Equal(expectedAttributes, attributes, CaseSensitiveTagHelperAttributeComparer.Default);
    }

    public static TheoryData<IEnumerable<TagHelperAttribute>, TagHelperAttribute, IEnumerable<TagHelperAttribute>> AddData
    {
        get
        {
            var A = new TagHelperAttribute("AName", "AName Value");
            var A2 = new TagHelperAttribute("aname", "AName Second Value");
            var B = new TagHelperAttribute("BName", "BName Value");

            return new TheoryData<
                IEnumerable<TagHelperAttribute>, // initialAttributes
                TagHelperAttribute, // attributeToAdd
                IEnumerable<TagHelperAttribute>> // expectedAttributes
                {
                    { Enumerable.Empty<TagHelperAttribute>(), A, new[] { A } },
                    { new[] { A }, B, new[] { A, B } },
                    { new[] { A }, A2, new[] { A, A2 } },
                };
        }
    }
}
```

### 2. **Test Data Patterns**

**Theory Data**
```csharp
public static TheoryData<string, string, bool> StringIndexerData
{
    get
    {
        return new TheoryData<string, string, bool>
        {
            { "test", "value", true },
            { "other", "value", false }
        };
    }
}
```

**Test Fixtures**
```csharp
public class TagHelperTestBase
{
    protected TagHelperContext CreateTagHelperContext()
    {
        return new TagHelperContext(
            tagName: "div",
            allAttributes: new TagHelperAttributeList(),
            items: new Dictionary<object, object>(),
            uniqueId: "test");
    }

    protected TagHelperOutput CreateTagHelperOutput()
    {
        return new TagHelperOutput(
            tagName: "div",
            attributes: new TagHelperAttributeList(),
            getChildContentAsync: async useCachedResult =>
            {
                var tagHelperContent = new DefaultTagHelperContent();
                tagHelperContent.SetContent("test");
                return tagHelperContent;
            });
    }
}
```

## Performance Guidelines

### 1. **Memory Management**

**String Handling**
```csharp
// Use StringBuilder for string concatenation
private static string BuildAttributeString(string name, string value)
{
    var builder = new StringBuilder();
    builder.Append(name);
    builder.Append("=\"");
    builder.Append(value);
    builder.Append("\"");
    return builder.ToString();
}

// Use string interning for repeated strings
private static readonly string DefaultTagName = "div";
```

**Collection Operations**
```csharp
// Use appropriate collection types
private readonly List<TagHelperAttribute> _attributes = new List<TagHelperAttribute>();
private readonly Dictionary<string, TagHelperAttribute> _attributeMap = new Dictionary<string, TagHelperAttribute>(StringComparer.OrdinalIgnoreCase);
```

### 2. **HTML Encoding**

**Unsafe Code for Performance**
```csharp
[MethodImpl(MethodImplOptions.AggressiveInlining)]
public static unsafe void HtmlEncode(string value, TextWriter writer)
{
    fixed (char* chars = value)
    {
        // Fast encoding implementation
    }
}
```

**Encoder Usage**
```csharp
public class HtmlEncoder : IHtmlEncoder
{
    public string HtmlEncode(string value)
    {
        if (string.IsNullOrEmpty(value))
            return value;

        return WebUtility.HtmlEncode(value);
    }
}
```

### 3. **Async Patterns**

**Async-First Design**
```csharp
public virtual Task ProcessAsync(TagHelperContext context, TagHelperOutput output)
{
    // Default implementation calls sync method
    Process(context, output);
    return Task.CompletedTask;
}

public virtual void Process(TagHelperContext context, TagHelperOutput output)
{
    // Override this for sync processing
}
```

## Security Guidelines

### 1. **Input Validation**

**Attribute Validation**
```csharp
public void SetAttribute(string name, object value)
{
    if (string.IsNullOrEmpty(name))
        throw new ArgumentException("Attribute name cannot be null or empty", nameof(name));

    if (value == null)
        throw new ArgumentNullException(nameof(value));

    // Implementation
}
```

**Content Sanitization**
```csharp
public void SetContent(string content)
{
    if (content == null)
        throw new ArgumentNullException(nameof(content));

    // HTML encode content to prevent XSS
    _content = _htmlEncoder.HtmlEncode(content);
}
```

### 2. **Output Encoding**

**Automatic Encoding**
```csharp
public class TagHelperContent : IHtmlContent
{
    private string _content;
    private readonly IHtmlEncoder _htmlEncoder;

    public void SetContent(string content)
    {
        _content = _htmlEncoder.HtmlEncode(content);
    }

    public void WriteTo(TextWriter writer, HtmlEncoder encoder)
    {
        writer.Write(_content);
    }
}
```

## Build and Configuration Standards

### 1. **Project Structure**

**Directory Organization**
```
src/
├── Razor/
│   ├── src/
│   │   ├── Microsoft.AspNetCore.Razor.csproj
│   │   ├── TagHelpers/
│   │   └── PublicAPI.Shipped.txt
│   └── test/
│       ├── Microsoft.AspNetCore.Razor.Test.csproj
│       └── TagHelpers/
└── Razor.Runtime/
    ├── src/
    │   ├── Microsoft.AspNetCore.Razor.Runtime.csproj
    │   ├── Hosting/
    │   └── Runtime/
    └── test/
        ├── Microsoft.AspNetCore.Razor.Runtime.Test.csproj
        └── Runtime/
```

**Project File Standards**
```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <Summary>Razor is a markup syntax for adding server-side logic to web pages. This package contains runtime components for rendering Razor pages and implementing tag helpers.</Summary>
    <Description>$(Summary)

Commonly used types:
Microsoft.AspNetCore.Razor.TagHelpers.HtmlAttributeNameAttribute
Microsoft.AspNetCore.Razor.TagHelpers.HtmlTargetElementAttribute
Microsoft.AspNetCore.Razor.TagHelpers.ITagHelper</Description>
    <TargetFramework>$(DefaultNetCoreTargetFramework)</TargetFramework>
    <IsAspNetCoreApp>true</IsAspNetCoreApp>
    <GenerateDocumentationFile>true</GenerateDocumentationFile>
    <PackageTags>$(PackageTags);taghelper;taghelpers</PackageTags>
    <IsPackable>false</IsPackable>

    <!-- Required to implement an HtmlEncoder -->
    <AllowUnsafeBlocks>true</AllowUnsafeBlocks>
  </PropertyGroup>

  <ItemGroup>
    <Reference Include="Microsoft.AspNetCore.Html.Abstractions" />
  </ItemGroup>

  <ItemGroup>
    <InternalsVisibleTo Include="Microsoft.AspNetCore.Razor.Test" />
    <InternalsVisibleTo Include="Microsoft.AspNetCore.Razor.Runtime.Test" />
  </ItemGroup>
</Project>
```

### 2. **API Baselines**

**Public API Management**
- Use `PublicAPI.Shipped.txt` for shipped APIs
- Use `PublicAPI.Unshipped.txt` for new APIs
- Follow the API review process for breaking changes
- Maintain backward compatibility

### 3. **Code Analysis**

**Static Analysis**
- Enable all relevant Roslyn analyzers
- Use nullable reference types where appropriate
- Follow CA (Code Analysis) rules
- Use `[SuppressMessage]` attributes for justified suppressions

## Documentation Standards

### 1. **API Documentation**

**XML Documentation Requirements**
- All public APIs must have XML documentation
- Use `<summary>`, `<remarks>`, `<example>` tags appropriately
- Reference other types using `<see cref="..."/>`
- Document parameters using `<param name="...">`
- Document return values using `<returns>`

### 2. **Code Comments**

**Inline Comments**
```csharp
// Use comments to explain complex logic
// TODO: Add performance optimization
// FIXME: Handle edge case properly
// NOTE: This is a workaround for issue #1234
```

**Block Comments**
```csharp
/*
 * Multi-line comments for complex explanations
 * or temporary code blocks
 */
```

## Error Handling

### 1. **Exception Patterns**

**Custom Exceptions**
```csharp
public class TagHelperException : Exception
{
    public TagHelperException(string message) : base(message) { }
    public TagHelperException(string message, Exception innerException) : base(message, innerException) { }
}
```

**Error Messages**
```csharp
// Use clear, descriptive error messages
throw new ArgumentException("Tag name cannot be null or empty.", nameof(tagName));

// Include relevant context
throw new InvalidOperationException($"Unable to process tag helper '{helper.GetType().Name}' in context '{context.TagName}'.");
```

### 2. **Logging**

**EventSource Pattern**
```csharp
[EventSource(Name = "Microsoft-AspNetCore-Authentication")]
public class AuthenticationEventSource : EventSource
{
    public static readonly AuthenticationEventSource Log = new AuthenticationEventSource();

    [Event(eventId: 1, Level = EventLevel.Informational)]
    private void AuthenticationMiddlewareStart(string traceIdentifier, string path) => WriteEvent(1, traceIdentifier, path);
}
```

## Versioning and Compatibility

### 1. **Semantic Versioning**

**Version Components**
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes (backward compatible)

### 2. **Breaking Changes**

**Process for Breaking Changes**
1. API review required
2. Document migration path
3. Provide deprecation warnings
4. Update version appropriately

### 3. **Backward Compatibility**

**Compatibility Requirements**
- Maintain API compatibility within major versions
- Use `[Obsolete]` attributes for deprecated APIs
- Provide migration guidance for breaking changes
- Test against previous versions

## Code Review Checklist

### 1. **Functional Requirements**
- [ ] Code meets functional requirements
- [ ] Edge cases are handled appropriately
- [ ] Error conditions are properly managed
- [ ] Performance requirements are met

### 2. **Code Quality**
- [ ] Code follows established patterns
- [ ] Naming conventions are consistent
- [ ] Documentation is complete and accurate
- [ ] Code is readable and maintainable

### 3. **Testing**
- [ ] Unit tests cover all scenarios
- [ ] Integration tests verify end-to-end functionality
- [ ] Performance tests validate requirements
- [ ] Tests follow naming conventions

### 4. **Security**
- [ ] Input validation is implemented
- [ ] Output encoding is used appropriately
- [ ] No sensitive information in logs
- [ ] Dependencies are secure

### 5. **Performance**
- [ ] No obvious performance bottlenecks
- [ ] Memory usage is reasonable
- [ ] Async patterns are used appropriately
- [ ] Caching is implemented where beneficial

This style guide ensures consistency, quality, and maintainability across the ASP.NET Core Razor project codebase.
