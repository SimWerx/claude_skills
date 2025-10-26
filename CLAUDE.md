# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **skills repository** for extending Claude's capabilities with specialized knowledge and workflows. Skills are modular packages that teach Claude how to complete specific tasks consistently using progressive disclosure: lightweight metadata at startup, full instructions loaded on-demand, detailed references accessed as needed.

**Forked from**: anthropics/skills
**Purpose**: Professional productivity workflows and business skills

## Commands

### Skill Creation and Validation

```bash
# Create a new skill from template
python skill-creator/scripts/init_skill.py my-new-skill --path ./

# Validate a skill's structure and frontmatter
python skill-creator/scripts/quick_validate.py path/to/skill

# Package a skill for distribution (validates first)
python skill-creator/scripts/package_skill.py path/to/skill
```

## Skill Creation Workflow

This repository provides two methods for creating skills, with distinct use cases:

### Primary Method: Skills Factory Generator (AI-Powered)

**Use for**: Creating new production-ready skills from scratch

**How it works**:
1. Drag `SKILLS_FACTORY_GENERATOR_PROMPT.md` into Claude Code conversation
2. Describe the skill you need in natural language
3. Claude generates complete skill automatically:
   - SKILL.md with full content (not placeholders)
   - sample_prompt.md with test examples
   - references/ with detailed templates
   - assets/ with sample data
   - ZIP file ready for deployment

**Advantages**:
- Complete, production-ready output in 30 seconds
- No manual template filling required
- Automatic validation and packaging
- Best practices built-in

**See**: [SKILLS_FACTORY_GENERATOR_PROMPT.md](SKILLS_FACTORY_GENERATOR_PROMPT.md)

### Utility Scripts: skill-creator/ (Validation & Packaging Only)

**Use for**: Validating and packaging existing skills

**Available scripts**:
- `quick_validate.py` - Verify SKILL.md structure, frontmatter, naming
- `package_skill.py` - Create ZIP files for Claude.ai upload (validates first)
- `init_skill.py` - Legacy template generator (creates empty scaffolds)

**When to use scripts directly**:
- Validating manually-created skills
- Packaging skills for distribution
- Quick structure checks during development

**Recommendation**: Use Skills Factory Generator for creation, scripts for validation/packaging

### Git Operations

This repository uses standard git workflows. When committing:
- Follow existing commit message style (see git log)
- Focus commit messages on "why" rather than "what"
- Keep commits atomic and focused

## Architecture

### Skill Structure (Universal Pattern)

Every skill follows this standard architecture:

```
skill-name/
├── SKILL.md (required)          # Lean navigation file (30-50 lines)
│   ├── YAML frontmatter         # name + description
│   ├── When to use this skill   # Specific triggers
│   ├── How to use this skill    # 4-step workflow
│   ├── Core principles          # 3-5 key rules
│   └── Links to references/     # Pointers to details
├── scripts/ (optional)          # Executable code (Python/Bash)
├── references/ (optional)       # Documentation loaded as-needed
└── assets/ (optional)           # Files used in output (not loaded to context)
```

### Progressive Disclosure (Three-Level Loading)

1. **Metadata** (always loaded): ~100 words from YAML frontmatter
2. **SKILL.md** (loaded when triggered): <500 lines, navigation and workflows
3. **References** (loaded as needed): Unlimited detail, loaded on-demand

This pattern ensures efficient token usage by loading only what's needed when it's needed.

### Two Skill Categories

**Anthropic Reference Skills** (included for reference):
- `template-skill` - Basic template for new skills
- `skill-creator` - Meta-skill with init/validate/package scripts
- `internal-comms` - Internal communications templates
- `document-skills/` - Production DOCX, PDF, PPTX, XLSX skills

**Custom Productivity Skills**:
- `research-synthesis` - Research → executive summaries with citations
- `executive-memo` - Strategic memos, status reports, decision docs
- `data-interrogation` - CSV analysis → actionable insights
- `technical-docs` - Technical markdown documentation (READMEs, API docs)

## SKILL.md Format Requirements

### Required YAML Frontmatter

```yaml
---
name: skill-name                          # Lowercase + hyphens only
description: What it does and when to use it. Specific triggers.
---
```

**Validation Rules** (enforced by `quick_validate.py`):
- Name: Lowercase letters, digits, hyphens only (no underscores/spaces)
- Name must match directory name exactly
- Description: Must include WHAT the skill does AND WHEN to use it
- No angle brackets (< >) in description
- YAML frontmatter properly formatted with `---` delimiters

### Optional YAML Frontmatter Fields

**allowed-tools** (Claude Code only):

Restrict which tools Claude can use when this skill is active. Useful for read-only workflows, security-sensitive operations, or limiting scope.

```yaml
---
name: safe-file-reader
description: Read-only file access for code review. Use when analyzing code without making changes.
allowed-tools: Read, Grep, Glob
---
```

When `allowed-tools` is specified, Claude can ONLY use those tools while the skill is active (no permission prompts needed for listed tools).

**Use cases**:
- Read-only skills that shouldn't modify files
- Skills with limited scope (e.g., data analysis only)
- Security-sensitive workflows requiring tool restrictions

**Important**: This feature only works in Claude Code. Skills uploaded to Claude.ai ignore this field and follow standard permission model.

### Required Sections in SKILL.md

1. **When to use this skill** - Specific scenarios and file types
2. **How to use this skill** - 4-step workflow
3. **Core principles** - 3-5 key rules
4. **Keywords** - For discoverability

### File Size Targets

- SKILL.md: 30-50 lines (overview only)
- References: 50-200 lines each (detailed content)
- Total skill: As needed (references loaded on-demand)

## Writing Style (Critical)

**Third-person descriptions**:
- ✅ Good: "Claude should use this skill when analyzing data"
- ❌ Bad: "You should use this skill"

**Imperative instructions**:
- ✅ Good: "To extract text, use pdfplumber"
- ❌ Bad: "You should extract text using pdfplumber"

**No marketing speak**:
- Avoid: cutting-edge, innovative, state-of-the-art, revolutionary, emojis, hype
- Use: direct, pragmatic, technical language

**Assume Claude is smart**:
- Only include what Claude doesn't already know
- Challenge every sentence: "Does this justify its token cost?"
- Skip basics like "functions are reusable blocks of code..."

**Emphatic language for progressive disclosure**:

When directing Claude to read additional context files, use strong, explicit directives:

- ✅ Good: "🚨 **REQUIRED READING**: Before generating hooks, you MUST read `references/frameworks.md`"
- ✅ Good: "To create thumbnails, you **MUST** carefully review the design requirements in `Design Requirements.md`"
- ✅ Good: "**ABSOLUTELY CRITICAL**: Read `prompting-guidelines.md` before calling the API"
- ❌ Bad: "See `references/frameworks.md` for more details"
- ❌ Bad: "Review the design requirements if needed"

**Pattern**: Use conditional phrasing that creates explicit dependencies:
```markdown
Before doing X, you MUST read: `/path/to/file.md`

If you want to do Y, then you **MUST** also read: `/path/to/context.md`
```

This emphatic language ensures Claude loads critical context at the right time, making progressive disclosure more reliable.

## Resource Directory Conventions

### scripts/ - Executable Code
- Python/Bash scripts that can be run directly
- More reliable than generated code
- Saves tokens (no code in context)
- Make executable with `chmod +x`
- Example: [pdf/scripts/fill_fillable_fields.py](document-skills/pdf/scripts/fill_fillable_fields.py)

### references/ - Documentation
- Loaded into context when needed
- Schemas, APIs, policies, workflows, templates
- Keep one level deep (no nesting)
- Example: [research-synthesis/references/formats.md](research-synthesis/references/formats.md)

### assets/ - Output Resources
- NOT loaded into context
- Used in final output Claude produces
- Templates, images, fonts, boilerplate
- Example: Brand templates, starter projects

## Skill Creation Workflow

1. **Test without skill** - Document specific failures
2. **Plan resources** - Decide what goes in scripts/, references/, assets/
3. **Initialize**: `python skill-creator/scripts/init_skill.py my-skill --path ./`
4. **Edit SKILL.md** - Complete TODO items, keep under 50 lines
5. **Customize resources** - Add scripts/references/assets or delete example files
6. **Validate**: `python skill-creator/scripts/quick_validate.py my-skill`
7. **Iterate** - Test with real usage, refine based on behavior

## Common Patterns

### Template Pattern
Provide exact output structure in references/:
```markdown
## Report format

Use this exact structure:
# [Title]
## Summary
[One paragraph]
## Findings
- Finding 1
```

### Workflow Pattern
For multi-step tasks, provide clear sequences:
```markdown
## How to use this skill

1. Identify the type (summary, comparison, trend)
2. Load appropriate template from references/
3. Apply core principles
4. Create structured output
```

## Anti-Patterns (Avoid)

- ❌ Don't offer too many options: "Use pypdf, or pdfplumber, or PyMuPDF..."
- ❌ Don't use Windows paths: `scripts\helper.py`
- ❌ Don't explain basics Claude already knows
- ❌ Don't nest references within references (keep one level deep)
- ❌ Don't include marketing language or emojis
- ❌ Don't make SKILL.md longer than 50 lines (move details to references/)

## Key Skill-Creator Scripts

### [init_skill.py](skill-creator/scripts/init_skill.py)
Creates new skill scaffold with:
- SKILL.md template with TODO placeholders
- Example directories: scripts/, references/, assets/
- Example files showing proper structure

### [quick_validate.py](skill-creator/scripts/quick_validate.py)
Fast validation checking:
- SKILL.md exists
- Valid YAML frontmatter (name + description)
- Naming conventions (hyphen-case, lowercase)
- No angle brackets in description
- Returns exit code 0 (valid) or 1 (invalid)

### [package_skill.py](skill-creator/scripts/package_skill.py)
Validates and packages skill into distributable ZIP:
- Runs validation first
- Creates ZIP maintaining directory structure
- Output: `skill-name.zip`

## Reference Documentation

- [docs/skill-format-spec.md](docs/skill-format-spec.md) - SKILL.md structure and validation rules
- [docs/skill-authoring-guide.md](docs/skill-authoring-guide.md) - Comprehensive best practices

## Repository-Specific Conventions

### Custom Skills Follow These Patterns
- **Answer-first methodology** - Lead with conclusion
- **Evidence-based** - All claims need sources
- **Professional tone** - Direct, pragmatic, senior PM voice
- **Progressive disclosure** - Core principles in SKILL.md, detailed templates in references/

## Quality Checklist

Before shipping a skill:
- [ ] Description is specific with triggers
- [ ] SKILL.md under 50 lines
- [ ] "When to use" section included
- [ ] "How to use" workflow (4 steps)
- [ ] Core principles (3-5 bullets)
- [ ] Keywords for discoverability
- [ ] References files for details
- [ ] No marketing language
- [ ] Third-person, imperative voice
- [ ] Validates with `quick_validate.py`
- [ ] Tested with real prompts
- [ ] **Multi-model tested**: Validated on Haiku (fast), Sonnet (balanced), and Opus (most capable)
- [ ] Works across deployment platforms (Claude.ai ZIP, Claude Code filesystem, API if applicable)

## Key Insights

1. **Skills are teaching tools** - Each skill is a specialized "onboarding guide" for Claude
2. **Token efficiency is critical** - Progressive disclosure prevents context bloat
3. **Scripts > Generated Code** - Include executable scripts for repeated operations
4. **Templates enable consistency** - Reference files ensure consistent output structure
5. **Keep SKILL.md lean** - Main file is navigation, details live in references/

## Staying Updated with Official Anthropic Standards

This repository tracks official Anthropic guidance to ensure compatibility with the latest Skills capabilities.

### Primary Sources (Monitor Regularly)

**1. Anthropic's Official Skills Repository**
- URL: https://github.com/anthropics/skills
- Status: 13.7k+ stars, actively maintained (as of October 2025)
- License: Apache 2.0 (can fork and adapt)
- Contents: Reference skills, document manipulation examples
- **Action**: Watch repo for commits, review quarterly for new patterns

**2. Official Documentation**
- URL: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/
- Pages to monitor:
  - Best Practices: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
  - Claude Code Skills: https://docs.claude.com/en/docs/claude-code/agent-skills
  - Skills API: https://docs.anthropic.com/en/api/skills-guide
- **Action**: Monthly review for updates, breaking changes

**3. Anthropic Engineering Blog**
- URL: https://www.anthropic.com/engineering
- Key post: "Equipping agents for the real world with Agent Skills"
- **Action**: Subscribe to announcements, review new posts quarterly

**4. Community Resources**
- travisvn/awesome-claude-skills: Curated community skills
- claude-code-plugins-plus: Plugin marketplace with 227+ plugins
- **Action**: Review for emerging patterns, popular approaches

### What to Check During Reviews

**Quarterly Review Checklist**:
- [ ] New YAML frontmatter fields (like `allowed-tools` added Oct 2025)
- [ ] Updated validation requirements
- [ ] New best practices or patterns
- [ ] Breaking changes to skill format
- [ ] New API endpoints or capabilities
- [ ] Plugin system updates
- [ ] Multi-model testing recommendations

**When Updating This Repo**:
1. Compare official examples against our templates
2. Update SKILLS_FACTORY_GENERATOR_PROMPT.md with new patterns
3. Refresh docs/skill-authoring-guide.md with latest best practices
4. Test generated skills against new requirements
5. Update Quality Checklist with new criteria

### Version Tracking

**Document skills disclaimer**: Per Anthropic, document skills (DOCX, PDF, PPTX, XLSX) are "point-in-time snapshots and are not actively maintained." Use them as reference implementations, not production dependencies.

**Latest known updates**:
- October 2025: Skills API (`/v1/skills`) announced
- October 2025: `allowed-tools` frontmatter field added (Claude Code only)
- October 2025: Plugin distribution system launched
- October 2025: Personal vs Project skills distinction formalized

**Maintenance cadence**: Review official sources monthly, update this repo quarterly (or when breaking changes announced).
