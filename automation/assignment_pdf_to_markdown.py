"""Convert assignment PDF to Markdown.

Allows me to type solution in Markdown and then convert solution back to PDF to submit.

NOTE: pymupdf on its own is also very useful even on CLI :

$ python -m pymupdf    
usage: pymupdf [-h] {show,clean,join,extract,embed-info,embed-add,embed-del,embed-upd,embed-extract,embed-copy,gettext,internal} ...
$ python -m pymupdf gettext /path/to/file_name.pdf
(creates /path/to/file_name.txt !)
$ cd /path/to/folder && ~/iit-madras-web-mtech-ai/automation/all_pdfs_to_markdown.sh     # script that runs pymupdf gettext converts all **/*.pdf to *.txt
# this error happened for one PDF only
RuntimeError: program error: minslot too small = 0
Failed for trimester3/CH5440W_MultiVariateAnalysis/lectures/30.06.2026/StatisticalDistance.pdf , continuing.
"""

from argparse import ArgumentParser
from datetime import date
from pathlib import Path
import re
from typing import cast

import pymupdf4llm

AUTHOR = 'Sohang'
ROLL_NO = 'DA25M622'
TODAY = date.today().isoformat()

HEADER = f"""---
Author: {AUTHOR}
RollNo: {ROLL_NO}
CreationDate: 
ChangeDate: 
CurrentDate: {TODAY}
---

<!-- set all attributes used by VS Code Markdown Converter extension to blank above, so that it doesn't come in generated PDF -->

"""

parser = ArgumentParser(description='Convert Assignment PDF to Markdown')
parser.add_argument('pdf_path', help='Path to Assignment PDF')
parser.add_argument('--image-size-limit', 
    type=float, 
    default=1, 
    help='Maximum size (in ratio of page size) for images to be extracted. Larger images will be skipped. By default, all images are extracted.'
)
args = parser.parse_args()

pdf_path = Path(args.pdf_path)
if not pdf_path.exists():
    raise FileNotFoundError(f'PDF file not found: {pdf_path}')

image_dir = pdf_path.parent / f'{pdf_path.stem}_images'
image_dir.mkdir(parents=True, exist_ok=True)

markdown_args = {
    'write_images': True,
    'image_path': str(image_dir),
    'image_format': 'png',
    'page_separators': False,
}

try:
    md_text: str = cast(str, pymupdf4llm._layout_to_markdown(
        pdf_path, 
        footer=False, 
        **markdown_args
    ))
except AttributeError:
    md_text = cast(str, pymupdf4llm.to_markdown(
        pdf_path,
        image_size_limit=args.image_size_limit,
        **markdown_args
    ))

md_text = HEADER + md_text

# Insert an explicit author/roll line at the top of the Markdown.
author_line = f'**Author:** {AUTHOR}, **Roll No.:** {ROLL_NO}\n\n'
md_text = HEADER + author_line + md_text[len(HEADER):]


def remove_page_numbers(text: str) -> str:
    text = re.sub(r'(?m)^[ \t]*Page\s*\d+[ \t]*$', '', text)
    text = re.sub(r'(?m)^[ \t]*\d+[ \t]*$', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip() + '\n'


def normalize_math(text: str) -> str:
    text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', text, flags=re.S)
    text = re.sub(r'\\\((.*?)\\\)', r'$\1$', text, flags=re.S)
    text = re.sub(
        r'\\begin\{(?:equation|align|gather)\}(.*?)\\end\{(?:equation|align|gather)\}',
        r'$$\1$$',
        text,
        flags=re.S,
    )
    return text

md_text = normalize_math(md_text)
md_text = remove_page_numbers(md_text)

md_path = pdf_path.parent / f'solution_{pdf_path.stem}.md'
md_path.write_text(md_text)
print('Saved Assignment Markdown at:', md_path)
print('Saved extracted images at:', image_dir)
