# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **skills repository** for extending Claude's capabilities with specialized knowledge and workflows. Skills are modular packages that teach Claude how to complete specific tasks consistently using progressive disclosure: lightweight metadata at startup, full instructions loaded on-demand, detailed references accessed as needed.

**Forked from**: anthropics/skills
**Purpose**: Professional productivity workflows and business skills
**Aligned with**: Anthropic Agent Skills Spec v1.0 (October 16, 2025)

## Skill Creation

### Primary Method: Skill Factory (AI-Powered)

**Use for**: Creating production-ready skills from natural language descriptions

**How it works**:
1. Load the `skill-factory` skill
2. Describe the skill you need in natural language
3. Claude generates complete skill automatically:
   - SKILL.md with full content (not placeholders)
   - sample_prompt.md with test examples
   - references/ with detailed templates
   - assets/ with sample data

**Advantages**:
- Complete, production-ready output in 30 seconds
- No manual template filling required
- Automatic validation
- Best practices built-in

**Location**: `skill-factory/SKILL.md`

**Usage**:
```
Load the skill-factory skill and help me create a new skill for [your use case].
```

### Utility Scripts

**Validation and packaging** for deployment to Claude.ai/Claude Desktop:

```bash
# Validate a skill's structure and frontmatter
python scripts/quick_validate.py path/to/skill

# Package a skill into ZIP for upload (validates first)
python scripts/package_skill.py path/to/skill
```

Output ZIPs are saved to `zips/` for upload to Claude.ai → Settings → Skills.

### Research-Enhanced Workflow (Automatic)

When generating skills about frameworks, tools, or evolving best practices, the Skill Factory automatically invokes the `background-research` skill to:
- Ground skills in current evidence (sources from 2024-2025)
- Include source citations for credibility: "(Source: Publication, Year)"
- Add temporal context ("as of December 2025")
- Identify deprecated approaches
- Ensure recommendations reflect current standards

**Auto-detection logic**:
- Invoke research: Frameworks, methodologies, tools, best practices
- Skip research: Evergreen workflows, fixed specifications, user-provided complete specs

**User control**:
- `research_depth: skip` - Force skip (fast, no web searches)
- `research_depth: standard` - 2-3 searches (default when auto-detected)
- `research_depth: comprehensive` - 5+ searches (thorough investigation)

See `skill-factory/references/generation-workflow.md` for complete heuristics and [background-research skill](generated-skills/background-research/) for methodology.

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
├── SKILL.md (required)          # Under 500 lines, concise navigation
│   ├── YAML frontmatter         # name + description
│   ├── When to use this skill   # Specific triggers
│   ├── How to use this skill    # Workflow steps
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

### Skill Categories

**Core Infrastructure Skills**:
- `skill-factory` - AI-powered skill generator with progressive disclosure
- `background-research` - Web research for temporal grounding

**Example Skills** (`examples/`):
- `internal-comms` - Internal communications templates
- `document-skills/` - Production DOCX, PDF, PPTX, XLSX skills
- `data-interrogation` - CSV analysis patterns
- `executive-memo` - Strategic document templates
- `technical-docs` - Technical markdown documentation

**Custom Productivity Skills** (root level):
- `research-synthesis` - Research → executive summaries with citations

### research-archive/ - Research Audit Trail

Research outputs from the `background-research` skill are archived here with timestamps.

**Purpose**:
- **Auditability**: Verify sources and statistics used in skill generation
- **Currency tracking**: Know when research was conducted to assess if skills need updating
- **Re-use**: Reference existing research when generating related skills
- **Team collaboration**: Share research artifacts without sharing entire chat history
- **Fact-checking**: Validate claims against original sources

**Naming convention**: `YYYY-MM-DD-HHMM-topic-kebab.md`
- Date/time: When research was conducted (e.g., `2025-10-25-1430`)
- Topic: Kebab-case version of research topic, max 50 chars
- Example: `2025-10-25-1430-ai-engine-optimization.md`

**Gitignored**: Yes (development artifacts, not source code)

**Relationship to skills**:
- Archive = source of truth (local development)
- `references/research-findings.md` = copy included in ZIP (for uploaded skills)
- SKILL.md HTML comment points to archive location

**Usage patterns**:
- Single research → single skill: One archive file referenced by one skill
- Batch research → multiple skills: One archive file referenced by multiple skills
- Same topic, different dates: Compare archives to see how domain evolved

**Future enhancements**:
- **Research reuse detection**: Before conducting new research, check for recent research on same topic (<30 days). Options: reuse findings (saves tokens), ask user to reuse or refresh, or always refresh for currency. Improves efficiency for iterative skill development.
- **Auto-generated index**: Create `research-archive/index.md` with metadata table (date, topic, skill, confidence, sources). Enables quick discovery of existing research without scanning filenames.
- **Monthly organization**: If archive grows to 100+ files, organize into monthly subdirectories (e.g., `research-archive/2025-10/`). Currently using flat structure (simpler for small scale).

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

- SKILL.md: Under 500 lines for optimal performance (keep concise, use progressive disclosure)
- References: As needed (detailed content, loaded on-demand)
- Total skill: Unlimited (references loaded only when needed)

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
3. **Generate with Skill Factory**: Load `skill-factory` and describe the skill
4. **Review SKILL.md** - Verify content, keep under 500 lines (use progressive disclosure)
5. **Customize resources** - Add scripts/references/assets as needed
6. **Test** - Use skill on real tasks, verify outputs
7. **Iterate** - Refine based on behavior

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
- ❌ Don't make SKILL.md longer than 500 lines (move detailed content to references/)

## Reference Documentation

- [docs/skill-format-spec.md](docs/skill-format-spec.md) - SKILL.md structure and validation rules
- [docs/skill-authoring-guide.md](docs/skill-authoring-guide.md) - Comprehensive best practices
- [skill-factory/SKILL.md](skill-factory/SKILL.md) - AI-powered skill generation

## Repository-Specific Conventions

### Custom Skills Follow These Patterns
- **Answer-first methodology** - Lead with conclusion
- **Evidence-based** - All claims need sources
- **Professional tone** - Direct, pragmatic, senior PM voice
- **Progressive disclosure** - Core principles in SKILL.md, detailed templates in references/

## Quality Checklist

Before shipping a skill:
- [ ] Description is specific with triggers
- [ ] SKILL.md under 500 lines (concise, with details in references/)
- [ ] "When to use" section included
- [ ] "How to use" workflow (4 steps)
- [ ] Core principles (3-5 bullets)
- [ ] Keywords for discoverability
- [ ] References files for details
- [ ] No marketing language
- [ ] Third-person, imperative voice
- [ ] Tested with real prompts
- [ ] **Multi-model tested**: Validated on Haiku (fast), Sonnet (balanced), and Opus (most capable)
- [ ] Works across deployment platforms (Claude.ai, Claude Desktop, Claude Code, API if applicable)

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
- Status: 19k+ stars, actively maintained (as of December 2025)
- Spec: v1.0 (October 16, 2025)
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
2. Update `skill-factory/` with new patterns
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
