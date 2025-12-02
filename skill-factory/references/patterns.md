# Skill Patterns

Templates, writing conventions, and patterns for skill creation.

## Skill Type Patterns

### Pattern 1: Analysis Skills (e.g., data-interrogation)

**Structure**:
- SKILL.md: Overview, triggers, workflow, core principles
- references/formats.md: Analysis report templates, comparative analysis format
- assets/sample_data.csv: 15 lines of realistic tabular data

**Key principles**:
- Executive lens (decision-useful insights)
- Flag data quality issues
- Show methodology for reproducibility

### Pattern 2: Document Creation Skills (e.g., executive-memo)

**Structure**:
- SKILL.md: Document types, workflow, quality checklist
- references/formats.md: Full templates for each document type

**Key principles**:
- Answer-first structure
- Evidence-based claims
- Professional tone for target audience

### Pattern 3: Technical Skills (e.g., technical-docs)

**Structure**:
- SKILL.md: Markdown conventions, document types, quality checklist
- references/templates.md: README, API docs, changelog templates

**Key principles**:
- Proper syntax (language tags, headers)
- Runnable code examples
- Consistent formatting

### Pattern 4: Data Processing Skills (with scripts)

**Structure**:
- SKILL.md: Operations, workflow, script usage
- scripts/processor.py: Class-based processor with type hints
- references/api_reference.md: Detailed processing options
- assets/sample_input.json: 20 lines of test data

**Key principles**:
- Scripts for reliability
- Clear error messages
- Deterministic output

---

## Writing Style Requirements

### Third-Person Descriptions

- Good: "Claude should use this skill when analyzing financial data"
- Bad: "You should use this skill when..."
- Bad: "I can help you analyze data"

### Imperative Instructions

- Good: "Load data from CSV file"
- Bad: "You should load data from the CSV file"
- Bad: "If you need to load data, you might want to..."

### No Marketing Speak

**Forbidden**: cutting-edge, innovative, state-of-the-art, revolutionary, game-changing

**Forbidden**: emojis in SKILL.md or references (OK in scripts output)

**Forbidden**: exclamation points, hype language

**Required**: direct, pragmatic, technical language

### Assume Claude is Smart

- Only include what Claude doesn't already know
- Skip basics: "Functions are reusable blocks of code..."
- Be concise: "Use pdfplumber" not "PDFs are common formats and you'll need a library..."

---

## Handling Time-Sensitive Content

Use collapsible "old patterns" sections:

```markdown
## Current method

Use the v2 API endpoint: `api.example.com/v2/messages`

<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>

The v1 API used: `api.example.com/v1/messages`

This endpoint is no longer supported. Migrate to v2.
</details>
```

**When to use**:
- API version changes
- Library/framework migrations
- Deprecated workflows
- Tool version updates

---

## Emphatic Language for References

When directing Claude to read files, use strong directives:

**Good**:
- "**REQUIRED READING**: Before generating X, you MUST read `references/file.md`"
- "You **MUST** carefully review `Design Requirements.md` before proceeding"

**Bad**:
- "See references/file.md for more details"
- "Review the requirements if needed"

---

## sample_prompt.md Template

```markdown
# Using [Skill Name]

## Quick Start

Hey Claude! I just added the '[skill-name]' skill. Can you show me what it can do?

## With Your Data

I have [describe data/context]. Use the '[skill-name]' skill to analyze it and surprise me!

## Specific Task

Use the '[skill-name]' skill to:
1. [Specific goal]
2. [Another goal]
3. [Final goal]

Make it awesome!

## Examples That Work Great

**Basic usage:**
"Hey Claude, I just uploaded the '[skill-name]' skill. Here's my data—blow my mind with insights!"

**With context:**
"I need to [complex goal]. Use the '[skill-name]' skill and show me your best work."

**Creative mode:**
"Can you use '[skill-name]' to help me [achieve X]? Get creative!"
```

**Tone requirements**:
- Casual and inviting (not formal)
- "Hey Claude!" style openings
- Exciting language: "surprise me", "blow my mind"
- Copy-paste ready (zero customization)
- Encourage creative exploration
- NO formal testing language

---

## Python Script Template

Include scripts when:
- Operations are fragile and require exact execution
- Code would be repeatedly regenerated
- Deterministic output is critical

```python
#!/usr/bin/env python3
"""
Brief description of what this script does.

Usage:
    python helper.py input.csv output.json
"""

import sys
from pathlib import Path
from typing import List, Dict, Any


class SkillHelper:
    """Helper class for [skill-name] operations."""

    def __init__(self, input_path: str):
        """Initialize with input file path."""
        self.input_path = Path(input_path)
        self.data: List[Dict[str, Any]] = []

    def load_data(self) -> None:
        """Load and validate input data."""
        pass

    def process(self) -> Dict[str, Any]:
        """Process data and return results."""
        pass

    def save_output(self, output_path: str) -> None:
        """Save processed results to output file."""
        pass


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python helper.py <input_file> <output_file>")
        sys.exit(1)

    helper = SkillHelper(sys.argv[1])
    helper.load_data()
    results = helper.process()
    helper.save_output(sys.argv[2])
    print(f"Processed {sys.argv[1]} -> {sys.argv[2]}")


if __name__ == "__main__":
    main()
```

---

## Workflow Checklists

For complex workflows (4+ steps), include copy-paste checklists:

```markdown
## How to use this skill

Copy this checklist and track progress:

```
Task Progress:
- [ ] Step 1: Analyze input data
- [ ] Step 2: Validate requirements
- [ ] Step 3: Generate output
- [ ] Step 4: Verify results
```

**Step 1: Analyze input data**
[Detailed instructions]

**Step 2: Validate requirements**
[Detailed instructions]
```

**Benefits**:
- Claude can check off items as it progresses
- Prevents skipping critical validation steps
- Makes progress visible to user

---

## MCP Tool Integration

Use fully qualified tool names: `ServerName:tool_name`

```markdown
## How to use this skill

1. **Query data** - Use `BigQuery:bigquery_schema` to retrieve schemas
2. **Create issues** - Use `GitHub:create_issue` for tracking
3. **Search files** - Use `Filesystem:search_files` to locate documents
```

**Common patterns**:

| Server | Tool | Use Case |
|--------|------|----------|
| `BigQuery` | `bigquery_schema`, `bigquery_query` | Database queries |
| `GitHub` | `create_issue`, `get_file` | Repository operations |
| `Filesystem` | `read_file`, `write_file` | Local file operations |

---

## Test Data Guidelines

**CSV** (10-20 lines max):
```csv
date,product,revenue,units_sold,region
2024-01-15,Widget A,1250.00,25,North
2024-01-16,Widget B,890.50,15,South
2024-01-17,Widget A,2100.00,42,East
```

**JSON**:
```json
{
  "metadata": {
    "version": "1.0",
    "generated": "2024-01-15"
  },
  "items": [
    {"id": 1, "name": "Example", "status": "active"},
    {"id": 2, "name": "Sample", "status": "pending"}
  ]
}
```

