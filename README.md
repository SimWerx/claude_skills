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

## Skills Deployment Options

Skills work across four Claude platforms with different workflows:

### For Claude.ai (ZIP Upload Method)

Upload skills as ZIP files via Settings → Capabilities → Skills.

**Characteristics**:
- Individual user skills only (no organization-wide distribution)
- Must upload separate ZIP for each skill
- Works with our Skills Factory Generator + `package_skill.py`

**Use this repository's tools**: See "Creating New Skills" and "AI-Powered Skill Generation" sections below.

### For Claude Desktop (Native Application)

Native Mac, Windows, and Linux desktop application for power users.

**Deployment**: Settings → Capabilities → Skills
- Same ZIP upload workflow as Claude.ai web interface
- Skills persist locally on your machine
- Individual user skills only (no team distribution)

**When to use Claude Desktop vs Claude Code**:
- **Claude Desktop** = GUI application for non-technical users and general productivity
- **Claude Code** = CLI/IDE integration for developers and technical workflows

**Use this repository's tools**: Same as Claude.ai - see "Creating New Skills" and "AI-Powered Skill Generation" sections below.

### For Claude Code (Personal & Project Skills)

**Personal Skills** (`~/.claude/skills/`):
- Available across **all your projects**
- Store your individual workflows and preferences
- Not shared with team members

```bash
# Create personal skill
mkdir -p ~/.claude/skills/my-skill
# Add SKILL.md with frontmatter
```

**Project Skills** (`.claude/skills/`):
- **Shared with team via git** - checked into repository
- Auto-discovered by teammates when they pull
- Project-specific expertise and conventions

```bash
# Create project skill
mkdir -p .claude/skills/team-skill
# Add SKILL.md, commit to git
git add .claude/skills/
git commit -m "Add team skill for API integration"
git push
```

**Plugin Distribution**: Skills can also be bundled in [Claude Code plugins](https://docs.claude.com/en/docs/claude-code/plugins) for community sharing via marketplace.

### For Claude API

Programmatic access via the `/v1/skills` endpoint (announced October 2025).

**Required headers**:
- `skills-2025-10-02` - Skills API beta access
- `code-execution-2025-08-25` - Only required for skills that include `scripts/` or executable code

**Features**:
- Reference skills by `skill_id` in API calls
- Version control via API
- Supports both Anthropic-managed skills and custom skills
- Programmatic deployment and updates

**Usage example**:
```python
import anthropic

client = anthropic.Anthropic(
    api_key="your-api-key"
)

# Use skill in API call
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    skills=["skill_id_here"],
    messages=[{"role": "user", "content": "Your message"}],
    betas=["skills-2025-10-02"]
)
```

See [Skills API Quickstart](https://docs.anthropic.com/en/api/skills-guide) for comprehensive documentation.

### Migration Between Platforms

**ZIP → Claude Desktop**: Upload ZIP file directly
- Settings → Capabilities → Skills → Upload
- Same workflow as Claude.ai web interface

**ZIP → Claude Code**: Unzip skills into `~/.claude/skills/` or `.claude/skills/`

```bash
# Personal
unzip skill-name.zip -d ~/.claude/skills/

# Project (team-shared)
unzip skill-name.zip -d .claude/skills/
git add .claude/skills/skill-name/
```

**This Repository Supports All Platforms**: Skills generated here work across Claude.ai, Claude Desktop, Claude Code, and API with appropriate deployment methods.

### Platform-Specific Features & Behaviors

Different Claude platforms support different skill features. Understanding these differences helps you choose the right deployment method:

| Feature | Claude.ai | Claude Desktop | Claude Code | API |
|---------|-----------|----------------|-------------|-----|
| **Deployment Method** | ZIP upload | ZIP upload | Filesystem | Programmatic |
| **Team Sharing** | No | No | Yes (project skills) | Yes |
| **Progressive Disclosure** | Yes | Yes | Yes | Yes |
| **allowed-tools** | Ignored | Ignored | **Enforced** | Not applicable |
| **Scripts Execution** | Limited | Limited | Full | Full (with header) |
| **Plugin Distribution** | No | No | Yes | No |

**Key differences**:
- **allowed-tools**: Only enforced in Claude Code. Claude.ai and Claude Desktop ignore this frontmatter field and use standard permission model.
- **Team Sharing**: Claude Code project skills (`.claude/skills/`) are shared via git. API allows programmatic distribution.
- **Scripts**: Full script execution requires `code-execution-2025-08-25` beta header in API calls.

### About .claude/skills/example-project-skill/

This repository includes a working example of a Claude Code project skill.

**Purpose**: Demonstrates the team-shared skills pattern
**Location**: `.claude/skills/` (where Claude Code auto-discovers project skills)
**Function**: Both an example to learn from AND a working skill when using this repo with Claude Code

When you open this repository in Claude Code, it will automatically discover and load this skill, demonstrating how teams can share project-specific expertise via git. The skill itself explains the pattern and provides a template for creating your own team-shared skills.

## Why Skills Over Alternatives?

**Progressive Disclosure is the Core Value**

Skills use a three-tier loading pattern that makes them uniquely efficient:
1. **Metadata only** (always loaded) - Just skill name and description (~100 words)
2. **SKILL.md** (loaded when triggered) - Navigation and workflows (<500 lines)
3. **References** (loaded as needed) - Detailed templates, examples, schemas (unlimited)

This means you can fit far more capabilities into the same context window, or achieve the same capabilities with much smaller context footprint.

**Skills vs MCPs**

| Aspect | Skills | MCPs |
|--------|--------|------|
| **Context loading** | Progressive (name → instructions → details) | Full schemas loaded upfront |
| **Setup complexity** | Just markdown + optional scripts | Server infrastructure required |
| **Execution** | Local, same process as agent | External server |
| **Maintenance** | Simple to debug and iterate | Requires server monitoring |
| **Best for** | Self-contained workflows, local tools | External APIs, shared infrastructure |

**Skills vs Slash Commands**

| Aspect | Skills | Slash Commands |
|--------|--------|----------------|
| **Triggering** | Agent decides when to use | User manually invokes |
| **Autonomy** | Agent chooses inputs/context | User provides all inputs |
| **Flexibility** | Dynamic, context-aware usage | Fixed, linear workflow |
| **Best for** | Agent-driven automation | User-directed templates |

**Skills vs Subagents**

| Aspect | Skills | Subagents |
|--------|--------|-----------|
| **Context** | Inherits full conversation context | Separate, isolated context |
| **Control** | Human-in-the-loop, direct steering | No user interaction once launched |
| **Tool loading** | Progressive disclosure | Full tool schemas loaded |
| **Best for** | Tasks needing conversation context | Isolated, parallel work |

**Key Advantages**

1. **Reduced Context Load** - Only metadata loaded initially; everything else progressively disclosed
2. **Compounding Abilities** - Skills can leverage other skills with minimal overhead
3. **Simplicity** - No infrastructure needed; just markdown files and optional scripts
4. **Agent Autonomy** - Agents decide when and how to use skills
5. **Human-in-Loop** - Direct interaction and steering possible

*Source: Insights from [Anthropic's Skills engineering blog](https://www.anthropic.com/engineering/agent-skills) and community best practices*

## Repository Skills

### Anthropic Reference Skills (Included)

**skill-creator** - Utility scripts for skill validation and packaging
- `quick_validate.py` - Verify SKILL.md structure and frontmatter
- `package_skill.py` - Create ZIP files for Claude.ai upload
- For creating new skills, use Skills Factory Generator (see AI-Powered Skill Generation below)

**internal-comms** - Write internal communications (3P updates, newsletters, FAQs, status reports) with example templates for each format

**document-skills/** - Production-grade skills for document manipulation:
- **docx** - Create, edit, analyze Word documents with tracked changes and comments
- **pdf** - Extract text/tables, fill forms, merge/split documents
- **pptx** - Create, edit, analyze PowerPoint presentations with layouts and charts
- **xlsx** - Create, edit, analyze Excel spreadsheets with formulas and formatting

> **Note**: Document skills (DOCX, PDF, PPTX, XLSX) are point-in-time reference implementations from Anthropic and are not actively maintained. Use them as examples and learning resources rather than production dependencies. For production use, test thoroughly and adapt to your specific requirements.

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

### In Claude Code

**Personal Skills** (just for you):
```bash
# Copy any skill from this repo
mkdir -p ~/.claude/skills/
cp -r skill-name ~/.claude/skills/

# Or unzip generated skills
unzip zips/skill-name.zip -d ~/.claude/skills/

# Restart Claude Code to load the skill
```

**Project Skills** (team-shared):
```bash
# Copy into your project (already done in this repo - see .claude/skills/example-project-skill/)
mkdir -p .claude/skills/
cp -r skill-name .claude/skills/

# Or unzip generated skills
unzip zips/skill-name.zip -d .claude/skills/

# Commit to share with team
git add .claude/skills/
git commit -m "Add skill-name skill for team"
git push
```

**Quick Test**: This repository includes an example project skill at [.claude/skills/example-project-skill/](.claude/skills/example-project-skill/SKILL.md) demonstrating the team-shared pattern.

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

**Browse ready-to-generate skill ideas**: Check out [skill-ideas/](skill-ideas/) for pre-written skill requests you can generate in 30 seconds. Each file contains a complete skill specification ready for the Skills Factory Generator - just reference the file and Claude creates everything automatically.

### Research-Enhanced Skill Generation

The Skills Factory automatically conducts web research for time-sensitive skills (frameworks, tools, best practices) to ensure currency and credibility.

**How it works**:
1. Factory auto-detects research need (Step 2: frameworks/tools/methodologies → invoke research)
2. Invokes `background-research` skill with current date
3. Receives structured findings with source citations
4. Transfers evidence to generated skill

**Research findings are integrated into**:
- **Core Principles**: Evidence-based rules with source citations "(Source: Publication, Year)"
- **References**: Current frameworks and methodologies from research
- **Keywords**: Contemporary terminology discovered in research
- **Descriptions**: Temporal context ("as of October 2025")

**Control research behavior**:
- `research_depth: skip` - No web research (fast, for evergreen skills)
- `research_depth: standard` - 2-3 searches (default for time-sensitive)
- `research_depth: comprehensive` - 5+ searches (deep investigation)

**Example**: When generating an AEO skill, the factory automatically researches "AI Engine Optimization October 2025", finds current statistics (57% AI Overviews presence), and includes source citations (CXL, BrightEdge, Ahrefs 2025) in Core Principles.

**Research persistence**:

When research is conducted, the output is saved to two locations:

1. **research-archive/**: Timestamped archive for audit trail and fact-checking
   - Format: `2025-10-25-1430-ai-engine-optimization.md`
   - Gitignored (local development only)
   - Single source of truth for verifying claims and tracking currency

2. **references/research-findings.md**: Copy included in skill ZIP
   - Uploaded to Claude.ai with skill
   - Available as progressive disclosure context
   - Users can say "review your research findings" in conversation

This dual approach enables both local auditability (archive) and portable context (included in ZIP).

See [background-research skill](generated-skills/background-research/) for complete methodology.

## Repository Structure

```
claude_skills/
├── README.md                              # This file
├── CLAUDE.md                              # Claude Code operational guide
├── SKILLS_FACTORY_GENERATOR_PROMPT.md    # AI-powered skill generator
├── .claude/skills/                        # Example project skills
│   └── example-project-skill/             # Team-shared skill demo
├── docs/                                  # Reference documentation
│   ├── skill-format-spec.md               # SKILL.md format specification
│   ├── skill-authoring-guide.md           # Best practices for creating skills
│   ├── skills-factory-guide.md            # AI-powered skill generation guide
│   ├── agent_skills.md                    # Official Claude docs reference
│   └── skill_blog.md                      # Anthropic blog insights reference
├── skill-ideas/                           # Seed ideas for Skills Factory
│   ├── README.md                          # How to use skill ideas
│   └── *.md files                         # Natural language skill requests
├── generated-skills/                      # Auto-generated skills (gitignored)
│   └── [skill-name]/                      # Production-ready skills
├── zips/                                  # ZIP files (gitignored)
│   └── [skill-name].zip                   # Ready for Claude.ai upload
├── skill-creator/                         # Validation and packaging scripts
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

**docs/agent_skills.md** - Official Claude documentation reference copy for Agent Skills in Claude Code. Synced October 2025.

**docs/skill_blog.md** - Anthropic engineering blog insights on Agent Skills. Source of emphatic language patterns and progressive disclosure best practices.

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

**Last Updated**: October 2025
**Maintained by**: Community Contributors
**Synced with**: Anthropic Skills (Oct 2025) - Multi-platform support, allowed-tools, Skills API
