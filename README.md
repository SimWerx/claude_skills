# Claude Skills

Professional productivity skills repository built on Anthropic's Skills framework.

**Forked from**: anthropics/skills
**License**: See LICENSE files in individual skill directories

## What are Skills?

Skills are modular packages that extend Claude's capabilities with specialized knowledge and workflows. Each skill teaches Claude how to complete specific tasks in a repeatable way using progressive disclosure: lightweight metadata at startup, full instructions loaded on-demand, detailed references accessed as needed.

For comprehensive documentation, see:
- [Skills Overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Creating Custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)

## Repository Skills

### Anthropic Reference Skills (Included)

**template-skill** - Basic template for creating new skills from scratch

**skill-creator** - Comprehensive meta-skill for creating effective skills with scripts for initialization, validation, and packaging

**internal-comms** - Write internal communications (3P updates, newsletters, FAQs, status reports) with example templates for each format

**document-skills/** - Production-grade skills for document manipulation:
- **docx** - Create, edit, analyze Word documents with tracked changes and comments
- **pdf** - Extract text/tables, fill forms, merge/split documents
- **pptx** - Create, edit, analyze PowerPoint presentations with layouts and charts
- **xlsx** - Create, edit, analyze Excel spreadsheets with formulas and formatting

### Custom Productivity Skills

**research-synthesis** - Transform research materials into executive summaries with proper citations, evidence hierarchy, and actionable insights. Progressive disclosure: Core principles in main file, output formats in `references/`.

**executive-memo** - Create strategic memos, status reports, decision documents, and technical briefs using direct, pragmatic senior PM voice. Progressive disclosure: Workflows in main file, detailed templates in `references/`.

**data-interrogation** - Analyze CSV/tabular data with executive-level insights, pattern detection, and actionable recommendations. Progressive disclosure: Key principles in main file, analysis formats in `references/`.

**technical-docs** - Create technical markdown documentation (READMEs, API docs, changelogs, specs) with proper syntax and standard conventions. Progressive disclosure: Core conventions in main file, detailed templates in `references/`.

## Using These Skills

### In Claude.ai

1. Navigate to Settings → Capabilities → Skills
2. Upload skill folder (ZIP if needed)
3. Enable the skill
4. Reference in conversations when needed

### In Claude Code (Cursor)
```

Or reference skills directly in project `.cursor/rules/` directory.

### Via Claude API

See [Skills API Guide](https://docs.anthropic.com/en/api/skills-guide) for programmatic usage.

## Creating New Skills

### Quick Start

Use Anthropic's initialization script:

```bash
python skill-creator/scripts/init_skill.py my-new-skill --path ./
```

This creates:
- `my-new-skill/SKILL.md` with proper frontmatter template
- `scripts/`, `references/`, `assets/` subdirectories
- Example files showing structure

### Skill Structure

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter: name + description
│   └── Markdown: instructions, workflows, references
├── scripts/ (optional)
│   └── Executable code for reliability
├── references/ (optional)
│   └── Documentation loaded as needed
└── assets/ (optional)
    └── Files used in output (templates, images)
```

### Design Principles

Following Anthropic's best practices:

1. **Concise** - Only include context Claude doesn't already have. Challenge every sentence.
2. **Progressive disclosure** - SKILL.md overview, detailed content in `references/`
3. **Third-person descriptions** - "Claude should use this skill when..."
4. **Imperative instructions** - "To accomplish X, do Y" (not "You should...")
5. **Clear triggers** - Specific use cases and keywords for discoverability
6. **Workflows** - Step-by-step "How to use this skill" sections

### Validation and Packaging

Validate skill structure:
```bash
python skill-creator/scripts/quick_validate.py path/to/skill
```

Package for distribution:
```bash
python skill-creator/scripts/package_skill.py path/to/skill
```

### AI-Powered Skill Generation (Recommended)

For rapid prototyping and production-ready skills, use the **Skills Factory Generator** in Claude Code/Cursor:

**Quick start**:
1. Drag `SKILLS_FACTORY_GENERATOR_PROMPT.md` into Claude Code conversation
2. Request: `"Generate a skill for analyzing customer feedback CSV files"`
3. Claude creates complete skill files and ZIP automatically
4. Upload ZIP to Claude.ai → Settings → Skills

**What you get**:
- Fully populated SKILL.md (not template placeholders)
- Complete references/ with production-ready templates
- Functional Python scripts (when necessary)
- Realistic test data (10-20 lines)
- Automatic ZIP packaging
- Zero manual work required

**Comparison**:

| Tool | Output | Time Required | Manual Work |
|------|--------|---------------|-------------|
| `init_skill.py` | Template skeleton | Instant | 2-4 hours to complete |
| **Skills Factory** | Production-ready skill | 30 seconds | None |

**Example requests**:
- `"Generate a skill for converting meeting notes to action items"`
- `"Create 3 skills for financial services: quarterly analysis, risk assessment, compliance docs"`
- `"Generate an advanced skill with Python script for processing invoice PDFs"`

See [docs/skills-factory-guide.md](docs/skills-factory-guide.md) for comprehensive usage guide, examples, and best practices.

## Repository Structure

```
claude_skills/
├── README.md                              # This file
├── CLAUDE.md                              # Claude Code operational guide
├── SKILLS_FACTORY_GENERATOR_PROMPT.md    # AI-powered skill generator
├── docs/                                  # Reference documentation
│   ├── skill-format-spec.md               # SKILL.md format specification
│   ├── skill-authoring-guide.md           # Best practices for creating skills
│   └── skills-factory-guide.md            # AI-powered skill generation guide
├── generated-skills/                      # Auto-generated skills (from Factory)
│   └── [skill-name]/                      # Production-ready skills
└── zips/                                  # ZIP files ready for Claude.ai upload
│   └── [skill-name].zip
├── template-skill/                        # Basic skill template
├── skill-creator/                         # Meta-skill for skill creation
│   └── scripts/
│       ├── init_skill.py                  # Initialize new skill
│       ├── package_skill.py               # Validate and package
│       └── quick_validate.py              # Fast validation
├── internal-comms/                        # Anthropic's internal comms skill
│   └── examples/                          # 3P updates, newsletters, FAQs
├── document-skills/                       # Anthropic's production doc skills
│   ├── docx/
│   ├── pdf/
│   ├── pptx/
│   └── xlsx/
├── research-synthesis/                    # Custom: Research synthesis
│   └── references/
│       └── formats.md                     # Output templates
├── executive-memo/                        # Custom: Business documents
│   └── references/
│       └── formats.md                     # Document templates
├── data-interrogation/                    # Custom: Data analysis
│   └── references/
│       └── formats.md                     # Analysis formats
└── technical-docs/                        # Custom: Technical documentation
    └── references/
        └── templates.md                   # Doc templates
```

## Reference Documentation

**docs/skill-format-spec.md** - Quick reference for valid SKILL.md structure, frontmatter requirements, and validation rules.

**docs/skill-authoring-guide.md** - Comprehensive best practices for creating high-quality skills with progressive disclosure, workflows, and quality checklist.

**docs/skills-factory-guide.md** - Complete guide to AI-powered skill generation using the Skills Factory Generator in Claude Code/Cursor. Includes examples, patterns, customization options, and troubleshooting.

## Contributing

This repository welcomes contributions. New skills should:
1. Follow patterns in `docs/skill-authoring-guide.md`
2. Use progressive disclosure (lean SKILL.md, details in references/)
3. Include "When to use" and "How to use" sections
4. Be tested with real usage before committing


## References

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Best Practices Guide](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)

---

**Last Updated**: October 2024
**Maintained by**: Community Contributors
