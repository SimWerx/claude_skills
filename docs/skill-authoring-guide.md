# Skill Authoring Guide

Direct instructions for building high-quality Claude skills.

## Core Principle: Be Concise

Context window is shared. Only include what Claude doesn't already know.

**Assume Claude is smart**. Challenge every piece of information:
- "Does Claude need this explained?"
- "Can I assume Claude knows this?"
- "Does this justify its token cost?"

**Good** (50 tokens):
```markdown
## Extract PDF text

Use pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
```

**Bad** (150 tokens):
```markdown
## Extract PDF text

PDF files are a common format containing text and images. 
You'll need a library for extraction. Many options exist, 
but pdfplumber is recommended because it's easy to use...
```

## Progressive Disclosure

**Three-level loading**:
1. Metadata (always): ~100 words
2. SKILL.md (when triggered): <500 lines
3. References (as needed): unlimited

**Structure for efficiency**:
```
skill/
├── SKILL.md              # Lean navigation (30-50 lines)
│   ├── When to use
│   ├── How to use (4 steps)
│   ├── Core principles (3-5 bullets)
│   └── Links to references/
└── references/
    ├── formats.md        # Detailed templates
    ├── workflows.md      # Complex processes
    └── examples.md       # Usage examples
```

**Pattern**: Main file points to details. Claude reads details only when needed.

## Writing Style

**Third-person descriptions**:
- Good: "Claude should use this skill when analyzing data"
- Bad: "You should use this skill"
- Bad: "I can help you analyze data"

**Imperative instructions**:
- Good: "To extract text, use pdfplumber"
- Bad: "You should extract text using pdfplumber"
- Bad: "If you need to extract text, you might want to use pdfplumber"

**No marketing speak**:
- Avoid: cutting-edge, innovative, state-of-the-art, revolutionary
- Avoid: emojis, exclamation points, hype
- Use: direct, pragmatic, technical language

## Required Sections

Every SKILL.md should have:

### 1. When to use this skill
Specific triggers and scenarios:
```markdown
## When to use this skill

Use for CSV files, spreadsheets, sales data, customer metrics, 
or any tabular data requiring analysis and insights.
```

### 2. How to use this skill
4-step workflow:
```markdown
## How to use this skill

1. Identify the type (summary, comparison, trend)
2. Load appropriate template from references/
3. Apply core principles
4. Create structured output
```

### 3. Core principles
3-5 key rules:
```markdown
## Core principles

1. **Answer-first** - Lead with conclusion
2. **Evidence-based** - Claims need sources
3. **Concise** - No unnecessary words
```

### 4. Keywords
For discoverability:
```markdown
## Keywords

data analysis, CSV, spreadsheet, metrics, business intelligence
```

## Degrees of Freedom

Match specificity to task fragility.

**High freedom** (text instructions): Multiple valid approaches
```markdown
## Code review

1. Analyze structure
2. Check for bugs
3. Suggest improvements
4. Verify conventions
```

**Low freedom** (exact scripts): Operations are fragile
```markdown
## Database migration

Run exactly: `python scripts/migrate.py --verify --backup`
Do not modify or add flags.
```

## Workflows

For multi-step tasks, provide clear sequences:

```markdown
## PDF form filling workflow

1. **Analyze form**: Run `scripts/analyze_form.py input.pdf`
2. **Create mapping**: Edit fields.json
3. **Validate**: Run `scripts/validate_fields.py fields.json`
4. **Fill form**: Run `scripts/fill_form.py input.pdf fields.json output.pdf`
5. **Verify**: Run `scripts/verify_output.py output.pdf`
```

## Reference Files

Move detailed content to `references/`:

**SKILL.md** (main file):
```markdown
## Document formats

For templates, see [references/formats.md](references/formats.md)
```

**references/formats.md**:
```markdown
# Document Formats

## Strategic Memo
[Full template with all sections]

## Status Report
[Full template with all sections]
```

**Keep references one level deep**. Don't nest references within references.

## Common Patterns

### Template Pattern
Provide exact output structure:
```markdown
## Report format

Use this exact structure:
```markdown
# [Title]
## Summary
[One paragraph]
## Findings
- Finding 1
- Finding 2
```
```

### Examples Pattern
Show input/output pairs:
```markdown
## Commit message format

**Example**:
Input: Added JWT authentication
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation
```
```

## Anti-Patterns

**Don't offer too many options**:
- Bad: "Use pypdf, or pdfplumber, or PyMuPDF, or..."
- Good: "Use pdfplumber. For scanned PDFs, use pytesseract."

**Don't use Windows paths**:
- Bad: `scripts\helper.py`
- Good: `scripts/helper.py`

**Don't explain basics**:
- Bad: "Functions are reusable blocks of code that..."
- Good: "Use this function..."

## Scripts and Assets

**Scripts** (`scripts/`): Executable code
- More reliable than generated code
- Saves tokens (no code in context)
- Ensures consistency
- Make it clear: execute vs. read as reference

**References** (`references/`): Documentation
- Loaded into context when needed
- Schemas, APIs, policies, workflows
- If >10k words, provide grep patterns in main file

**Assets** (`assets/`): Output resources
- Not loaded into context
- Used in final output
- Templates, images, fonts, boilerplate

## Iteration Process

1. **Test without skill** - Document specific failures
2. **Create evaluations** - Build 3 test scenarios
3. **Write minimal instructions** - Just enough to pass tests
4. **Iterate** - Refine based on real behavior
5. **Observe Claude** - Watch how it navigates the skill

## Quality Checklist

Before shipping:
- [ ] Description is specific with triggers
- [ ] SKILL.md under 50 lines
- [ ] "When to use" section included
- [ ] "How to use" workflow (4 steps)
- [ ] Core principles (3-5 bullets)
- [ ] Keywords for discoverability
- [ ] References files for details
- [ ] No marketing language
- [ ] Third-person, imperative voice
- [ ] Tested with real prompts

## Quick Reference

**Good SKILL.md structure**:
```yaml
---
name: skill-name
description: What it does and when to use it. Specific triggers.
---

## When to use this skill
[Specific scenarios]

## How to use this skill
1. Step one
2. Step two
3. Step three
4. Step four

## Core principles
1. Key rule
2. Key rule
3. Key rule

## References
See [references/file.md](references/file.md)

## Keywords
keyword, keyword, keyword
```

**File sizes**:
- SKILL.md: 30-50 lines
- References: 50-200 lines each
- Total skill: As needed (references loaded on-demand)

That's the guide. Keep skills lean, tested, and iterated based on real usage.

