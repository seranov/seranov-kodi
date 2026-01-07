# GitHub Release Guide

> **Note:** This repository now uses automated GitHub Pages deployment!  
> For detailed build and publish instructions, see [BUILD_AND_PUBLISH.md](BUILD_AND_PUBLISH.md)

## Quick Release Process

### Automated Process (Recommended)

The repository automatically builds and deploys to GitHub Pages on every push to `main`:

1. **Update version numbers** in `addon.xml` files
2. **Update documentation** (RELEASE_NOTES.md, etc.)
3. **Commit and push** to `main` branch
4. **GitHub Actions automatically:**
   - Builds all ZIP archives
   - Generates addons.xml and checksums
   - Deploys to GitHub Pages
   - Makes updates available to Kodi users

**That's it!** No manual steps needed.

### Repository URL

**Live Repository:** `https://seranov.github.io/seranov-kodi/`

Users can:
- ✅ Install repository once from ZIP file
- ✅ Get automatic updates through Kodi
- ✅ No manual downloads needed for updates

---

## Creating GitHub Release (Optional)

While not required for Kodi functionality, GitHub Releases provide better visibility:

### Step 1: Create Git Tag

```bash
git checkout main
git pull origin main
git tag -a v1.0.1 -m "Release v1.0.1 - Description"
git push origin v1.0.1
```

### Step 2: Create GitHub Release

1. **Go to:** https://github.com/seranov/seranov-kodi/releases/new

2. **Fill in details:**
   - **Tag:** Select `v1.0.1` (or create new)
   - **Target:** `main` branch
   - **Title:** `v1.0.1 - Release Name`
   - **Description:** Copy from `RELEASE_NOTES.md`

3. **Attach files (optional):**
   - `repository.seranov-1.0.0.zip` (for easy download)
   - Other add-on ZIPs if needed

4. **Publish Release**

### Step 3: Verify

- ✅ Release page loads correctly
- ✅ Files are downloadable
- ✅ GitHub Pages is updated (check `https://seranov.github.io/seranov-kodi/addons.xml`)

---

## Manual Release (Fallback)

If automated deployment fails, see [BUILD_AND_PUBLISH.md](BUILD_AND_PUBLISH.md) for manual deployment instructions.


---


## Documentation

For complete instructions on:
- Building the repository locally
- Understanding the CI/CD pipeline
- Troubleshooting deployment issues
- Manual deployment procedures

**See:** [BUILD_AND_PUBLISH.md](BUILD_AND_PUBLISH.md)

---

## Files and Structure

### Repository Files

All add-ons are automatically packaged and deployed:

- `repository.seranov-1.0.0.zip` - Repository installation file
- `plugin.video.random.recursive-1.0.0.zip` - Random player
- `plugin.video.unified.browser-1.0.0.zip` - Unified browser
- `context.screenshots-1.0.5.zip` - Screenshots context menu
- `service.seranov.nfoscanner-1.0.0.zip` - NFO scanner service
- `addons.xml` - Repository metadata
- `addons.xml.md5` - Checksum

### Key Documentation Files

- ✅ [RELEASE_NOTES.md](RELEASE_NOTES.md) - Release notes (bilingual)
- ✅ [INSTALLATION.md](INSTALLATION.md) - Installation guide (bilingual)
- ✅ [BUILD_AND_PUBLISH.md](BUILD_AND_PUBLISH.md) - Build & deployment guide
- ✅ [README.md](../README.md) - Main repository documentation

---

## Installation Instructions for Users

### Method 1: Install Repository (Recommended)

1. Download: `repository.seranov-1.0.0.zip`
2. In Kodi: **Add-ons** → **Install from zip file**
3. Select the downloaded file
4. Install add-ons from: **Install from repository** → **Seranov's Kodi Repository**

### Method 2: Direct Installation

Download and install individual add-on ZIPs directly.

**Note:** Without repository, users won't get automatic updates.

---

## Monitoring and Verification

### Check Deployment Status

1. **GitHub Actions:** https://github.com/seranov/seranov-kodi/actions
2. **GitHub Pages:** https://seranov.github.io/seranov-kodi/
3. **addons.xml:** https://seranov.github.io/seranov-kodi/addons.xml

### Test in Kodi

1. Install repository from ZIP
2. Right-click → **Check for updates**
3. Verify correct version appears

---

## Support

- **Documentation:** [doc/](../doc/)
- **Issues:** https://github.com/seranov/seranov-kodi/issues
- **Email:** seranov@yandex.ru
- ✅ `addons.xml` - Repository metadata (with Russian translations)
- ✅ `addons.xml.md5` - Checksum file

### Git Tag
- ✅ `v1.0.0` - Created locally (needs to be pushed after merge)

---

## Post-Release Tasks

After the release is created, consider:

1. **Announce the release:**
   - Create a post on Kodi forums (if applicable)
   - Share on social media
   - Update any external documentation

2. **Test installation:**
   - Install the repository in a fresh Kodi instance
   - Verify all add-ons install correctly
   - Test basic functionality

3. **Monitor feedback:**
   - Watch for GitHub issues
   - Check email for user questions
   - Be ready to create patch releases if needed

---

## Future Releases

For future releases, follow this workflow:

1. **Update version numbers:**
   - Edit `addon.xml` in the relevant add-on directory
   - Update version in README if needed

2. **Rebuild repository:**
   ```bash
   python3 scripts/generate_repo.py
   ```

3. **Create release notes:**
   - Document changes since last release
   - Follow the format in `RELEASE_NOTES.md`

4. **Tag and release:**
   - Create new tag (e.g., `v1.1.0`)
   - Upload updated zip files
   - Publish release notes

---

## Troubleshooting

### If tag creation fails:
```bash
# Delete local tag and recreate
git tag -d v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0 - Initial Kodi Repository Release"
git push origin v1.0.0
```

### If release upload fails:
- Check file sizes (GitHub has 2GB limit per file)
- Verify you have release creation permissions
- Try uploading files one at a time

### If users report installation issues:
1. Verify the zip files are not corrupted
2. Check that the repository URL in `repository.seranov/addon.xml` is correct
3. Ensure `addons.xml` and `addons.xml.md5` are accessible via the raw GitHub URL

---

## Contact

For questions about this release process:
- **Email:** seranov@yandex.ru
- **GitHub:** https://github.com/seranov/seranov-kodi/issues
