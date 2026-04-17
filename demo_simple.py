#!/usr/bin/env python3
"""
简化演示脚本 - 展示 batch-replace 工具的基本用法
"""

import sys
from pathlib import Path

# 添加到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from batch_replace.agents.locate_agent import LocateAgent
from batch_replace.agents.search_agent import MatchMode, SearchAgent, SearchConfig


def demo_search():
    """演示搜索功能"""
    print("=" * 80)
    print("Batch Replace Tool - 批量修改体系文件工具")
    print("=" * 80)
    print()
    print("演示: 搜索功能")
    print()

    # 配置搜索
    config = SearchConfig(
        match_mode=MatchMode.EXACT,
        case_sensitive=False,
        include_patterns=["*.md"],
        exclude_patterns=[".git/", "__pycache__/"],
    )

    search_agent = SearchAgent(config)

    # 搜索关键词
    target = "质量管理体系"
    scope = Path(__file__).parent / "tests" / "fixtures"

    print(f"搜索: {target}")
    print(f"范围: {scope}")
    print()

    file_matches_list = search_agent.search(target, scope)

    if not file_matches_list:
        print("未找到匹配项")
        return

    # 显示结果
    total_matches = sum(len(fm.matches) for fm in file_matches_list)
    print(f"找到 {len(file_matches_list)} 个文件，共 {total_matches} 处匹配")
    print()

    # 定位并显示详细信息
    locate_agent = LocateAgent()
    located_matches = locate_agent.locate_all(file_matches_list)

    for match in located_matches[:5]:  # 只显示前5个
        print(f"\n文件: {match.file_path}")
        print(f"  位置: 第 {match.line} 行, 第 {match.column} 列")
        print(f"  匹配内容: {match.target_line[:60]}...")

    if len(located_matches) > 5:
        print(f"\n... 还有 {len(located_matches) - 5} 处匹配 ...")

    print("\n" + "=" * 80)


def demo_preview():
    """演示预览功能"""
    print("\n演示: 修改预览")
    print()

    target = "质量管理体系"
    replacement = "质量管控体系"

    config = SearchConfig(
        match_mode=MatchMode.EXACT,
        case_sensitive=False,
        include_patterns=["*.md"],
        exclude_patterns=[".git/", "__pycache__/"],
    )

    search_agent = SearchAgent(config)
    scope = Path(__file__).parent / "tests" / "fixtures"

    file_matches_list = search_agent.search(target, scope)
    locate_agent = LocateAgent()
    located_matches = locate_agent.locate_all(file_matches_list)

    if located_matches:
        match = located_matches[0]

        print(f"文件: {match.file_path}")
        print(f"位置: 第 {match.line} 行, 第 {match.column} 列")
        print()

        print("BEFORE:")
        for i, line in enumerate(match.context_before):
            line_num = match.line - len(match.context_before) + i
            print(f"  {line_num:4d} | {line}")

        print(f"  {match.line:4d} | {match.target_line}")

        for i, line in enumerate(match.context_after):
            line_num = match.line + i + 1
            print(f"  {line_num:4d} | {line}")

        print()
        print("AFTER:")
        for i, line in enumerate(match.context_before):
            line_num = match.line - len(match.context_before) + i
            print(f"  {line_num:4d} | {line}")

        modified_line = match.target_line.replace(match.target_text, f"[{replacement}]")
        print(f"  {match.line:4d} | {modified_line}")

        for i, line in enumerate(match.context_after):
            line_num = match.line + i + 1
            print(f"  {line_num:4d} | {line}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    demo_search()
    demo_preview()
    print("\n演示完成!")
