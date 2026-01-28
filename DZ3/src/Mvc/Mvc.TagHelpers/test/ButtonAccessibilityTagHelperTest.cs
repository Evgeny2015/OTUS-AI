// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using Microsoft.AspNetCore.Html;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.AspNetCore.Mvc.ViewFeatures;
using Microsoft.AspNetCore.Razor.TagHelpers;
using Microsoft.AspNetCore.Razor.TagHelpers.Testing;
using Microsoft.AspNetCore.InternalTesting;
using Moq;

namespace Microsoft.AspNetCore.Mvc.TagHelpers;

public class ButtonAccessibilityTagHelperTest
{
    [Fact]
    public void Process_AddsTypeButton_WhenTypeNotSpecified()
    {
        // Arrange
        var expectedAttributes = new TagHelperAttributeList
        {
            { "type", "button" },
            { "id", "test-button" },
            { "class", "btn" },
        };

        var context = new TagHelperContext(
            tagName: "button",
            allAttributes: new TagHelperAttributeList(
                Enumerable.Empty<TagHelperAttribute>()),
            items: new Dictionary<object, object>(),
            uniqueId: "test");

        var output = new TagHelperOutput(
            "button",
            new TagHelperAttributeList
            {
                { "id", "test-button" },
                { "class", "btn" },
            },
            getChildContentAsync: (useCachedResult, encoder) => Task.FromResult<TagHelperContent>(result: null))
        {
            TagMode = TagMode.StartTagAndEndTag,
        };

        var htmlGenerator = new TestableHtmlGenerator(new EmptyModelMetadataProvider());
        var tagHelper = new ButtonAccessibilityTagHelper();

        // Act
        tagHelper.Process(context, output);

        // Assert
        Assert.Equal(expectedAttributes, output.Attributes);
        Assert.Equal("button", output.TagName);
    }

    [Fact]
    public void Process_DoesNotOverrideExistingType()
    {
        // Arrange
        var expectedAttributes = new TagHelperAttributeList
        {
            { "type", "submit" },
            { "id", "test-button" },
        };

        var context = new TagHelperContext(
            tagName: "button",
            allAttributes: new TagHelperAttributeList(
                Enumerable.Empty<TagHelperAttribute>()),
            items: new Dictionary<object, object>(),
            uniqueId: "test");

        var output = new TagHelperOutput(
            "button",
            new TagHelperAttributeList
            {
                { "type", "submit" },
                { "id", "test-button" },
            },
            getChildContentAsync: (useCachedResult, encoder) => Task.FromResult<TagHelperContent>(result: null))
        {
            TagMode = TagMode.StartTagAndEndTag,
        };

        var tagHelper = new ButtonAccessibilityTagHelper();

        // Act
        tagHelper.Process(context, output);

        // Assert
        Assert.Equal(expectedAttributes, output.Attributes);
        Assert.Equal("button", output.TagName);
    }

    [Fact]
    public void Process_AddsAriaLabel_WhenNotPresent()
    {
        // Arrange
        var expectedAttributes = new TagHelperAttributeList
        {
            { "type", "button" },
            { "aria-label", "Click me" },
            { "id", "test-button" },
        };

        var context = new TagHelperContext(
            tagName: "button",
            allAttributes: new TagHelperAttributeList(
                Enumerable.Empty<TagHelperAttribute>()),
            items: new Dictionary<object, object>(),
            uniqueId: "test");

        var output = new TagHelperOutput(
            "button",
            new TagHelperAttributeList
            {
                { "id", "test-button" },
            },
            getChildContentAsync: (useCachedResult, encoder) => Task.FromResult<TagHelperContent>(result: null))
        {
            TagMode = TagMode.StartTagAndEndTag,
        };

        output.Content.SetContent("Click me");

        var tagHelper = new ButtonAccessibilityTagHelper();

        // Act
        tagHelper.Process(context, output);

        // Assert
        Assert.Equal(expectedAttributes, output.Attributes);
        Assert.Equal("button", output.TagName);
    }

    [Fact]
    public void Process_DoesNotOverrideExistingAriaLabel()
    {
        // Arrange
        var expectedAttributes = new TagHelperAttributeList
        {
            { "type", "button" },
            { "aria-label", "Custom label" },
            { "id", "test-button" },
        };

        var context = new TagHelperContext(
            tagName: "button",
            allAttributes: new TagHelperAttributeList(
                Enumerable.Empty<TagHelperAttribute>()),
            items: new Dictionary<object, object>(),
            uniqueId: "test");

        var output = new TagHelperOutput(
            "button",
            new TagHelperAttributeList
            {
                { "aria-label", "Custom label" },
                { "id", "test-button" },
            },
            getChildContentAsync: (useCachedResult, encoder) => Task.FromResult<TagHelperContent>(result: null))
        {
            TagMode = TagMode.StartTagAndEndTag,
        };

        output.Content.SetContent("Click me");

        var tagHelper = new ButtonAccessibilityTagHelper();

        // Act
        tagHelper.Process(context, output);

        // Assert
        Assert.Equal(expectedAttributes, output.Attributes);
        Assert.Equal("button", output.TagName);
    }

    [Fact]
    public void Process_UsesButtonContentForAriaLabel()
    {
        // Arrange
        var expectedAttributes = new TagHelperAttributeList
        {
            { "type", "button" },
            { "aria-label", "Save Changes" },
            { "class", "btn-primary" },
        };

        var context = new TagHelperContext(
            tagName: "button",
            allAttributes: new TagHelperAttributeList(
                Enumerable.Empty<TagHelperAttribute>()),
            items: new Dictionary<object, object>(),
            uniqueId: "test");

        var output = new TagHelperOutput(
            "button",
            new TagHelperAttributeList
            {
                { "class", "btn-primary" },
            },
            getChildContentAsync: (useCachedResult, encoder) => Task.FromResult<TagHelperContent>(result: null))
        {
            TagMode = TagMode.StartTagAndEndTag,
        };

        output.Content.SetContent("Save Changes");

        var tagHelper = new ButtonAccessibilityTagHelper();

        // Act
        tagHelper.Process(context, output);

        // Assert
        Assert.Equal(expectedAttributes, output.Attributes);
        Assert.Equal("button", output.TagName);
    }

    [Fact]
    public void Process_UsesValueAttributeForAriaLabel()
    {
        // Arrange
        var expectedAttributes = new TagHelperAttributeList
        {
            { "type", "button" },
            { "aria-label", "Submit Form" },
            { "value", "Submit Form" },
        };

        var context = new TagHelperContext(
            tagName: "button",
            allAttributes: new TagHelperAttributeList(
                Enumerable.Empty<TagHelperAttribute>()),
            items: new Dictionary<object, object>(),
            uniqueId: "test");

        var output = new TagHelperOutput(
            "button",
            new TagHelperAttributeList
            {
                { "value", "Submit Form" },
            },
            getChildContentAsync: (useCachedResult, encoder) => Task.FromResult<TagHelperContent>(result: null))
        {
            TagMode = TagMode.StartTagAndEndTag,
        };

        var tagHelper = new ButtonAccessibilityTagHelper();

        // Act
        tagHelper.Process(context, output);

        // Assert
        Assert.Equal(expectedAttributes, output.Attributes);
        Assert.Equal("button", output.TagName);
    }

    [Fact]
    public void Process_UsesTitleAttributeForAriaLabel()
    {
        // Arrange
        var expectedAttributes = new TagHelperAttributeList
        {
            { "type", "button" },
            { "aria-label", "Click to save" },
            { "title", "Click to save" },
        };

        var context = new TagHelperContext(
            tagName: "button",
            allAttributes: new TagHelperAttributeList(
                Enumerable.Empty<TagHelperAttribute>()),
            items: new Dictionary<object, object>(),
            uniqueId: "test");

        var output = new TagHelperOutput(
            "button",
            new TagHelperAttributeList
            {
                { "title", "Click to save" },
            },
            getChildContentAsync: (useCachedResult, encoder) => Task.FromResult<TagHelperContent>(result: null))
        {
            TagMode = TagMode.StartTagAndEndTag,
        };

        var tagHelper = new ButtonAccessibilityTagHelper();

        // Act
        tagHelper.Process(context, output);

        // Assert
        Assert.Equal(expectedAttributes, output.Attributes);
        Assert.Equal("button", output.TagName);
    }

    [Fact]
    public void Process_PriorityIsCorrect()
    {
        // Arrange
        var tagHelper = new ButtonAccessibilityTagHelper();

        // Act & Assert
        Assert.Equal(-1000, tagHelper.Order);
    }

    [Fact]
    public void Process_HandlesEmptyButtonContent()
    {
        // Arrange
        var expectedAttributes = new TagHelperAttributeList
        {
            { "type", "button" },
            { "class", "icon-btn" },
        };

        var context = new TagHelperContext(
            tagName: "button",
            allAttributes: new TagHelperAttributeList(
                Enumerable.Empty<TagHelperAttribute>()),
            items: new Dictionary<object, object>(),
            uniqueId: "test");

        var output = new TagHelperOutput(
            "button",
            new TagHelperAttributeList
            {
                { "class", "icon-btn" },
            },
            getChildContentAsync: (useCachedResult, encoder) => Task.FromResult<TagHelperContent>(result: null))
        {
            TagMode = TagMode.StartTagAndEndTag,
        };

        // Empty content
        output.Content.SetContent("");

        var tagHelper = new ButtonAccessibilityTagHelper();

        // Act
        tagHelper.Process(context, output);

        // Assert
        Assert.Equal(expectedAttributes, output.Attributes);
        Assert.Equal("button", output.TagName);
    }

    [Fact]
    public void Process_HandlesWhitespaceOnlyContent()
    {
        // Arrange
        var expectedAttributes = new TagHelperAttributeList
        {
            { "type", "button" },
            { "aria-label", "Save" },
            { "class", "btn" },
        };

        var context = new TagHelperContext(
            tagName: "button",
            allAttributes: new TagHelperAttributeList(
                Enumerable.Empty<TagHelperAttribute>()),
            items: new Dictionary<object, object>(),
            uniqueId: "test");

        var output = new TagHelperOutput(
            "button",
            new TagHelperAttributeList
            {
                { "class", "btn" },
            },
            getChildContentAsync: (useCachedResult, encoder) => Task.FromResult<TagHelperContent>(result: null))
        {
            TagMode = TagMode.StartTagAndEndTag,
        };

        // Whitespace content that should be trimmed
        output.Content.SetContent("  Save  ");

        var tagHelper = new ButtonAccessibilityTagHelper();

        // Act
        tagHelper.Process(context, output);

        // Assert
        Assert.Equal(expectedAttributes, output.Attributes);
        Assert.Equal("button", output.TagName);
    }

    [Fact]
    public void Process_PrefersContentOverValueAttribute()
    {
        // Arrange
        var expectedAttributes = new TagHelperAttributeList
        {
            { "type", "button" },
            { "aria-label", "Button Text" },
            { "value", "Value Text" },
        };

        var context = new TagHelperContext(
            tagName: "button",
            allAttributes: new TagHelperAttributeList(
                Enumerable.Empty<TagHelperAttribute>()),
            items: new Dictionary<object, object>(),
            uniqueId: "test");

        var output = new TagHelperOutput(
            "button",
            new TagHelperAttributeList
            {
                { "value", "Value Text" },
            },
            getChildContentAsync: (useCachedResult, encoder) => Task.FromResult<TagHelperContent>(result: null))
        {
            TagMode = TagMode.StartTagAndEndTag,
        };

        output.Content.SetContent("Button Text");

        var tagHelper = new ButtonAccessibilityTagHelper();

        // Act
        tagHelper.Process(context, output);

        // Assert
        Assert.Equal(expectedAttributes, output.Attributes);
        Assert.Equal("button", output.TagName);
    }

    [Fact]
    public void Process_PrefersValueOverTitleAttribute()
    {
        // Arrange
        var expectedAttributes = new TagHelperAttributeList
        {
            { "type", "button" },
            { "aria-label", "Value Text" },
            { "title", "Title Text" },
        };

        var context = new TagHelperContext(
            tagName: "button",
            allAttributes: new TagHelperAttributeList(
                Enumerable.Empty<TagHelperAttribute>()),
            items: new Dictionary<object, object>(),
            uniqueId: "test");

        var output = new TagHelperOutput(
            "button",
            new TagHelperAttributeList
            {
                { "title", "Title Text" },
            },
            getChildContentAsync: (useCachedResult, encoder) => Task.FromResult<TagHelperContent>(result: null))
        {
            TagMode = TagMode.StartTagAndEndTag,
        };

        output.Attributes.SetAttribute("value", "Value Text");

        var tagHelper = new ButtonAccessibilityTagHelper();

        // Act
        tagHelper.Process(context, output);

        // Assert
        Assert.Equal(expectedAttributes, output.Attributes);
        Assert.Equal("button", output.TagName);
    }

    [Fact]
    public void Process_DoesNotAddAriaLabel_WhenNoSuitableTextFound()
    {
        // Arrange
        var expectedAttributes = new TagHelperAttributeList
        {
            { "type", "button" },
            { "id", "icon-button" },
        };

        var context = new TagHelperContext(
            tagName: "button",
            allAttributes: new TagHelperAttributeList(
                Enumerable.Empty<TagHelperAttribute>()),
            items: new Dictionary<object, object>(),
            uniqueId: "test");

        var output = new TagHelperOutput(
            "button",
            new TagHelperAttributeList
            {
                { "id", "icon-button" },
            },
            getChildContentAsync: (useCachedResult, encoder) => Task.FromResult<TagHelperContent>(result: null))
        {
            TagMode = TagMode.StartTagAndEndTag,
        };

        // No content, no value, no title
        output.Content.SetContent("");

        var tagHelper = new ButtonAccessibilityTagHelper();

        // Act
        tagHelper.Process(context, output);

        // Assert
        Assert.Equal(expectedAttributes, output.Attributes);
        Assert.Equal("button", output.TagName);
    }

    [Fact]
    public void Process_HandlesSelfClosingButton()
    {
        // Arrange
        var expectedAttributes = new TagHelperAttributeList
        {
            { "type", "button" },
            { "value", "Submit" },
        };

        var context = new TagHelperContext(
            tagName: "button",
            allAttributes: new TagHelperAttributeList(
                Enumerable.Empty<TagHelperAttribute>()),
            items: new Dictionary<object, object>(),
            uniqueId: "test");

        var output = new TagHelperOutput(
            "button",
            new TagHelperAttributeList
            {
                { "value", "Submit" },
            },
            getChildContentAsync: (useCachedResult, encoder) => Task.FromResult<TagHelperContent>(result: null))
        {
            TagMode = TagMode.SelfClosing,
        };

        var tagHelper = new ButtonAccessibilityTagHelper();

        // Act
        tagHelper.Process(context, output);

        // Assert
        Assert.Equal(expectedAttributes, output.Attributes);
        Assert.Equal("button", output.TagName);
    }

    [Fact]
    public void Process_AddsBothTypeAndAriaLabel()
    {
        // Arrange
        var expectedAttributes = new TagHelperAttributeList
        {
            { "type", "button" },
            { "aria-label", "Submit" },
            { "class", "btn-submit" },
        };

        var context = new TagHelperContext(
            tagName: "button",
            allAttributes: new TagHelperAttributeList(
                Enumerable.Empty<TagHelperAttribute>()),
            items: new Dictionary<object, object>(),
            uniqueId: "test");

        var output = new TagHelperOutput(
            "button",
            new TagHelperAttributeList
            {
                { "class", "btn-submit" },
            },
            getChildContentAsync: (useCachedResult, encoder) => Task.FromResult<TagHelperContent>(result: null))
        {
            TagMode = TagMode.StartTagAndEndTag,
        };

        output.Content.SetContent("Submit");

        var tagHelper = new ButtonAccessibilityTagHelper();

        // Act
        tagHelper.Process(context, output);

        // Assert
        Assert.Equal(expectedAttributes, output.Attributes);
        Assert.Equal("button", output.TagName);
    }

    [Fact]
    public void Process_HandlesNullContextAndOutput()
    {
        // Arrange
        var tagHelper = new ButtonAccessibilityTagHelper();

        // Act & Assert
        Assert.Throws<ArgumentNullException>(() => tagHelper.Process(null, null));
    }

    [Fact]
    public void Process_HandlesNullContext()
    {
        // Arrange
        var tagHelper = new ButtonAccessibilityTagHelper();
        var output = new TagHelperOutput(
            "button",
            new TagHelperAttributeList(),
            getChildContentAsync: (useCachedResult, encoder) => Task.FromResult<TagHelperContent>(result: null));

        // Act & Assert
        Assert.Throws<ArgumentNullException>(() => tagHelper.Process(null, output));
    }

    [Fact]
    public void Process_HandlesNullOutput()
    {
        // Arrange
        var tagHelper = new ButtonAccessibilityTagHelper();
        var context = new TagHelperContext(
            tagName: "button",
            allAttributes: new TagHelperAttributeList(
                Enumerable.Empty<TagHelperAttribute>()),
            items: new Dictionary<object, object>(),
            uniqueId: "test");

        // Act & Assert
        Assert.Throws<ArgumentNullException>(() => tagHelper.Process(context, null));
    }
}
