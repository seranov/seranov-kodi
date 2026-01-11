# Documentation Index

This directory contains all documentation for the Kodi Play Random project.

## Quick Navigation

### For Users
- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[INSTALLATION.md](INSTALLATION.md)** - Detailed installation instructions
- **[README.md](README.md)** - Main project documentation
- **[GITHUB_PAGES_GUIDE.md](GITHUB_PAGES_GUIDE.md)** - How the website works

### For Developers
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute to the project
- **[PYTHON_SCRIPTS_GUIDE.md](PYTHON_SCRIPTS_GUIDE.md)** - Technical documentation for conversion scripts
- **[QUICK_INTEGRATION_GUIDE.md](QUICK_INTEGRATION_GUIDE.md)** - Integration with GitHub Actions

### For Project Maintainers
- **[BUILD_AND_PUBLISH.md](BUILD_AND_PUBLISH.md)** - Build and publishing process
- **[RELEASE_GUIDE.md](RELEASE_GUIDE.md)** - How to create releases
- **[RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)** - Checklist before release
- **[VERSION_UPDATE.md](VERSION_UPDATE.md)** - How to update versions

### All Documentation Files

| File | Purpose | For |
|------|---------|-----|
| README.md | Main project overview | Everyone |
| README.ru.md | Russian translation of README | Russian speakers |
| QUICKSTART.md | Quick start guide | New users |
| QUICKSTART.ru.md | Russian quick start | Russian speakers |
| INSTALLATION.md | Installation instructions | Users |
| INSTALLATION.ru.md | Russian installation guide | Russian speakers |
| KODI_URL_INSTALLATION.md | Installing from repository URL | Users |
| CONTRIBUTING.md | Contribution guidelines | Developers |
| CONTRIBUTING.ru.md | Russian contribution guide | Russian developers |
| BUILD_AND_PUBLISH.md | Build and publish guide | Maintainers |
| BUILD_AND_PUBLISH.ru.md | Russian build guide | Russian maintainers |
| RELEASE_GUIDE.md | Release process | Maintainers |
| RELEASE_CHECKLIST.md | Pre-release checklist | Release manager |
| RELEASE_COMPLETE.md | Completed release info | Maintainers |
| RELEASE_NOTES.md | Release notes | Users |
| VERSION_UPDATE.md | Version update procedure | Maintainers |
| VERSION_UPDATE.ru.md | Russian version update | Russian maintainers |
| GITHUB_PAGES_GUIDE.md | GitHub Pages setup | Website maintainers |
| PYTHON_SCRIPTS_GUIDE.md | Python script documentation | Developers |
| QUICK_INTEGRATION_GUIDE.md | CI/CD integration | DevOps |

## Documentation Organization

### By Audience

#### Users
Start here:
1. [QUICKSTART.md](QUICKSTART.md)
2. [INSTALLATION.md](INSTALLATION.md)
3. [README.md](README.md)

#### Developers
Start here:
1. [CONTRIBUTING.md](CONTRIBUTING.md)
2. [PYTHON_SCRIPTS_GUIDE.md](PYTHON_SCRIPTS_GUIDE.md)
3. [BUILD_AND_PUBLISH.md](BUILD_AND_PUBLISH.md)

#### Maintainers
Start here:
1. [RELEASE_GUIDE.md](RELEASE_GUIDE.md)
2. [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)
3. [BUILD_AND_PUBLISH.md](BUILD_AND_PUBLISH.md)

### By Topic

#### Installation
- [QUICKSTART.md](QUICKSTART.md) - 5-minute setup
- [INSTALLATION.md](INSTALLATION.md) - Detailed instructions
- [KODI_URL_INSTALLATION.md](KODI_URL_INSTALLATION.md) - From repository URL

#### Development
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- [PYTHON_SCRIPTS_GUIDE.md](PYTHON_SCRIPTS_GUIDE.md) - Script details
- [BUILD_AND_PUBLISH.md](BUILD_AND_PUBLISH.md) - Build process

#### Releases & Versions
- [RELEASE_GUIDE.md](RELEASE_GUIDE.md) - Release steps
- [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) - Pre-release checks
- [RELEASE_NOTES.md](RELEASE_NOTES.md) - What's new
- [VERSION_UPDATE.md](VERSION_UPDATE.md) - Version updates

#### GitHub Pages & Deployment
- [GITHUB_PAGES_GUIDE.md](GITHUB_PAGES_GUIDE.md) - Website documentation
- [QUICK_INTEGRATION_GUIDE.md](QUICK_INTEGRATION_GUIDE.md) - CI/CD setup

## Key Concepts

### Repository Structure
```
project/
├── doc/                           # This directory
│   ├── README.md                 # Main documentation
│   ├── QUICKSTART.md             # Quick start guide
│   ├── INSTALLATION.md           # Installation guide
│   ├── CONTRIBUTING.md           # Contribution guide
│   ├── PYTHON_SCRIPTS_GUIDE.md   # Script documentation
│   └── report/                   # Deployment reports
├── scripts/                       # Python scripts
│   ├── convert_md_to_html.py    # MD → HTML converter
│   └── generate_readme.py        # readme.html generator
├── plugin.video.unified.browser/  # Plugin directory
├── plugin.video.random.recursive/ # Plugin directory
├── service.seranov.nfoscanner/   # Service directory
├── context.screenshots/           # Context menu addon
└── repository.seranov/            # Repository addon
```

### GitHub Pages Deployment
```
Commit to main
    ↓
GitHub Actions triggered
    ↓
Convert .md files to .html
    ↓
Generate readme.html with addon cards
    ↓
Create addon ZIP archives
    ↓
Generate addons.xml metadata
    ↓
Deploy to gh-pages branch
    ↓
https://github.com/seranov/kodi-play-random (GitHub Pages)
```

### File Format Notes

#### Markdown Files
- **Naming**: `UPPERCASE.md` or `UPPERCASE.LANG.md` (e.g., README.ru.md)
- **Encoding**: UTF-8
- **Line endings**: LF (Unix-style)
- **Automatically converted** to HTML by GitHub Actions

#### HTML Files (Generated)
- **Auto-generated** from markdown files
- **Located**: `docs/doc/` directory on GitHub Pages
- **Updated**: Every deployment
- **Not** stored in git repository

## How to Contribute Documentation

1. **Edit markdown files** in this directory
2. **Use proper formatting** (see examples in existing files)
3. **Link to other docs** using relative paths: `[Link](FILENAME.md)`
4. **Add translations** if you speak other languages (append `.LANG` to filename)
5. **Test locally** (if using conversion scripts)
6. **Push to main** - GitHub Actions will auto-generate HTML

### Markdown Guidelines

```markdown
# Main Title (H1)
Use for page title only.

## Section Title (H2)
Use for major sections.

### Subsection Title (H3)
Use for subsections.

**Bold text** for emphasis
*Italic text* for definitions

- Bullet lists
- For multiple items

1. Numbered lists
2. For procedures

`inline code` for commands
\`\`\`
code block
for examples
\`\`\`

> Blockquotes
> for tips and warnings

[Link text](URL or FILENAME.md)
```

## Maintenance

### Regular Updates
- Update documentation when releasing new versions
- Keep screenshots up-to-date
- Review and fix broken links (quarterly)
- Update installation instructions when needed

### Automated Updates
- HTML pages generated automatically via GitHub Actions
- No manual HTML editing needed
- Just update .md files

### Quality Checklist
- [ ] Spell checked
- [ ] Links verified
- [ ] Code examples tested
- [ ] Screenshots current
- [ ] Translated to all languages

## Report Directory

The `report/` subdirectory contains deployment and progress reports:
- `IMPLEMENTATION_COMPLETE.md` - Completion status
- `2026-01-11-github-pages-deployment-update.md` - Latest deployment notes
- Other dated reports from various updates

## Support

### Finding Information
1. Use **Ctrl+F** to search this page
2. Check **[QUICKSTART.md](QUICKSTART.md)** for common questions
3. See **[CONTRIBUTING.md](CONTRIBUTING.md)** for development help
4. Read **[README.md](README.md)** for comprehensive overview

### Getting Help
- **Issues**: GitHub Issues page
- **Questions**: GitHub Discussions (if enabled)
- **Bugs**: Include error output and steps to reproduce

## Languages Supported

Documentation is available in:
- 🇺🇸 **English** (`.md` files without lang suffix)
- 🇷🇺 **Russian** (`.ru.md` files)

More languages welcome! To add:
1. Copy `.md` file
2. Append `.LANG` code (e.g., `.es.md` for Spanish)
3. Translate content
4. Test formatting
5. Submit pull request

## Version Information

This documentation is for **Kodi Play Random** project.

Current version information available in:
- `VERSION_UPDATE.md`
- `RELEASE_NOTES.md`
- Main `README.md`

Generated: 2026-01-11
Last Updated: 2026-01-11

---

**Happy learning!** 🚀

For the latest updates, visit: https://github.com/seranov/seranov-kodi

