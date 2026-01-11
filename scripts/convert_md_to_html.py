#!/usr/bin/env python3
"""
Скрипт для конвертации Markdown файлов в HTML с поддержкой GitHub Flavored Markdown.
Script to convert Markdown files to HTML with GitHub Flavored Markdown support.
"""

import re
import sys
from pathlib import Path
from typing import Optional

# Попытка импортировать markdown библиотеку
# Try to import markdown library
try:
    import markdown
    from markdown.extensions import tables, fenced_code, codehilite, extra, toc
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False
    print("Warning: markdown library not installed, using basic conversion", file=sys.stderr)


def create_html_template(title: str, content: str) -> str:
    """
    Создает HTML шаблон для документа.
    Creates HTML template for document.
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
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
            background-color: #f6f8fa;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background-color: white;
            padding: 40px;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
        }}
        h1 {{
            font-size: 2em;
            margin: 30px 0 20px 0;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
            color: #24292e;
        }}
        h2 {{
            font-size: 1.5em;
            margin: 25px 0 15px 0;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
            color: #24292e;
        }}
        h3 {{
            font-size: 1.25em;
            margin: 20px 0 10px 0;
            color: #24292e;
        }}
        h4, h5, h6 {{
            margin: 15px 0 10px 0;
            color: #24292e;
        }}
        p {{
            margin: 15px 0;
        }}
        a {{
            color: #0366d6;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        code {{
            background-color: #f6f8fa;
            padding: 0.2em 0.4em;
            margin: 0;
            font-size: 85%;
            border-radius: 3px;
            font-family: 'Courier New', Courier, monospace;
        }}
        pre {{
            background-color: #f6f8fa;
            border: 1px solid #ddd;
            border-radius: 6px;
            padding: 16px;
            overflow: auto;
            margin: 15px 0;
            font-size: 85%;
            line-height: 1.45;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
            margin: 0;
            border: 0;
        }}
        blockquote {{
            padding: 0 1em;
            color: #6a737d;
            border-left: 0.25em solid #dfe2e5;
            margin: 15px 0;
        }}
        ul, ol {{
            padding-left: 2em;
            margin: 15px 0;
        }}
        li {{
            margin: 5px 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }}
        table th {{
            background-color: #f6f8fa;
            border: 1px solid #ddd;
            padding: 6px 13px;
            font-weight: 600;
        }}
        table td {{
            border: 1px solid #ddd;
            padding: 6px 13px;
        }}
        table tr:nth-child(2n) {{
            background-color: #f6f8fa;
        }}
        img {{
            max-width: 100%;
            height: auto;
            margin: 15px 0;
        }}
        .back-link {{
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eaecef;
        }}
        .back-link a {{
            color: #0366d6;
        }}
        hr {{
            height: 0.25em;
            padding: 0;
            margin: 24px 0;
            background-color: #e1e4e8;
            border: 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="back-link">
            <a href="../">← Back to home</a>
        </div>
        {content}
    </div>
</body>
</html>"""


def convert_markdown_to_html(markdown_content: str) -> str:
    """
    Конвертирует Markdown в HTML.
    Converts Markdown to HTML.
    """
    if HAS_MARKDOWN:
        # Использование markdown библиотеки с расширениями
        # Use markdown library with extensions
        html = markdown.markdown(
            markdown_content,
            extensions=[
                'extra',
                'tables',
                'fenced_code',
                'codehilite',
                'toc',
            ]
        )
        return html
    else:
        # Базовая конвертация если библиотека не установлена
        # Basic conversion if library is not installed
        return _basic_markdown_to_html(markdown_content)


def _basic_markdown_to_html(content: str) -> str:
    """
    Базовое преобразование Markdown в HTML без внешних библиотек.
    Basic Markdown to HTML conversion without external libraries.
    """
    # Заголовки / Headers
    content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)

    # Жирный текст / Bold text
    content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'__(.+?)__', r'<strong>\1</strong>', content)

    # Курсив / Italic
    content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
    content = re.sub(r'_(.+?)_', r'<em>\1</em>', content)

    # Ссылки / Links
    content = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', content)

    # Код в блоках / Code blocks
    content = re.sub(r'```(.+?)```', r'<pre><code>\1</code></pre>', content, flags=re.DOTALL)

    # Инлайн-код / Inline code
    content = re.sub(r'`(.+?)`', r'<code>\1</code>', content)

    # Горизонтальная линия / Horizontal line
    content = re.sub(r'^[-*_]{3,}$', r'<hr>', content, flags=re.MULTILINE)

    # Цитаты / Blockquotes
    content = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', content, flags=re.MULTILINE)

    # Параграфы / Paragraphs
    paragraphs = content.split('\n\n')
    paragraphs = [f'<p>{p}</p>' if p and not p.startswith('<') else p for p in paragraphs]
    content = '\n'.join(paragraphs)

    return content


def convert_file(input_path: Path, output_path: Path) -> bool:
    """
    Конвертирует файл Markdown в HTML.
    Converts Markdown file to HTML.
    """
    try:
        # Чтение Markdown файла / Read Markdown file
        markdown_content = input_path.read_text(encoding='utf-8')

        # Получение заголовка из имени файла / Get title from filename
        title = input_path.stem.replace('_', ' ').replace('-', ' ')

        # Конвертация в HTML / Convert to HTML
        html_content = convert_markdown_to_html(markdown_content)

        # Создание полного HTML документа / Create full HTML document
        full_html = create_html_template(title, html_content)

        # Запись в выходной файл / Write to output file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(full_html, encoding='utf-8')

        print(f"✓ Converted: {input_path.name} → {output_path.name}")
        return True

    except Exception as e:
        print(f"✗ Error converting {input_path.name}: {e}", file=sys.stderr)
        return False


def main():
    """
    Основная функция скрипта.
    Main function of the script.
    """
    if len(sys.argv) < 2:
        print("Usage: convert_md_to_html.py <input_dir> [output_dir]", file=sys.stderr)
        sys.exit(1)

    input_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else input_dir.parent / "html"

    if not input_dir.is_dir():
        print(f"Error: {input_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    # Поиск всех MD файлов / Find all MD files
    md_files = list(input_dir.glob("*.md"))

    if not md_files:
        print(f"Warning: No markdown files found in {input_dir}", file=sys.stderr)
        return

    print(f"Found {len(md_files)} markdown file(s)")
    print(f"Output directory: {output_dir}")
    print()

    # Конвертация каждого файла / Convert each file
    successful = 0
    for md_file in sorted(md_files):
        html_file = output_dir / f"{md_file.stem}.html"
        if convert_file(md_file, html_file):
            successful += 1

    print()
    print(f"✓ Successfully converted {successful}/{len(md_files)} files")


if __name__ == "__main__":
    main()

