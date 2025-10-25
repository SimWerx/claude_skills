# Skill Format Specification

Quick reference for valid SKILL.md structure.

## File Structure

Every skill needs one required file:
```
skill-name/
└── SKILL.md
```

Optional additions:
```
skill-name/
├── SKILL.md              (required)
├── references/           (loaded on-demand)
├── scripts/              (executable code)
└── assets/               (output resources)
```

## SKILL.md Format

Two parts: YAML frontmatter + Markdown body.

### Required Frontmatter

```yaml
---
name: skill-name
description: What this skill does and when to use it. Be specific about triggers.
---
```

**Name rules**:
- Lowercase letters, numbers, hyphens only
- Must match directory name
- Examples: `research-synthesis`, `data-interrogation`, `executive-memo`

**Description rules**:
- Complete sentence describing purpose AND triggers
- Include keywords for discoverability
- Third-person: "Claude should use this skill when..."
- Examples:
  - Good: "Transform research materials into executive summaries with citations. Claude should use this skill when synthesizing multiple sources or analyzing research articles."
  - Bad: "Helps with research"

### Optional Frontmatter

```yaml
---
name: skill-name
description: Complete description
license: Apache 2.0
allowed-tools: [bash, python]
metadata:
  version: "1.0"
  author: "Team Name"
---
```

**License**: Short identifier or filename  
**Allowed-tools**: Pre-approved tools (Claude Code only)  
**Metadata**: Custom key-value pairs for client use

### Markdown Body

No restrictions. Write clear instructions for the AI.

Best practices:
- Keep main file 30-50 lines (overview and navigation)
- Move details to `references/` files
- Use "How to use this skill" workflow sections
- Include "When to use this skill" triggers
- Add "Keywords" section for discoverability

## Progressive Disclosure Pattern

**Efficient token usage**:
1. Metadata always loaded (name + description)
2. SKILL.md loaded when skill triggers
3. References loaded only when AI reads them

Example structure:
```
skill-name/
├── SKILL.md                    # 40 lines: overview, workflow, links
└── references/
    ├── formats.md              # Detailed templates
    ├── examples.md             # Usage examples
    └── advanced.md             # Complex scenarios
```

In SKILL.md, reference files like:
```markdown
See [references/formats.md](references/formats.md) for detailed templates.
```

## Validation

Name must:
- Match directory name
- Use lowercase + hyphens only
- Not contain spaces or special characters

Description must:
- Be non-empty
- Describe what AND when
- Use third-person voice

## Quick Examples

**Minimal skill**:
```yaml
---
name: hello-world
description: Demonstrates basic skill structure. Use when testing skill loading.
---

# Hello World

This is a minimal skill demonstrating the required format.
```

**With progressive disclosure**:
```yaml
---
name: data-analysis
description: Analyze CSV data with executive insights. Use when working with spreadsheets or tabular data.
---

## When to use
Use for CSV files, sales data, metrics analysis.

## How to use
1. Inspect data structure
2. Load format from references/formats.md
3. Apply analysis
4. Generate output

## Templates
See [references/formats.md](references/formats.md)
```

That's it. Keep it simple.

