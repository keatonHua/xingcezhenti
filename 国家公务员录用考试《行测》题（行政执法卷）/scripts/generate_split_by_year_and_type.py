#!/usr/bin/env python3
"""Split the national civil-service administrative-law exam files by year and module.

The repo contains raw markdown files like:
  01-政治理论/2025年国家公务员录用考试《行测》题（行政执法卷网友回忆版）.md

This script copies them into the reorganized layout:
  国家公务员录用考试《行测》题（行政执法卷）/
    2025/
      01-政治理论/
        题目.md
        答案.md
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET_ROOT = ROOT / "国家公务员录用考试《行测》题（行政执法卷）"


def split_question_and_answer(content: str):
    marker = "**答案**："
    if marker not in content:
        return content.strip(), "未检测到答案分隔标记。"
    question_part, answer_part = content.split(marker, 1)
    return question_part.strip(), f"{marker}{answer_part.strip()}"


def main():
    TARGET_ROOT.mkdir(parents=True, exist_ok=True)

    source_files = []
    for path in ROOT.rglob("*.md"):
        name = path.name
        if "国家公务员录用考试《行测》题" in name and "行政执法卷" in name:
            source_files.append(path)

    seen = set()
    processed = 0
    for file_path in sorted(source_files):
        key = str(file_path)
        if key in seen:
            continue
        seen.add(key)

        year_match = re.search(r"(\d{4})年", file_path.name)
        if not year_match:
            continue
        year = year_match.group(1)

        module_name = file_path.parent.name
        out_dir = TARGET_ROOT / year / module_name
        out_dir.mkdir(parents=True, exist_ok=True)

        text = file_path.read_text(encoding="utf-8")
        question_text, answer_text = split_question_and_answer(text)
        rel_path = file_path.relative_to(ROOT)

        question_content = (
            "---\n"
            "类型: \"题目\"\n"
            f"年份: \"{year}\"\n"
            f"题型: \"{module_name}\"\n"
            f"来源: \"{rel_path}\"\n"
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
            f"来源: \"{rel_path}\"\n"
            "---\n\n"
            f"# {year} 年国家公务员录用考试《行测》题（行政执法卷）\n\n"
            "## 答案\n\n"
            f"{answer_text}\n"
        )

        (out_dir / "题目.md").write_text(question_content, encoding="utf-8")
        (out_dir / "答案.md").write_text(answer_content, encoding="utf-8")
        processed += 1

    print(f"整理完成：共处理 {processed} 份原始题文件，输出目录：{TARGET_ROOT}")


if __name__ == "__main__":
    main()
