# Claude Skills - CEO/TPM Productivity

Custom skills for CEO and Technical Product Manager workflows, built on Anthropic's Skills framework.

## What are Skills?

Skills are modular packages that extend Claude's capabilities with specialized knowledge and workflows. Each skill teaches Claude how to complete specific tasks in a repeatable way.

For comprehensive information, see [Anthropic's Skills Documentation](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills).

## Available Skills

### From Anthropic (Reference)
- **template-skill** - Basic template for creating new skills
- **skill-creator** - Meta-skill for creating effective skills
- **internal-comms** - Writing internal communications (status reports, updates, FAQs)
- **document-skills/** - Production skills for DOCX, PDF, PPTX, XLSX manipulation

### Custom CEO/TPM Skills
- **research-synthesis** - Transform research into executive summaries with citations
- **executive-memo** - Create business memos and strategic documents
- **data-interrogation** - Analyze CSV/tabular data with executive insights
- **technical-docs** - Create and maintain technical markdown documentation

## Using These Skills

### In Claude.ai
1. Upload the skill folder (as ZIP if needed)
2. Enable in Settings → Capabilities
3. Reference the skill in your conversation

### In Claude Code (Cursor)
You can register this repository as a plugin marketplace:
```bash
/plugin marketplace add SimWerx/claude_skills
/plugin install custom-skills@simwerx-skills
```

### Via API
See the [Skills API Guide](https://docs.anthropic.com/en/api/skills-guide) for implementation.

## Creating Custom Skills

Each skill is a directory with a `SKILL.md` file:

```yaml
---
name: my-skill-name
description: What the skill does and when Claude should use it
---

# Instructions here
```

Use `template-skill` as your starting point, or see `skill-creator` for comprehensive guidance.

## Repository Structure

```
claude_skills/
├── README.md
├── template-skill/          # Basic template
├── skill-creator/           # Guide for creating skills
├── internal-comms/          # Anthropic's internal comms skill
├── document-skills/         # Anthropic's document manipulation skills
├── research-synthesis/      # Custom: Research synthesis
├── executive-memo/          # Custom: Business memos
├── data-interrogation/      # Custom: Data analysis
└── technical-docs/          # Custom: Technical documentation
```

## Skill Design Principles

Following Anthropic's best practices:
- **Concise** - Only include context Claude doesn't already have
- **Progressive disclosure** - SKILL.md points to detailed references as needed
- **Focused** - One workflow per skill, not everything at once
- **Third-person descriptions** - "Claude should use this skill when..."
- **Imperative instructions** - "To accomplish X, do Y"

## References

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Skills Overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Creating Custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)

## Contributing

This is a working repository for SimWerx/Liberty Dynamic productivity workflows. Custom skills may be company-specific.

## License

- Anthropic's example skills: See individual LICENSE.txt files
- Custom skills: Internal use
