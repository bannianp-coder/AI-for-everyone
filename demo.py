#!/usr/bin/env python3
"""
演示脚本 - 展示 batch-replace 工具的基本用法
"""
import sys
from pathlib import Path

# 添加到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from batch_replace.agents.locate_agent import LocateAgent
from batch_replace.agents.search_agent import MatchMode, SearchAgent, SearchConfig
from batch_replace.ui.console_ui import ConsoleUI
from rich.console import Console


def demo_preview():
    """演示预览功能"""
    console = Console()

    console.print("\n[bold cyan]演示: 修改预览[/]\n")

    target = "2222"
    replacement = "3333"

    config = SearchConfig(
        match_mode=MatchMode.EXACT,
        case_sensitive=False,
        include_patterns=["*"],
        exclude_patterns=[".git/", "__pycache__/"],
    )

    search_agent = SearchAgent(config)
    scope = Path(__file__).parent / "tests"

    file_matches_list = search_agent.search(target, scope)
    
    if not file_matches_list:
        console.print("[yellow]未找到匹配项[/]")
        return

    locate_agent = LocateAgent()
    located_matches = locate_agent.locate_all(file_matches_list)

    if located_matches:
        match = located_matches[0]

        console.print(f"[bold]文件:[/] {match.file_path}")
        console.print(f"[bold]位置:[/] 第 {match.line} 行\n")

        console.print("[dim]BEFORE:[/]")
        console.print(f"  {match.line:4d} │ {match.target_line}")

        console.print("\n[dim]AFTER:[/]")
        modified_line = match.target_line.replace(target, replacement)
        console.print(f"  {match.line:4d} │ {modified_line}")

        # 执行实际修改
        for file_match in file_matches_list:
            with open(file_match.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = content.replace(target, replacement)
            with open(file_match.file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        
        console.print("\n[bold green]✓ 已修改文件[/]")

    console.print("\n[dim]--- 演示结束 ---[/]")


if __name__ == "__main__":
    demo_preview()
