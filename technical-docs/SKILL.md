---
name: technical-docs
description: Create technical documentation in markdown including READMEs, API docs, changelogs, and technical specifications. Uses proper syntax, code blocks with language tags, and standard conventions. Claude should use this skill when creating or maintaining technical documentation in markdown format.
---

## When to use this skill

Use this skill for:
- README files for repositories
- API documentation
- Technical specifications
- Changelogs (Keep a Changelog format)
- Architecture documentation
- Configuration guides

## Key markdown conventions

### Code blocks with language tags

Always specify language for syntax highlighting:

````markdown
```python
def example():
    return "code"
```
````

### Headers for hierarchy

```markdown
# H1 - Main title (one per document)
## H2 - Major sections
### H3 - Subsections
```

### Tables

```markdown
| Column 1 | Column 2 |
|----------|----------|
| Data     | Data     |
```

## Document templates

### README structure

```markdown
# Project Name

Brief description (1-2 sentences).

## Installation

```bash
pip install package
```

## Usage

```python
from package import Module
result = Module.process()
```

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| param1    | "value" | What it does |

## API Reference

### function_name(param1, param2)

Description.

**Parameters:**
- `param1` (type): Description

**Returns:**
- type: Description

**Example:**
```python
result = function_name("value", 42)
```
```

### Changelog format

```markdown
# Changelog

## [Unreleased]

### Added
- New feature

### Changed
- Modified feature

### Fixed
- Bug fix

## [1.0.0] - 2025-01-15

### Added
- Initial release
```

## Quality checklist

- Valid markdown syntax
- Language tags on all code blocks
- Logical header hierarchy (no skipped levels)
- Working, runnable code examples
- Consistent formatting throughout
- Scannable structure
- One H1 per document

## Best practices

1. One H1 as document title only
2. Don't skip header levels (H2→H4)
3. Use tables for structured data
4. Relative links for internal docs
5. Blank lines around code blocks
6. Descriptive link text (not "click here")

## Keywords

technical documentation, markdown docs, README, API documentation, changelog, technical spec, code documentation, developer docs

