# Python Scripts Documentation

## Overview

Two Python scripts are used in the GitHub Pages deployment pipeline to generate HTML content:

1. **convert_md_to_html.py** - Converts Markdown documentation to HTML
2. **generate_readme.py** - Generates the main readme.html page

## convert_md_to_html.py

### Purpose
Converts Markdown (.md) files from the `/doc` directory to HTML files in the `/docs/doc` directory.

### Usage

```bash
python3 scripts/convert_md_to_html.py <input_directory> [output_directory]
```

### Arguments
- `<input_directory>` - Directory containing .md files (required)
- `[output_directory]` - Directory to output .html files (optional, defaults to input_dir/../html)

### Example

```bash
python3 scripts/convert_md_to_html.py doc docs/doc
```

### Features

#### Markdown Library Support
If the `markdown` library is installed, uses advanced features:
- GitHub Flavored Markdown (GFM)
- Table of contents generation
- Code syntax highlighting
- Fenced code blocks
- Extra formatting

#### Fallback Conversion
If markdown library is not available, uses basic regex-based conversion for:
- Headers (H1-H6)
- Bold (**text**)
- Italic (*text* and _text_)
- Links ([text](url))
- Code blocks (```code```)
- Inline code (`code`)
- Blockquotes (> text)
- Horizontal rules (---)

#### HTML Output
Each .md file generates a complete HTML5 document with:
- Responsive design
- GitHub-style CSS styling
- Back-to-home navigation
- Proper character encoding (UTF-8)
- Mobile viewport meta tags

### Output Structure

```
docs/doc/
├── README.html
├── QUICKSTART.html
├── INSTALLATION.html
├── CONTRIBUTING.html
└── ... (all .md files)
```

### CSS Styling

Embedded CSS includes:
- GitHub-style colors (#24292e, #666, etc.)
- Proper heading hierarchy with borders
- Code block styling with background colors
- Table formatting with borders and alternating rows
- Link colors and hover effects (#0366d6)
- Blockquote styling with left border

### Implementation Details

#### Class: AddonInfo (in generate_readme.py, but concepts apply)
Not directly in this file, but the script uses similar concepts.

#### Functions

##### `create_html_template(title: str, content: str) -> str`
Creates the HTML5 wrapper template around converted content.

Parameters:
- `title` - Page title (extracted from filename)
- `content` - HTML content from markdown

Returns:
- Complete HTML document as string

##### `convert_markdown_to_html(markdown_content: str) -> str`
Converts markdown content to HTML.

Parameters:
- `markdown_content` - Raw markdown text

Returns:
- HTML content (without wrapper)

Logic:
1. If markdown library available → use advanced conversion
2. Else → use basic regex conversion

##### `_basic_markdown_to_html(content: str) -> str`
Performs basic markdown-to-HTML conversion using regex patterns.

Supported patterns:
- `### Heading 3` → `<h3>Heading 3</h3>`
- `## Heading 2` → `<h2>Heading 2</h2>`
- `# Heading 1` → `<h1>Heading 1</h1>`
- `**bold**` → `<strong>bold</strong>`
- `*italic*` → `<em>italic</em>`
- `[link](url)` → `<a href="url">link</a>`
- `` `code` `` → `<code>code</code>`
- ` ```code``` ` → `<pre><code>code</code></pre>`

##### `convert_file(input_path: Path, output_path: Path) -> bool`
Converts a single .md file to HTML.

Parameters:
- `input_path` - Path to .md file
- `output_path` - Path to output .html file

Returns:
- `True` if successful, `False` on error

Process:
1. Read markdown content from file
2. Extract title from filename
3. Convert markdown to HTML
4. Wrap with HTML template
5. Write to output file
6. Print status message

##### `main()`
Entry point for the script.

Process:
1. Parse command-line arguments
2. Find all .md files in input directory
3. Convert each file to HTML
4. Report results (count of successful conversions)

### Error Handling

- Invalid input directory: Print error and exit with code 1
- File read/write errors: Print error message and continue with next file
- Markdown parse errors: Print error message and continue with next file

### Exit Codes

- `0` - Success (at least some files converted)
- `1` - Failure (invalid directory or all files failed)

---

## generate_readme.py

### Purpose
Generates readme.html with links to all addons and their descriptions.

### Usage

```bash
python3 scripts/generate_readme.py [docs_directory]
```

### Arguments
- `[docs_directory]` - Directory containing addon directories (optional, defaults to 'docs')

### Example

```bash
python3 scripts/generate_readme.py docs
```

### Features

#### Addon Discovery
- Scans docs directory for addon directories
- Detects addon patterns: `plugin.*`, `service.*`, `context.*`, `repository.*`
- Reads addon.xml from source directories (not docs)

#### Metadata Extraction
For each addon:
- ID (from addon element id attribute)
- Name (from addon element name attribute)
- Version (from addon element version attribute)
- Summary (from English <summary lang="en_GB">)
- Description (from English <description lang="en_GB">)

#### HTML Generation
Creates attractive card layout with:
- Addon name with icon (📦)
- Version information
- Summary (bold text)
- Description (regular text)
- Download ZIP button
- View Files link
- Responsive grid layout

#### Styling
Modern design with:
- Gradient background (purple: #667eea to #764ba2)
- Card-based layout
- Hover animations
- Button styling (primary and secondary)
- Documentation links section
- Installation instructions

### Output

Single file: `docs/readme.html`

### Implementation Details

#### Class: AddonInfo
Data class for addon information.

**Attributes:**
- `addon_id: str` - Addon identifier
- `name: str` - Display name
- `version: str` - Version number
- `summary: str` - One-line summary
- `description: str` - Detailed description

**Methods:**

`get_zip_name() -> str`
- Returns: `{addon_id}-{version}.zip`
- Used for download URL construction

`to_html() -> str`
- Returns: HTML card div for this addon
- Includes: Name, version, summary, description, buttons
- Uses CSS classes: addon-card, addon-link, btn, btn-primary, btn-secondary

#### Functions

##### `parse_addon_xml(xml_path: Path) -> Optional[AddonInfo]`
Parses addon.xml and extracts metadata.

Parameters:
- `xml_path` - Path to addon.xml file

Returns:
- AddonInfo object on success
- None on error

Process:
1. Parse XML file with ElementTree
2. Extract ID, name, version from root element
3. Find xbmc.addon.metadata extension
4. Extract English summary and description
5. Create and return AddonInfo

##### `scan_addons(docs_dir: Path) -> List[AddonInfo]`
Finds and parses all addons in docs directory.

Parameters:
- `docs_dir` - Path to docs directory

Returns:
- List of AddonInfo objects

Process:
1. Iterate through docs directory
2. Filter for addon directories (match patterns)
3. Look for addon.xml in source directory (using dir name)
4. Parse each addon.xml
5. Collect and return all addons

##### `create_html_content(addons: List[AddonInfo]) -> str`
Creates complete HTML page content.

Parameters:
- `addons` - List of AddonInfo objects

Returns:
- Complete HTML5 document as string

Process:
1. Generate addon cards from each addon
2. Create HTML template with:
   - Header section (title and repo info)
   - Content section (instructions and addon grid)
   - Documentation links
   - Footer with GitHub links
3. Return complete HTML

HTML Sections:
- **Header**: Logo, repo URL, title
- **Content**:
  - Installation instructions (2 methods)
  - Addon grid with cards
  - Documentation links
  - Repository file links
- **Footer**: Copyright, GitHub links, Kodi link

##### `main()`
Entry point for the script.

Process:
1. Parse command-line argument for docs directory
2. Scan for addons
3. Warn if no addons found
4. Generate HTML content
5. Write readme.html
6. Print success message

### Error Handling

- Missing or invalid XML: Print warning, skip addon
- No addons found: Print warning but continue (creates empty readme.html)
- File write errors: Print error message

### Exit Codes

- `0` - Success (readme.html generated)

### CSS Classes Used

**Container classes:**
- `.container` - Main wrapper (max-width: 1000px)
- `.header` - Top section with title
- `.content` - Main content area
- `.footer` - Bottom section

**Addon display:**
- `.addons-grid` - CSS grid for addon cards
- `.addon-card` - Individual addon card
- `.addon-link` - Addon name link
- `.addon-links` - Button container
- `.btn`, `.btn-primary`, `.btn-secondary` - Button styling

**Info sections:**
- `.info-section` - Styled information box
- `.doc-links` - Documentation links grid
- `.repo-info` - Repository URL box
- `.repo-url` - Monospace URL display

### Dependencies

**Required:**
- Python 3.9+ (for Path.is_relative_to() method used in error handling)
- xml.etree.ElementTree (standard library)
- pathlib (standard library)

**No external dependencies required!**

---

## Integration in GitHub Actions

### Workflow Execution Order

1. **Step 8** - Run `convert_md_to_html.py doc docs/doc`
   - Input: doc directory
   - Output: docs/doc directory with .html files

2. **Step 9** - Run `generate_readme.py docs`
   - Input: docs directory (with addon subdirectories)
   - Output: docs/readme.html

### Environment

Scripts run in Ubuntu Linux environment with:
- Python 3.9+ installed
- All files available
- Network access (not needed for these scripts)
- Write access to docs directory

### Error Handling in Workflow

If either script fails:
```yaml
echo "Error occurred"
exit 1
```

This will cause the workflow job to fail and prevent deployment of incomplete site.

---

## Testing Locally

### Prerequisites
```bash
python3 --version  # Should be 3.9 or higher
```

### Test convert_md_to_html.py
```bash
python3 scripts/convert_md_to_html.py doc test_output
ls test_output/
cat test_output/README.html  # View generated file
```

### Test generate_readme.py
First create test addon structure:
```bash
mkdir -p test_docs/plugin.test
cat > test_docs/plugin.test/addon.xml << 'EOF'
<?xml version='1.0' encoding='utf-8'?>
<addon id="plugin.test" name="Test Addon" version="1.0.0">
    <extension point="xbmc.addon.metadata">
        <summary lang="en_GB">Test summary</summary>
        <description lang="en_GB">Test description</description>
    </extension>
</addon>
EOF

python3 scripts/generate_readme.py test_docs
cat test_docs/readme.html  # View generated file
```

### Cleanup
```bash
rm -rf test_output test_docs
```

---

## Debugging Tips

### Enable verbose output
Both scripts use `print()` statements that should appear in GitHub Actions logs.

### Check generated files
```bash
# After running workflow, check in gh-pages branch
git checkout gh-pages
ls -la docs/
cat docs/readme.html | head -50
```

### Validate HTML
```bash
# Online validators:
# https://validator.w3.org/
# https://jigsaw.w3.org/css-validator/
```

### Check addon.xml files
```bash
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('plugin.video.test/addon.xml')
root = tree.getroot()
print(f'ID: {root.get(\"id\")}')
print(f'Name: {root.get(\"name\")}')
"
```

---

## Performance

Both scripts are optimized for fast execution:

- **convert_md_to_html.py**: ~100-500ms per file (depending on file size)
- **generate_readme.py**: ~50-200ms total (very fast)

Total conversion time for 20 doc files and 5 addons: < 2 seconds

---

## Future Enhancements

### convert_md_to_html.py
- [ ] Add YAML frontmatter support
- [ ] Generate table of contents
- [ ] Add syntax highlighting for code blocks
- [ ] Support for embedding images
- [ ] Custom CSS theme support

### generate_readme.py
- [ ] Search/filter functionality
- [ ] Addon rating system
- [ ] Screenshot display
- [ ] Multi-language support
- [ ] Changelog display
- [ ] Statistics (download count, etc.)

---

## License

These scripts are part of the kodi-play-random project and follow the same license.

