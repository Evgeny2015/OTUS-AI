// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using Microsoft.AspNetCore.Html;
using Microsoft.AspNetCore.Mvc.ViewFeatures;
using Microsoft.AspNetCore.Razor.TagHelpers;

namespace Microsoft.AspNetCore.Mvc.TagHelpers;

/// <summary>
/// <see cref="ITagHelper"/> implementation targeting <button> elements that adds accessibility attributes.
/// </summary>
/// <remarks>
/// This TagHelper adds aria-label and type attributes to button elements for improved accessibility.
/// </remarks>
[HtmlTargetElement("button")]
public class ButtonAccessibilityTagHelper : TagHelper
{
    /// <summary>
    /// Creates a new <see cref="ButtonAccessibilityTagHelper"/>.
    /// </summary>
    public ButtonAccessibilityTagHelper()
    {
        // Default constructor
    }

    /// <inheritdoc />
    /// <remarks>
    /// This TagHelper has a high priority to ensure it runs before other button-related TagHelpers.
    /// </remarks>
    public override int Order => -1000;

    /// <summary>
    /// Gets the <see cref="ViewContext"/> of the executing view.
    /// </summary>
    [HtmlAttributeNotBound]
    [ViewContext]
    public ViewContext ViewContext { get; set; }

    /// <summary>
    /// The text content of the button element.
    /// </summary>
    /// <remarks>
    /// Used to generate aria-label when not explicitly provided.
    /// </remarks>
    public string ButtonText { get; set; }

    /// <inheritdoc />
    /// <remarks>
    /// Adds aria-label attribute if not present and type="button" if not specified.
    /// </remarks>
    public override void Process(TagHelperContext context, TagHelperOutput output)
    {
        ArgumentNullException.ThrowIfNull(context);
        ArgumentNullException.ThrowIfNull(output);

        // Add type="button" if not specified to prevent form submission by default
        if (!output.Attributes.ContainsName("type"))
        {
            output.Attributes.SetAttribute("type", "button");
        }

        // Add aria-label if not present
        if (!output.Attributes.ContainsName("aria-label"))
        {
            var ariaLabel = GenerateAriaLabel(output);
            if (!string.IsNullOrEmpty(ariaLabel))
            {
                output.Attributes.SetAttribute("aria-label", ariaLabel);
            }
        }
    }

    /// <summary>
    /// Generates an aria-label for the button based on its content or context.
    /// </summary>
    /// <param name="output">The <see cref="TagHelperOutput"/> containing the button element.</param>
    /// <returns>A generated aria-label string, or null if no suitable label can be generated.</returns>
    protected virtual string GenerateAriaLabel(TagHelperOutput output)
    {
        // Try to get text content from the button
        var buttonText = GetButtonText(output);
        if (!string.IsNullOrEmpty(buttonText))
        {
            return buttonText.Trim();
        }

        // Try to get value attribute for input[type="button"] elements
        if (output.Attributes.TryGetAttribute("value", out var valueAttribute))
        {
            if (valueAttribute.Value is string valueText && !string.IsNullOrEmpty(valueText))
            {
                return valueText.Trim();
            }
        }

        // Try to get title attribute as fallback
        if (output.Attributes.TryGetAttribute("title", out var titleAttribute))
        {
            if (titleAttribute.Value is string titleText && !string.IsNullOrEmpty(titleText))
            {
                return titleText.Trim();
            }
        }

        // If no suitable text found, return null
        return null;
    }

    /// <summary>
    /// Extracts text content from the button element.
    /// </summary>
    /// <param name="output">The <see cref="TagHelperOutput"/> containing the button element.</param>
    /// <returns>The text content of the button, or null if no text content is found.</returns>
    protected virtual string GetButtonText(TagHelperOutput output)
    {
        // For self-closing buttons, check if there's any content
        if (output.TagMode == TagMode.SelfClosing)
        {
            return null;
        }

        // Get the content of the button
        var content = output.Content.GetContent();
        if (!string.IsNullOrEmpty(content))
        {
            return content;
        }

        // If no content, return null
        return null;
    }
}
