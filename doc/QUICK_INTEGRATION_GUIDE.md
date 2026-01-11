# Quick Integration Guide

## For GitHub Actions Workflow

The deployment workflow is fully configured in `.github/workflows/publish-release.yml`.

### Trigger Events

The workflow automatically runs on:

```yaml
on:
  push:
    branches:
      - main          # Any push to main branch
    tags:
      - 'v*'         # Any version tag (v1.0.0, v1.1.0, etc.)
  workflow_dispatch:  # Manual trigger from GitHub Actions tab
```

### Required Repository Settings

1. **GitHub Pages Configuration**
   - Branch: `gh-pages`
   - Source: `/` (root)
   - Enforce HTTPS: Yes (recommended)

2. **Permissions**
   - Actions: Read and write permissions (for gh-pages deployment)
   - Contents: Read access (for workflow)

### How It Works

```
1. Push to main or tag
    ↓
2. GitHub Actions workflow starts
    ↓
3. Checkout repository code
    ↓
4. Create addon ZIP archives
    ↓
5. Generate addons.xml metadata
    ↓
6. Convert .md files to .html
    ↓
7. Generate readme.html
    ↓
8. Deploy to gh-pages branch
    ↓
9. GitHub Pages serves the site
```

## For Local Development

### Create Test Addon

```bash
mkdir -p test-addon
cd test-addon

# Create addon structure
cat > addon.xml << 'EOF'
<?xml version='1.0' encoding='utf-8'?>
<addon id="plugin.test" name="Test Addon" version="1.0.0" provider-name="test">
    <requires>
        <import addon="xbmc.python" version="3.0.0" />
    </requires>
    <extension point="xbmc.python.pluginsource" library="main.py">
        <provides>video</provides>
    </extension>
    <extension point="xbmc.addon.metadata">
        <summary lang="en_GB">A test addon</summary>
        <description lang="en_GB">This is a test addon for development</description>
        <language />
        <platform>all</platform>
        <license>MIT</license>
        <website>https://github.com/your-repo</website>
        <email>your@email.com</email>
        <assets>
            <icon>icon.png</icon>
        </assets>
    </extension>
</addon>
EOF

# Create main.py
echo "# Test addon" > main.py

# Create icon
wget -O icon.png https://via.placeholder.com/256x256?text=Test
```

### Test Scripts Locally

```bash
# 1. Test Markdown conversion
python3 scripts/convert_md_to_html.py doc test_docs/doc

# 2. Test readme generation
python3 scripts/generate_readme.py test_docs

# 3. View generated files
open test_docs/readme.html  # macOS
xdg-open test_docs/readme.html  # Linux
start test_docs/readme.html  # Windows
```

### Simulate Full Deployment

```bash
#!/bin/bash
set -e

# Create output directory
mkdir -p docs/doc

# Create test addon ZIP
mkdir -p docs/plugin.test
cp test-addon/addon.xml docs/plugin.test/
cp test-addon/icon.png docs/plugin.test/
cd docs/plugin.test
zip -r plugin.test-1.0.0.zip addon.xml icon.png
cd ../..

# Generate files
python3 scripts/convert_md_to_html.py doc docs/doc
python3 scripts/generate_readme.py docs
touch docs/.nojekyll

# View result
echo "Generated files:"
find docs -type f -name "*.html" -o -name "*.xml" -o -name "*.md5"

# Open in browser
open docs/readme.html
```

## For First-Time Setup

### 1. Enable GitHub Pages

```bash
# Go to: Settings → Pages
# Source: GitHub Actions (or branch: gh-pages)
```

### 2. Verify Workflow Permissions

```bash
# Go to: Settings → Actions → General
# Workflow permissions: Read and write permissions
```

### 3. Run Workflow

```bash
# Push to main or manually trigger:
# Actions tab → Publish Kodi Repository → Run workflow
```

### 4. Check Results

```bash
# Wait 1-2 minutes for deployment
# Visit: https://username.github.io/repo-name/readme.html
```

## Common Issues

### Issue: Workflow fails with "No addons found"

**Cause:** Addon directories not named correctly or no addon.xml files

**Solution:**
```bash
# Ensure addon directories exist and match patterns:
ls -d plugin.* service.* context.* repository.* 2>/dev/null || echo "No addons found"

# Ensure addon.xml exists:
find . -name "addon.xml" | head -5
```

### Issue: Documentation not converted

**Cause:** Python markdown library not available

**Solution:** 
The script has a fallback, so it will still work but with basic formatting. To use advanced formatting:

```bash
pip install markdown
```

### Issue: Pages not deploying

**Cause:** GitHub Pages not configured properly

**Solution:**
1. Check Settings → Pages
2. Ensure branch is `gh-pages`
3. Verify source is `/` (root)
4. Check Actions logs for errors

### Issue: addon.xml not parsing

**Cause:** Invalid XML format

**Solution:**
```bash
# Validate XML:
python3 -m xml.dom.minidom plugin.test/addon.xml

# Or use online validator:
# https://www.xmlvalidation.com/
```

## Customization

### Change Repository Colors

Edit `scripts/generate_readme.py`, find:

```python
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Change hex colors to your preference.

### Add Custom Sections to readme.html

Edit the HTML template in `create_html_content()` function in `scripts/generate_readme.py`:

```python
<div class="custom-section">
    <h2>Custom Title</h2>
    <p>Custom content here</p>
</div>
```

### Modify Documentation Template

Edit `create_html_template()` in `scripts/convert_md_to_html.py` to change styling or layout.

## Performance Tips

### Reduce ZIP File Sizes

```bash
# Exclude unnecessary files
cat > .zipignore << 'EOF'
*.pyc
__pycache__
.git
.github
.idea
*.md
EOF

# Update create_addon_zip function to use it
```

### Cache Generated Files

GitHub Actions automatically caches installed packages. For faster builds:

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

### Monitor Workflow Performance

Check Actions tab → Workflow runs → Click run → Timing section

## Monitoring & Maintenance

### Regular Tasks

- [ ] Monitor workflow runs (weekly)
- [ ] Check for broken addon links (monthly)
- [ ] Update addon versions when releasing (before push)
- [ ] Validate addon.xml files before release
- [ ] Test local builds before pushing to main

### Watch for Errors

GitHub will email on workflow failures. Check:

1. Actions tab
2. Workflow logs
3. GitHub Status page

### Analytics

To track usage:
- Enable GitHub Insights
- Monitor release download counts
- Check Pages traffic (Settings → Pages)

## Integration with Other Tools

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Validate all addon.xml files
for addon_xml in */addon.xml; do
    python3 -m xml.dom.minidom "$addon_xml" > /dev/null || {
        echo "Invalid XML: $addon_xml"
        exit 1
    }
done

exit 0
```

### Local GitHub Actions Testing

```bash
# Install act: https://github.com/nektos/act
act -j build-and-deploy

# Or simulate with Docker:
docker run --rm -v ~/.ssh:/root/.ssh -v $PWD:/workspace \
    --workdir /workspace \
    ubuntu:latest bash -c "
        apt-get update && apt-get install -y python3
        python3 scripts/generate_readme.py docs
    "
```

### CI/CD Pipeline Integration

For other CI/CD systems (GitLab CI, Jenkins, etc.):

```bash
# Run the same steps as GitHub Actions
python3 scripts/convert_md_to_html.py doc docs/doc
python3 scripts/generate_readme.py docs
touch docs/.nojekyll

# Then deploy docs/ directory to your hosting
```

## Troubleshooting Checklist

- [ ] addon.xml files are valid XML
- [ ] Addon directory names match expected patterns
- [ ] .md files exist in `/doc` directory
- [ ] Python 3.9+ is being used
- [ ] GitHub Pages is enabled and configured
- [ ] Workflow permissions are set to "read and write"
- [ ] No sensitive data in addon.xml or .md files
- [ ] All external links in documentation are valid
- [ ] File permissions allow read/write in docs directory
- [ ] GitHub Actions log shows no Python errors

## Getting Help

1. Check workflow logs in Actions tab
2. Review generated files in gh-pages branch
3. Validate HTML at https://validator.w3.org/
4. Open issue with:
   - Workflow log excerpt
   - Screenshot of error
   - Steps to reproduce
   - Output of `find . -name "addon.xml"`

## Success Indicators

✅ Workflow completed successfully (green checkmark)
✅ readme.html displays addon cards
✅ Download links work
✅ Documentation links work
✅ Can add repository to Kodi
✅ addons.xml.md5 checksum valid

Everything else is extra polish!

