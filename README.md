# Batch Replace Tool - 批量修改体系文件工具

智能批量修改体系文件工具，支持逐条确认、预览对比、自动备份和回滚功能。

## 功能特性

- **智能检索**: 自动扫描指定范围内的所有文件
- **位置标注**: 精确显示匹配内容在文件中的位置（行号、列号、上下文）
- **批量修改**: 支持统一批量替换
- **逐条确认**: 每条修改前需用户确认，避免误操作
- **修改预览**: 修改前展示前后对比
- **自动备份**: 修改前自动创建备份
- **回滚支持**: 支持批量撤销已执行的修改
- **正则支持**: 支持正则表达式匹配

## 安装

```bash
# 克隆仓库
git clone <repo-url>
cd batch_replace_tool

# 安装依赖
pip install -e ".[dev]"
```

## 使用方法

### 基础用法

```bash
# 将 "质量管理体系" 替换为 "质量管控体系"
batch-replace "质量管理体系" "质量管控体系"

# 指定搜索范围
batch-replace "质量管理体系" "质量管控体系" --scope ./docs

# 限定文件类型
batch-replace "质量目标" "质量指标" --include "*.md" --include "*.txt"
```

### 高级用法

```bash
# 使用正则表达式
batch-replace "V\d+\.\d+" "V2.0" --regex

# 全词匹配
batch-replace "质量" "品质" --whole-word

# 区分大小写
batch-replace "ISO9001" "ISO9001:2015" --case-sensitive

# 排除特定目录
batch-replace "旧文本" "新文本" --exclude "archive/" --exclude "draft/"

# 跳过确认直接执行（危险！）
batch-replace "旧文本" "新文本" --yes

# 仅预览不执行
batch-replace "旧文本" "新文本" --dry-run

# 指定备份目录
batch-replace "旧文本" "新文本" --backup-dir ./backups

# 生成报告
batch-replace "旧文本" "新文本" --report
```

## 工作流程

1. **输入目标**: 输入要查找的文本和替换文本
2. **智能检索**: 自动扫描指定范围内的文件
3. **定位分析**: 标注匹配位置及上下文
4. **整体确认**: 展示检索结果汇总，确认是否继续
5. **逐条确认**: 每条修改前单独确认，可预览对比
6. **执行修改**: 确认后执行修改并创建备份
7. **生成报告**: 输出变更日志和报告

## 确认操作说明

在逐条确认阶段，可输入以下操作：

| 操作 | 说明 |
|------|------|
| `Y` | 确认修改此项 |
| `n` | 跳过此项（不修改） |
| `s` | 跳过此文件的所有剩余匹配 |
| `q` | 取消全部操作并回滚已修改 |
| `e` | 编辑替换文本（临时修改） |
| `m` | 显示更多上下文 |
| `?` | 显示帮助 |

## 项目结构

```
batch_replace_tool/
├── src/batch_replace/
│   ├── agents/           # Agent模块
│   │   ├── search_agent.py   # 检索Agent
│   │   ├── locate_agent.py   # 定位Agent
│   │   ├── confirm_agent.py  # 确认Agent
│   │   └── execute_agent.py  # 执行Agent
│   ├── models/           # 数据模型
│   ├── ui/               # UI模块
│   ├── utils/            # 工具函数
│   ├── cli.py            # CLI入口
│   └── __init__.py
├── tests/                # 测试文件
│   └── fixtures/         # 测试数据
├── pyproject.toml
└── README.md
```

## 技术栈

- Python 3.9+
- Click - CLI框架
- Rich - 终端UI库
- chardet - 编码检测

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black src tests
ruff check src tests
```

## 许可证

MIT License
