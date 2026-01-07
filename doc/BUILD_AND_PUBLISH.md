# Build and Publish Guide

> [Русская версия / Russian version](BUILD_AND_PUBLISH.ru.md)

This guide explains how to build and publish releases of the Kodi repository with automatic deployment to GitHub Pages.

## Overview

The repository uses an automated CI/CD pipeline that:
- ✅ Builds ZIP archives for all add-ons
- ✅ Generates `addons.xml` and `addons.xml.md5`
- ✅ Deploys to GitHub Pages automatically
- ✅ Enables automatic updates in Kodi

**Repository URL:** `https://seranov.github.io/seranov-kodi/`

---

## Local Build (Testing)

### Prerequisites

- Python 3.9 or later
- PowerShell (Windows) or Bash (Linux/Mac)
- Git

### Build Repository Locally

#### Windows (PowerShell)

```powershell
# Navigate to repository root
cd C:\prj\seranov-kodi

# Run build script
.\scripts\build-release.ps1
```

**Build Options:**

```powershell
# Build with specific version
.\scripts\build-release.ps1 -Version "1.0.1"

# Skip build, just show info
.\scripts\build-release.ps1 -SkipBuild

# Create git tag
.\scripts\build-release.ps1 -CreateGitTag
```

#### Linux/Mac (Bash)

```bash
# Navigate to repository root
cd ~/seranov-kodi

# Run Python generator directly
python3 scripts/generate_repo.py
```

### What Gets Built

After running the build, the `repo/` directory will contain:

```
repo/
├── addons.xml              # Repository metadata
├── addons.xml.md5          # Checksum file
├── context.screenshots/
│   ├── context.screenshots-1.0.5.zip
│   └── icon.png
├── plugin.video.random.recursive/
│   ├── plugin.video.random.recursive-1.0.0.zip
│   └── icon.png
├── plugin.video.unified.browser/
│   ├── plugin.video.unified.browser-1.0.0.zip
│   └── icon.png
├── repository.seranov/
│   ├── repository.seranov-1.0.0.zip
│   └── icon.png
└── service.seranov.nfoscanner/
    ├── service.seranov.nfoscanner-1.0.0.zip
    └── icon.png
```

---

## Automated GitHub Pages Deployment

### How It Works

The repository uses **GitHub Actions** to automatically build and deploy on every push to `main`:

1. **Trigger:** Push to `main` branch or tag starting with `v*`
2. **Build:** Creates all ZIP archives and metadata files
3. **Deploy:** Publishes to `gh-pages` branch
4. **Available:** Files are served via `https://seranov.github.io/seranov-kodi/`

### Workflow File

`.github/workflows/publish-release.yml`

**Key Features:**
- ✅ Python 3.9+ for modern Path APIs
- ✅ Creates ZIP archives for all add-ons
- ✅ Generates `addons.xml` with proper indentation
- ✅ Calculates MD5 checksums
- ✅ Deploys to GitHub Pages (`gh-pages` branch)
- ✅ Creates `.nojekyll` to prevent Jekyll processing

### Monitoring Deployments

1. **View GitHub Actions:**
   - Go to: https://github.com/seranov/seranov-kodi/actions
   - Check workflow status: **Publish Kodi Repository**

2. **Check gh-pages branch:**
   - Go to: https://github.com/seranov/seranov-kodi/tree/gh-pages
   - Verify files are present

3. **Test Repository URL:**
   - Visit: https://seranov.github.io/seranov-kodi/addons.xml
   - Should display XML content

---

## Publishing a New Release

### Step 1: Update Version Numbers

Update version in relevant `addon.xml` files:

**Example:** Update `plugin.video.random.recursive/addon.xml`
```xml
<addon id="plugin.video.random.recursive" version="1.0.1" ...>
```

**Files to check:**
- `plugin.video.random.recursive/addon.xml`
- `plugin.video.unified.browser/addon.xml`
- `context.screenshots/addon.xml`
- `service.seranov.nfoscanner/addon.xml`
- `repository.seranov/addon.xml` (if repository version changes)

### Step 2: Update Changelog

Add changes to changelog files:
- `doc/RELEASE_NOTES.md`
- Individual add-on changelogs (if any)

### Step 3: Commit and Push

```bash
# Add changes
git add .

# Commit with descriptive message
git commit -m "Release version 1.0.1

- Updated plugin.video.random.recursive to 1.0.1
- Fixed playback issues
- Added new features"

# Push to main
git push origin main
```

### Step 4: Create Git Tag (Optional)

```bash
# Create annotated tag
git tag -a v1.0.1 -m "Release version 1.0.1"

# Push tag
git push origin v1.0.1
```

### Step 5: Wait for Deployment

1. **GitHub Actions runs automatically** after push
2. **Monitor progress** at: https://github.com/seranov/seranov-kodi/actions
3. **Deployment takes ~1-2 minutes**
4. **Check GitHub Pages** is updated

### Step 6: Verify Deployment

```bash
# Check addons.xml is updated
curl https://seranov.github.io/seranov-kodi/addons.xml

# Check specific add-on ZIP exists
curl -I https://seranov.github.io/seranov-kodi/plugin.video.random.recursive/plugin.video.random.recursive-1.0.1.zip
```

### Step 7: Test in Kodi

1. Open Kodi
2. Go to **Add-ons** → **Seranov's Kodi Repository**
3. Right-click → **Check for updates**
4. Verify new version appears

---

## Creating GitHub Releases (Optional)

While GitHub Pages handles automatic updates, you can still create GitHub Releases for better visibility:

### Step 1: Go to Releases

Visit: https://github.com/seranov/seranov-kodi/releases/new

### Step 2: Fill Release Form

- **Tag version:** `v1.0.1` (select existing or create new)
- **Target:** `main`
- **Release title:** `v1.0.1 - Feature Update`
- **Description:** Copy from `RELEASE_NOTES.md`

### Step 3: Attach Files (Optional)

Upload key files from `repo/` directory:
- `repository.seranov-1.0.0.zip` (main installation file)
- Updated add-on ZIPs

### Step 4: Publish Release

Click **Publish release**

---

## GitHub Pages Configuration

### Initial Setup (Already Done)

The repository is configured with:

1. **GitHub Pages Settings:**
   - Source: `gh-pages` branch
   - Custom domain: None
   - URL: `https://seranov.github.io/seranov-kodi/`

2. **Repository Settings:**
   - Workflow permissions: Read and write
   - Pages enabled

### Verifying Configuration

1. Go to: https://github.com/seranov/seranov-kodi/settings/pages
2. Check:
   - ✅ Source: Deploy from branch `gh-pages`
   - ✅ Branch: `gh-pages` / `root`
   - ✅ Status: **Your site is live at https://seranov.github.io/seranov-kodi/**

---

## Troubleshooting

### Deployment Fails

**Check GitHub Actions logs:**
1. Go to: https://github.com/seranov/seranov-kodi/actions
2. Click on failed workflow
3. Review error messages

**Common issues:**
- Missing `addon.xml` files
- Invalid XML syntax
- Python version mismatch (needs 3.9+)

### GitHub Pages Not Updating

**Solutions:**
1. **Check gh-pages branch exists:**
   - https://github.com/seranov/seranov-kodi/tree/gh-pages

2. **Clear GitHub Pages cache:**
   - Wait 5-10 minutes for CDN propagation
   - Try in incognito/private browser window

3. **Check workflow permissions:**
   - Settings → Actions → General → Workflow permissions
   - Should be: **Read and write permissions**

### Kodi Not Detecting Updates

**Solutions:**
1. **Force update check:**
   - Right-click on repository → Check for updates

2. **Verify addons.xml:**
   - Visit: https://seranov.github.io/seranov-kodi/addons.xml
   - Verify version numbers are correct

3. **Check Kodi log:**
   - Look for repository update errors
   - Windows: `%APPDATA%\Kodi\kodi.log`

---

## Advanced: Manual Deployment

If automated deployment fails, you can deploy manually:

### Step 1: Build Locally

```powershell
# Build repository
.\scripts\build-release.ps1
```

### Step 2: Copy to docs/ Directory

```powershell
# Copy repo contents to docs/
Copy-Item -Path repo\* -Destination docs\ -Recurse -Force
```

### Step 3: Commit and Push

```bash
git add docs/
git commit -m "Manual deployment"
git push origin main
```

### Step 4: Deploy to gh-pages

```bash
# Using subtree push
git subtree push --prefix docs origin gh-pages

# Or force push if needed
git push origin `git subtree split --prefix docs main`:gh-pages --force
```

---

## File Structure Reference

### Source Files (in repository root)

```
plugin.video.random.recursive/
  addon.xml              # Version: 1.0.0
  main.py
  resources/...

context.screenshots/
  addon.xml              # Version: 1.0.5
  addon.py
  resources/...

repository.seranov/
  addon.xml              # Version: 1.0.0
  icon.png

scripts/
  build-release.ps1      # Windows build script
  generate_repo.py       # Python generator
  deploy-local.ps1       # Local deployment
```

### Generated Files (in repo/ and docs/)

```
repo/                    # Local build output
docs/                    # GitHub Pages content (deployed to gh-pages)
  addons.xml
  addons.xml.md5
  .nojekyll
  context.screenshots/
    context.screenshots-1.0.5.zip
    icon.png
  plugin.video.random.recursive/
    plugin.video.random.recursive-1.0.0.zip
    icon.png
  ...
```

---

## Best Practices

### Version Numbering

Follow Semantic Versioning: `MAJOR.MINOR.PATCH`

- **MAJOR:** Breaking changes
- **MINOR:** New features, backward compatible
- **PATCH:** Bug fixes

### Commit Messages

Use clear, descriptive commit messages:

```
✅ Good:
Release version 1.0.1 - Fix video playback

❌ Bad:
update
fix
changes
```

### Testing Before Release

1. **Build locally first:**
   ```powershell
   .\scripts\build-release.ps1
   ```

2. **Test ZIP installation in Kodi:**
   - Install from `repo/*.zip` files
   - Verify add-ons work correctly

3. **Check metadata:**
   - Open `repo/addons.xml`
   - Verify all versions and dependencies

### Documentation

Always update:
- ✅ `RELEASE_NOTES.md` - User-facing changes
- ✅ `addon.xml` - Version numbers
- ✅ Changelog sections

---

## Resources

### Documentation
- [Installation Guide](INSTALLATION.md)
- [Release Notes](RELEASE_NOTES.md)
- [Contributing Guide](CONTRIBUTING.md)

### Scripts
- `scripts/build-release.ps1` - Windows build and release
- `scripts/generate_repo.py` - Python repository generator
- `scripts/deploy-local.ps1` - Local Kodi deployment

### External Links
- [Kodi Add-on Development](https://kodi.wiki/view/Add-on_development)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## Support

If you encounter issues:

1. **Check documentation:** [doc/](../doc/)
2. **GitHub Issues:** [github.com/seranov/seranov-kodi/issues](https://github.com/seranov/seranov-kodi/issues)
3. **Email:** seranov@yandex.ru

---

**Last Updated:** 2026-01-07

