# GitHub Release Creation Guide

## Instructions for Creating the v1.0.0 Release

Since automated release creation requires special permissions, please follow these steps to manually create the GitHub release:

### Step 1: Merge the Pull Request

1. Go to https://github.com/seranov/kodi-play-random/pulls
2. Find the pull request for this branch: `copilot/create-release-for-kodi`
3. Review and merge the pull request into `main` branch

### Step 2: Create Git Tag

After merging, create the git tag from the `main` branch:

```bash
git checkout main
git pull origin main
git tag -a v1.0.0 -m "Release v1.0.0 - Initial Kodi Repository Release"
git push origin v1.0.0
```

### Step 3: Create GitHub Release

1. **Go to GitHub Releases page:**
   - Navigate to: https://github.com/seranov/kodi-play-random/releases/new

2. **Fill in Release Details:**
   - **Tag version:** Select `v1.0.0` (or create it from the dropdown if not already created)
   - **Target:** `main` branch
   - **Release title:** `v1.0.0 - Initial Release`
   - **Description:** Copy the content from `RELEASE_NOTES.md` file

3. **Upload Release Assets:**
   
   Upload the following files from the `repo/` directory:
   
   - ✅ `repository.seranov-1.0.0.zip` (Primary installation file)
   - ✅ `plugin.video.random.recursive-1.0.0.zip`
   - ✅ `plugin.video.unified.browser-1.0.0.zip`
   - ✅ `context.screenshots-1.0.5.zip`
   - ✅ `service.seranov.nfoscanner-1.0.0.zip`
   - ✅ `addons.xml`
   - ✅ `addons.xml.md5`

4. **Release Options:**
   - ✅ Check "Set as the latest release"
   - ✅ Do NOT check "Set as a pre-release" (this is a stable release)

5. **Publish Release:**
   - Click **Publish release**

### Step 4: Verify Release

After creating the release, verify:

1. **Release page loads correctly:**
   - https://github.com/seranov/kodi-play-random/releases/latest

2. **All assets are downloadable:**
   - Test downloading `repository.seranov-1.0.0.zip`
   - Verify file size and integrity

3. **Release notes are formatted correctly:**
   - Check that bilingual content displays properly
   - Verify all links work

### Step 5: Update README (Optional)

Consider adding a prominent installation section at the top of README.md:

```markdown
## 🚀 Quick Installation

Download and install the repository to get automatic updates:

1. **Download:** [repository.seranov-1.0.0.zip](https://github.com/seranov/kodi-play-random/releases/latest)
2. **Install in Kodi:** Add-ons → Install from zip file
3. **Browse add-ons:** Install from repository → Seranov's Kodi Repository

See [INSTALLATION.md](INSTALLATION.md) for detailed instructions.
```

---

## Files Prepared for Release

All necessary files are ready in the repository:

### Documentation
- ✅ `RELEASE_NOTES.md` - Complete release notes (English & Russian)
- ✅ `INSTALLATION.md` - Detailed installation guide (English & Russian)
- ✅ `README.md` - Repository documentation (already exists)

### Repository Files (in `repo/` directory)
- ✅ `repository.seranov-1.0.0.zip` - Repository add-on
- ✅ `plugin.video.random.recursive-1.0.0.zip` - Random player add-on
- ✅ `plugin.video.unified.browser-1.0.0.zip` - Unified browser add-on
- ✅ `context.screenshots-1.0.5.zip` - Screenshots add-on
- ✅ `service.seranov.nfoscanner-1.0.0.zip` - NFO scanner service
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
- **GitHub:** https://github.com/seranov/kodi-play-random/issues
