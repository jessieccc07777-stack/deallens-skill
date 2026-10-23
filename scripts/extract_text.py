#!/usr/bin/env python
"""Extract full text (paragraphs + tables) from a .docx or .pdf agreement into a .txt file.

Usage: python extract_text.py <input.docx|input.pdf> [output.txt]
Tables are emitted as [TBL] rows so equity/cap-table data is not lost.
"""
import sys
from pathlib import Path


def from_docx(path: Path) -> list[str]:
    from docx import Document
    doc = Document(str(path))
    out = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    for tb in doc.tables:
        for row in tb.rows:
            cells = [c.text.strip().replace("\n", " ") for c in row.cells]
            line = " | ".join(c for c in cells if c)
            if line:
                out.append("[TBL] " + line)
    return out


def from_pdf(path: Path) -> list[str]:
    from pypdf import PdfReader
    reader = PdfReader(str(path))
    out = []
    for i, page in enumerate(reader.pages, 1):
        text = (page.extract_text() or "").strip()
        if text:
            out.append(f"[PAGE {i}]")
            out.extend(ln for ln in (l.strip() for l in text.splitlines()) if ln)
    return out


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    if not src.exists():
        sys.exit(f"file not found: {src}")
    ext = src.suffix.lower()
    if ext == ".docx":
        lines = from_docx(src)
    elif ext == ".pdf":
        lines = from_pdf(src)
    else:
        sys.exit(f"unsupported format: {ext} (use .docx or .pdf)")
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".txt")
    dst.write_text("\n".join(lines), encoding="utf-8")
    print(f"{src.name} -> {dst.name}: {len(lines)} lines, {sum(len(x) for x in lines)} chars")


if __name__ == "__main__":
    main()
