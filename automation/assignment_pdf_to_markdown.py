#%%
from pylatexenc.latexencode import unicode_to_latex

# This will convert the Unicode character back to its LaTeX equivalent
char = "∈"
latex_code = unicode_to_latex(char)

print(latex_code)      # \ensuremath(\in)
#%%
from pathlib import Path
from argparse import ArgumentParser

import pymupdf4llm

header = """---
Author: 
CreationDate: 
ChangeDate: 
CurrentDate: 
---

<!-- set all attributes used by VS Code Markdown Converter extension to blank above, so that it doesn't come in generated PDF -->

"""

parser = ArgumentParser(description='Convert Assignment PDF to Markdown')
parser.add_argument('pdf_path', help='Path to Assignment PDF')
args = parser.parse_args()

pdf_path = Path(args.pdf_path)
md_text: str = pymupdf4llm.to_markdown(pdf_path)
md_text = header + md_text
# TODO: after title, add line (author Sohang, roll no.)
# TODO MAYBE: convert 1. <question> 2. <question> 3. <question> to format: ## Problem {i} <question> ### Solution {i}
# TODO: correct math expressions (convert to MathJAX format expected by Github Markdown)
# TODO: handle images in PDF (write them to images/ folder and include in Markdown)
# TODO: remove page numbers
(pdf_path.parent / f'solution_{pdf_path.stem}.md').write_text(md_text)