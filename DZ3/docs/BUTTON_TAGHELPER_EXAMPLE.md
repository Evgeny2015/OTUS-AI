# ButtonAccessibilityTagHelper Example

This document demonstrates how to use the `ButtonAccessibilityTagHelper` to improve button accessibility in ASP.NET Core applications.

## Overview

The `ButtonAccessibilityTagHelper` automatically adds accessibility attributes to `<button>` elements:

- Adds `type="button"` if not specified (prevents accidental form submission)
- Adds `aria-label` attribute if not present, using button content or other attributes

## Basic Usage

### Before (without TagHelper)
```html
<button>Click me</button>
```

### After (with TagHelper)
```html
<button type="button" aria-label="Click me">Click me</button>
```

## Examples

### 1. Button with Text Content
```html
<button class="btn-primary">Save Changes</button>
```

**Generated output:**
```html
<button type="button" aria-label="Save Changes" class="btn-primary">Save Changes</button>
```

### 2. Button with Value Attribute
```html
<button value="Submit Form">Submit</button>
```

**Generated output:**
```html
<button type="button" aria-label="Submit Form" value="Submit Form">Submit</button>
```

### 3. Button with Title Attribute
```html
<button title="Click to save your changes">Save</button>
```

**Generated output:**
```html
<button type="button" aria-label="Click to save your changes" title="Click to save your changes">Save</button>
```

### 4. Button with Existing Attributes
```html
<button type="submit" aria-label="Custom Label">Submit</button>
```

**Generated output (preserves existing attributes):**
```html
<button type="submit" aria-label="Custom Label">Submit</button>
```

### 5. Icon Button (No Text Content)
```html
<button class="icon-btn">
    <i class="fa fa-save"></i>
</button>
```

**Generated output (no aria-label added when no suitable text found):**
```html
<button type="button" class="icon-btn">
    <i class="fa fa-save"></i>
</button>
```

## Priority and Order

The `ButtonAccessibilityTagHelper` has a high priority (`Order = -1000`) to ensure it runs before other button-related TagHelpers, allowing other TagHelpers to potentially override its behavior if needed.

## Accessibility Benefits

1. **Prevents Accidental Form Submission**: Automatically adds `type="button"` to prevent buttons from submitting forms by default
2. **Screen Reader Support**: Adds `aria-label` for better screen reader accessibility
3. **Consistent Behavior**: Ensures all buttons have consistent accessibility attributes

## Integration

The TagHelper is automatically registered when using ASP.NET Core MVC. No additional configuration is required.

## Testing

The TagHelper includes comprehensive unit tests covering:
- Adding `type="button"` when not specified
- Adding `aria-label` from button content
- Using `value` attribute for `aria-label`
- Using `title` attribute for `aria-label`
- Preserving existing attributes
- Handling edge cases (empty content, self-closing buttons, etc.)
