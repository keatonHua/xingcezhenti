#!/usr/bin/env python3
"""Split national civil-service exam 'administrative law' papers into year/type folders.

Structure created:
  国家公务员录用考试《行测》题（行政执法卷）/
    {year}/
      {module}/
        题目.md
        答案.md

The script reads the existing raw markdown files already in the repo and writes split files
without modifying the original files.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET_ROOT = ROOT / "国家公务员录用考试《行测》题（行政执法卷）》"

# Use a stable literal path name that matches the directory created in the repo.
TARGET_ROOT = ROOT / "国家公务员录用考试《行测》题（行政执法卷）"

SOURCE_PATTERNS = [
    "*国家公务员录用考试《行测》题（行政执法卷网友回忆版）*.md",
    "*国家公务员录用考试《行测》题（行政执法卷）*.md",
]


def split_question_and_answer(content: str):
    marker = "**答案**："
    if marker not in content:
        return content.strip(), "未检测到答案分隔标记。"
    question_part, answer_part = content.split(marker, 1)
    return question_part.strip(), f"{marker}{answer_part.strip()}"


def main():
    TARGET_ROOT.mkdir(parents=True, exist_ok=True)

    source_files = []
    for pattern in SOURCE_PATTERNS:
        source_files.extend(ROOT.glob(f"**/{pattern}"))

    seen = set()
    for file_path in sorted(source_files):
        if file_path in seen:
            continue
        seen.add(file_path)

        year_match = re.search(r"(\d{4})年", file_path.name)
        if not year_match:
            continue
        year = year_match.group(1)

        module_name = file_path.parent.name
        out_dir = TARGET_ROOT / year / module_name
        out_dir.mkdir(parents=True, exist_ok=True)

        text = file_path.read_text(encoding="utf-8")
        question_text, answer_text = split_question_and_answer(text)

        question_path = out_dir / "题目.md"
        answer_path = out_dir / "答案.md"

        question_content = (
            "---\n"
            "类型: \"题目\"\n"
            f"年份: \"{year}\"\n"
            f"题型: \"{module_name}\"\n"
            f"来源: \"{file_path.relative_to(ROOT)}\"\n"
            "---\n\n"
            f"# {year} 年国家公务员录用考试《行测》题（行政执法卷）\n\n"
            "## 题目\n\n"
            f"{question_text}\n"
        )
        answer_content = (
            "---\n"
            "类型: \"答案\"\n"
            f"年份: \"{year}\"\n"
            f"题型: \"{module_name}\"\n"
            f"来源: \"{file_path.relative_to(ROOT)}\"\n"
            "---\n\n"
            f"# {year} 年国家公务员录用考试《行测》题（行政执法卷）\n\n"
            "## 答案\n\n"
            f"{answer_text}\n"
        )

        question_path.write_text(question_content, encoding="utf-8")
        answer_path.write_text(answer_content, encoding="utf-8")

    print(f"整理完成：共处理 {len(seen)} 份原始题文件，输出目录：{TARGET_ROOT}")


if __name__ == "__main__":
    main()
