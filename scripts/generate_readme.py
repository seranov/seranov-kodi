#!/usr/bin/env python3
"""
Скрипт для генерации readme.html со ссылками на плагины и их описаниями.
Script to generate readme.html with links to plugins and their descriptions.
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class AddonInfo:
    """Информация о дополнении / Add-on information"""

    def __init__(self, addon_id: str, name: str, version: str, summary: str, description: str):
        """
        Инициализация информации о дополнении.
        Initialize add-on information.
        """
        self.addon_id: str = addon_id
        self.name: str = name
        self.version: str = version
        self.summary: str = summary
        self.description: str = description

    def get_zip_name(self) -> str:
        """Получить имя ZIP архива / Get ZIP archive name"""
        return f"{self.addon_id}-{self.version}.zip"

    def to_html(self) -> str:
        """Преобразовать в HTML строку / Convert to HTML string"""
        zip_name: str = self.get_zip_name()
        return f"""
        <div class="addon-card">
            <h3>
                <a href="{self.addon_id}/{zip_name}" class="addon-link">
                    📦 {self.name}
                </a>
            </h3>
            <p class="version">Version: <strong>{self.version}</strong></p>
            <p class="summary">{self.summary}</p>
            <p class="description">{self.description}</p>
            <div class="addon-links">
                <a href="{self.addon_id}/" class="btn btn-secondary">View Files</a>
                <a href="{self.addon_id}/{zip_name}" class="btn btn-primary">Download ZIP</a>
            </div>
        </div>
"""


def parse_addon_xml(xml_path: Path) -> Optional[AddonInfo]:
    """
    Парсирует addon.xml файл и извлекает информацию.
    Parse addon.xml file and extract information.
    """
    try:
        tree: ET.ElementTree = ET.parse(xml_path)
        root: ET.Element = tree.getroot()

        addon_id: str = root.get('id', 'unknown')
        name: str = root.get('name', addon_id)
        version: str = root.get('version', '1.0.0')

        # Извлечение summary и description на английском / Extract summary and description in English
        summary: str = ''
        description: str = ''

        metadata: Optional[ET.Element] = root.find(".//extension[@point='xbmc.addon.metadata']")
        if metadata is not None:
            summary_elem: Optional[ET.Element] = metadata.find("summary[@lang='en_GB']")
            if summary_elem is not None:
                summary = summary_elem.text or ''

            desc_elem: Optional[ET.Element] = metadata.find("description[@lang='en_GB']")
            if desc_elem is not None:
                description = desc_elem.text or ''

        return AddonInfo(addon_id, name, version, summary, description)

    except Exception as e:
        print(f"Error parsing {xml_path}: {e}", file=sys.stderr)
        return None


def scan_addons(docs_dir: Path) -> List[AddonInfo]:
    """
    Сканирует директорию docs для поиска аддонов.
    Scan docs directory for add-ons.
    """
    addons: List[AddonInfo] = []

    # Ищет папки с аддонами / Look for addon directories
    addon_patterns: List[str] = [
        'plugin.*',
        'service.*',
        'context.*',
        'repository.*'
    ]

    for addon_dir in sorted(docs_dir.iterdir()):
        if not addon_dir.is_dir():
            continue

        # Проверяет, начинается ли папка с известного префикса
        # Check if directory name starts with known prefix
        is_addon_dir: bool = any(
            addon_dir.name.startswith(pattern.split('*')[0])
            for pattern in addon_patterns
        )

        if not is_addon_dir:
            continue

        # Ищет addon.xml в исходной папке (не в docs)
        # Look for addon.xml in the source folder (not in docs)
        addon_xml: Path = Path(addon_dir.name) / 'addon.xml'
        if addon_xml.exists():
            addon_info: Optional[AddonInfo] = parse_addon_xml(addon_xml)
            if addon_info:
                addons.append(addon_info)

    return addons


def create_html_content(addons: List[AddonInfo]) -> str:
    """
    Создает HTML контент со ссылками на плагины.
    Create HTML content with plugin links.
    """
    addon_cards: str = ''.join(addon.to_html() for addon in addons)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Seranov Kodi Repository</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        
        .header {{
            background-color: white;
            padding: 40px 30px;
            border-radius: 10px 10px 0 0;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            color: #24292e;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            color: #666;
            margin-bottom: 20px;
        }}
        
        .repo-info {{
            background-color: #f6f8fa;
            padding: 20px;
            border-radius: 5px;
            margin-top: 20px;
            text-align: left;
        }}
        
        .repo-info h3 {{
            color: #24292e;
            margin-bottom: 10px;
        }}
        
        .repo-url {{
            background-color: white;
            border: 1px solid #ddd;
            padding: 10px 15px;
            border-radius: 5px;
            font-family: monospace;
            word-break: break-all;
            color: #0366d6;
        }}
        
        .content {{
            background-color: white;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        
        .content h2 {{
            font-size: 1.8em;
            color: #24292e;
            margin-bottom: 20px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .addons-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .addon-card {{
            border: 1px solid #e1e4e8;
            border-radius: 8px;
            padding: 20px;
            background-color: #f6f8fa;
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
        }}
        
        .addon-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
            border-color: #667eea;
        }}
        
        .addon-card h3 {{
            margin-bottom: 10px;
            font-size: 1.3em;
        }}
        
        .addon-link {{
            color: #0366d6;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.2s ease;
        }}
        
        .addon-link:hover {{
            color: #667eea;
            text-decoration: underline;
        }}
        
        .version {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
        }}
        
        .summary {{
            font-weight: 500;
            color: #24292e;
            margin-bottom: 8px;
            min-height: 40px;
        }}
        
        .description {{
            color: #666;
            font-size: 0.95em;
            margin-bottom: 15px;
            flex-grow: 1;
            line-height: 1.4;
        }}
        
        .addon-links {{
            display: flex;
            gap: 10px;
            margin-top: auto;
        }}
        
        .btn {{
            padding: 8px 16px;
            border-radius: 5px;
            text-decoration: none;
            font-size: 0.9em;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: all 0.2s ease;
            flex: 1;
            text-align: center;
            display: inline-block;
        }}
        
        .btn-primary {{
            background-color: #667eea;
            color: white;
        }}
        
        .btn-primary:hover {{
            background-color: #5568d3;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        }}
        
        .btn-secondary {{
            background-color: #e1e4e8;
            color: #24292e;
        }}
        
        .btn-secondary:hover {{
            background-color: #d1d5da;
        }}
        
        .info-section {{
            background-color: #f6f8fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }}
        
        .info-section h3 {{
            color: #24292e;
            margin-bottom: 10px;
        }}
        
        .info-section ol {{
            margin-left: 20px;
        }}
        
        .info-section li {{
            margin-bottom: 8px;
        }}
        
        code {{
            background-color: #f1f6fc;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
            font-size: 0.9em;
            color: #d73a49;
        }}
        
        .footer {{
            background-color: white;
            padding: 20px 30px;
            border-radius: 0 0 10px 10px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin-top: 0;
        }}
        
        .footer a {{
            color: #0366d6;
            text-decoration: none;
        }}
        
        .footer a:hover {{
            text-decoration: underline;
        }}
        
        .doc-links {{
            background-color: #f6f8fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        
        .doc-links h3 {{
            color: #24292e;
            margin-bottom: 15px;
        }}
        
        .doc-links ul {{
            list-style: none;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 10px;
        }}
        
        .doc-links li {{
            margin-bottom: 0;
        }}
        
        .doc-links a {{
            display: block;
            padding: 10px 15px;
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 5px;
            color: #0366d6;
            text-decoration: none;
            transition: all 0.2s ease;
        }}
        
        .doc-links a:hover {{
            border-color: #667eea;
            background-color: #f9f9f9;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 Seranov Kodi Repository</h1>
            <p>A comprehensive repository of Kodi add-ons for enhanced multimedia experience</p>
            
            <div class="repo-info">
                <h3>📍 Repository URL</h3>
                <div class="repo-url">
                    https://seranov.github.io/kodi-play-random/
                </div>
            </div>
        </div>
        
        <div class="content">
            <h2>📦 Installation Instructions</h2>
            
            <div class="info-section">
                <h3>Method 1: Install Repository (Recommended)</h3>
                <ol>
                    <li>Download <code>repository.seranov-1.0.0.zip</code> from the list below</li>
                    <li>In Kodi, navigate to <strong>Add-ons → Install from zip file</strong></li>
                    <li>Select the downloaded repository zip file</li>
                    <li>Wait for the installation notification</li>
                    <li>Go to <strong>Add-ons → Install from repository → Seranov's Kodi Repository</strong></li>
                    <li>Choose and install the add-ons you want</li>
                </ol>
            </div>
            
            <div class="info-section">
                <h3>Method 2: Direct ZIP Installation</h3>
                <ol>
                    <li>Download the desired add-on ZIP file from below</li>
                    <li>In Kodi, go to <strong>Add-ons → Install from zip file</strong></li>
                    <li>Select the downloaded ZIP file</li>
                    <li>Wait for installation to complete</li>
                </ol>
            </div>
            
            <h2>📋 Available Add-ons</h2>
            <div class="addons-grid">
{addon_cards}
            </div>
            
            <div class="doc-links">
                <h3>📚 Documentation</h3>
                <ul>
                    <li><a href="doc/README.html">📖 Main Documentation</a></li>
                    <li><a href="doc/QUICKSTART.html">⚡ Quick Start</a></li>
                    <li><a href="doc/INSTALLATION.html">🔧 Installation Guide</a></li>
                    <li><a href="doc/CONTRIBUTING.html">🤝 Contributing</a></li>
                    <li><a href="doc/RELEASE_NOTES.html">📝 Release Notes</a></li>
                </ul>
            </div>
            
            <div class="info-section">
                <h3>📁 Repository Files</h3>
                <ul style="margin-left: 20px;">
                    <li><a href="addons.xml" style="color: #0366d6;">addons.xml</a> - Repository metadata (required by Kodi)</li>
                    <li><a href="addons.xml.md5" style="color: #0366d6;">addons.xml.md5</a> - Checksum for verification</li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p>Seranov Kodi Repository &copy; 2024-2026</p>
            <p>
                <a href="https://github.com/seranov/seranov-kodi">GitHub Repository</a> | 
                <a href="https://github.com/seranov/seranov-kodi/issues">Report Issues</a>
            </p>
            <p style="margin-top: 10px; font-size: 0.85em;">
                This repository contains add-ons for <a href="https://kodi.tv">Kodi Media Center</a>
            </p>
        </div>
    </div>
</body>
</html>"""


def main():
    """Основная функция / Main function"""

    # Получение пути к docs директории
    # Get path to docs directory
    if len(sys.argv) > 1:
        docs_dir: Path = Path(sys.argv[1])
    else:
        docs_dir: Path = Path('docs')

    print(f"Scanning for add-ons in: {docs_dir}")

    # Сканирование аддонов / Scan add-ons
    addons: List[AddonInfo] = scan_addons(docs_dir)

    if not addons:
        print("Warning: No add-ons found!", file=sys.stderr)
        addons: List[AddonInfo] = []
    else:
        print(f"Found {len(addons)} add-on(s)")

    # Создание HTML контента / Create HTML content
    html_content: str = create_html_content(addons)

    # Запись в файл / Write to file
    readme_path: Path = docs_dir / 'readme.html'
    readme_path.write_text(html_content, encoding='utf-8')

    print(f"✓ Generated: {readme_path}")


if __name__ == "__main__":
    main()

