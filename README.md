# SimWerx/Liberty Dynamic - Claude Skills

Internal productivity skills repository for CEO/TPM workflows, built on Anthropic's Skills framework.

**Repository**: https://github.com/SimWerx/claude_skills  
**Forked from**: anthropics/skills  
**Status**: Internal use - Private skills development

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

### SimWerx Custom Skills (CEO/TPM Workflows)

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

Register this repository as a plugin marketplace:
```bash
/plugin marketplace add SimWerx/claude_skills
/plugin install simwerx-custom-skills
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

## Repository Structure

```
claude_skills/
├── README.md                  # This file
├── template-skill/            # Basic skill template
├── skill-creator/             # Meta-skill for skill creation
│   └── scripts/
│       ├── init_skill.py      # Initialize new skill
│       ├── package_skill.py   # Validate and package
│       └── quick_validate.py  # Fast validation
├── internal-comms/            # Anthropic's internal comms skill
│   └── examples/              # 3P updates, newsletters, FAQs
├── document-skills/           # Anthropic's production doc skills
│   ├── docx/
│   ├── pdf/
│   ├── pptx/
│   └── xlsx/
├── research-synthesis/        # Custom: Research synthesis
│   └── references/
│       └── formats.md         # Output templates
├── executive-memo/            # Custom: Business documents
│   └── references/
│       └── formats.md         # Document templates
├── data-interrogation/        # Custom: Data analysis
│   └── references/
│       └── formats.md         # Analysis formats
└── technical-docs/            # Custom: Technical documentation
    └── references/
        └── templates.md       # Doc templates
```

## Roadmap

### Planned Skills (Liberty Dynamic Specific)

- **brand-compliance** - Liberty Dynamic terminology, voice, regulatory language
- **product-docs** - EDD technical documentation with approved terminology
- **presentation-audit** - Extract and analyze PPTX content for terminology violations
- **sales-materials** - Generate sales content with brand compliance checking

These will incorporate Liberty Dynamic memories:
- Terminology preferences (fuel air event, EDD Initiator, concussive output)
- Regulatory context (BATFE compliance, NFA regulations)
- Brand positioning (premium product, not cost-saving)
- Location specifics (Denver HQ, timing precision)

## Contributing

This is an internal working repository for SimWerx/Liberty Dynamic. New skills should:
1. Follow Anthropic's best practices (see `skill-creator/SKILL.md`)
2. Use progressive disclosure pattern
3. Include clear triggers and workflows
4. Be tested with real usage before committing

## License

- **Anthropic skills**: See individual LICENSE.txt files in skill directories
- **Custom skills**: SimWerx/Liberty Dynamic internal use
- **This repository**: Forked from anthropics/skills (Apache 2.0)

## References

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Best Practices Guide](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [SimWerx Fork](https://github.com/SimWerx/claude_skills)

---

**Last Updated**: January 2025  
**Maintained by**: SimWerx Team
