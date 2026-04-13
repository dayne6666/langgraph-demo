# LangGraph Demo 项目设计文档

## 文档信息
- **项目名称**: LangGraph Demo
- **版本**: 0.0.1
- **最后更新**: 2026-04-13
- **设计状态**: 进行中

---

## 1. 项目概述

### 1.1 项目简介
这是一个基于 LangGraph v1.0.0 构建的智能代理（Agent）项目模板，提供了可可视化调试的 AI 代理应用开发框架。项目展示了如何使用 LangGraph 构建可扩展的智能工作流，集成多种工具调用，并支持多 LLM 模型配置。

### 1.2 核心特性
- ✅ 基于 LangGraph 的 React 代理架构
- ✅ 支持 LangGraph Studio 可视化调试
- ✅ 集成 LangSmith 追踪功能
- ✅ 多 LLM 模型支持（DeepSeek、Ark/OpenAI 兼容）
- ✅ 5 种工具定义方式示例
- ✅ 完整的测试体系（单元测试 + 集成测试）
- ✅ GitHub Actions CI/CD 流程
- ✅ 代码质量检查（Ruff + MyPy）

### 1.3 适用场景
- 智能对话机器人
- 自动化任务助理
- 多步推理工作流
- 工具调用型 AI 应用
- 可扩展的 Agent 框架

---

## 2. 技术架构

### 2.1 技术栈

| 技术/依赖 | 版本要求 | 用途 | 来源 |
|---------|---------|------|------|
| Python | >=3.10 | 开发语言 | pyproject.toml |
| LangGraph | >=1.0.0 | AI 代理工作流框架 | pyproject.toml |
| LangChain | - | LLM 应用开发框架 | 间接依赖 |
| python-dotenv | >=1.0.1 | 环境变量管理 | pyproject.toml |
| Ruff | >=0.6.1 | 代码检查和格式化 | pyproject.toml |
| MyPy | >=1.11.1 | 类型检查 | pyproject.toml |
| pytest | >=8.3.5 | 测试框架 | pyproject.toml |
| anyio | >=4.7.0 | 异步测试支持 | pyproject.toml |
| langgraph-cli | >=0.4.14 | LangGraph 本地开发服务 | pyproject.toml |

### 2.2 架构层次

```
┌─────────────────────────────────────────────────────┐
│                   LangGraph Studio                   │
│              (可视化调试 & 状态重放)                  │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                   API 服务层                          │
│              (LangGraph Server)                       │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                   代理核心层                          │
│           (React Agent - my_agent.py)                │
│  ┌───────────────────────────────────────────────┐  │
│  │  System Prompt: "你是一个智能助手..."         │  │
│  │  LLM: DeepSeek / Ark                           │  │
│  │  Tools: [calculate3, ...]                      │  │
│  └───────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌───▼────┐ ┌───────▼───────┐
│   LLM 层     │ │ 工具层  │ │  配置管理层    │
│ (my_llm.py)  │ │(tools/) │ │  (env + json)  │
└──────────────┘ └────────┘ └───────────────┘
```

### 2.3 核心架构组件

#### 2.3.1 LLM 模型层
**文件**: `src/agent/my_llm.py`

**职责**:
- 初始化和配置大语言模型
- 管理 API 密钥和服务地址
- 提供可复用的 LLM 实例

**当前配置**:
```python
# DeepSeek 聊天模型
deepseek_llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    base_url=deepseekBaseUrl,
    api_key=deepseek
)

# Ark/OpenAI 兼容模型
llm = init_chat_model(
    model="ark-code-latest",
    model_provider="openai",
    base_url=ark_base_url,
    api_key=ark_api_key
)
```

#### 2.3.2 代理核心层
**文件**: `src/agent/my_agent.py`

**职责**:
- 定义代理工作流图（Graph）
- 注册工具集合
- 配置系统提示词
- 管理代理执行流程

**当前实现**:
```python
graph = create_react_agent(
    deepseek_llm,
    tools=[calculate3],
    prompt="你是一个智能助手，尽可能的调用工具回答用户的问题",
)
```

#### 2.3.3 工具层
**目录**: `src/agent/tools/`

**职责**:
- 提供可被代理调用的工具函数
- 支持多种工具定义方式
- 封装业务逻辑

**5 种工具定义方式**:

| 文件 | 方式 | 特点 |
|-----|-----|------|
| tool_demo1.py | 基础装饰器 | 最简单的 `@tool` 装饰器方式 |
| tool_demo2.py | Pydantic Schema | 自定义参数模型 |
| tool_demo3.py | Annotated 参数 | 使用 `Annotated` 描述参数 |
| tool_demo4.py | 文档字符串解析 | 从 docstring 提取参数信息 |
| tool_demo5.py | StructuredTool | 手动构建结构化工具 |

#### 2.3.4 配置管理层
**文件**: `langgraph.json`, `.env`

**职责**:
- 管理环境变量
- 配置 LangGraph 部署
- 定义图的入口点

---

## 3. 目录结构

### 3.1 完整目录树

```
langgraph_demo/
│
├── 📄 .github/                          # GitHub CI/CD 配置
│   └── workflows/
│       ├── unit-tests.yml              # 单元测试工作流
│       └── integration-tests.yml       # 集成测试工作流
│
├── 📁 .idea/                           # IDE 配置（不提交）
│
├── 📁 src/                             # 主源码目录
│   └── 📁 agent/                       # 代理应用核心包
│       ├── 📄 __init__.py              # 包导出接口
│       ├── 📄 my_agent.py              # 代理图定义（核心）
│       ├── 📄 my_llm.py                # LLM 模型配置
│       └── 📁 tools/                   # 工具函数集合
│           ├── 📄 __init__.py
│           ├── 📄 tool_demo1.py        # 基础工具示例
│           ├── 📄 tool_demo2.py        # Pydantic 参数示例
│           ├── 📄 tool_demo3.py        # Annotated 参数示例（当前使用）
│           ├── 📄 tool_demo4.py        # 文档解析参数示例
│           ├── 📄 tool_demo5.py        # 结构化工具示例
│           └── 🖼️ 1776008880048.jpg   # 静态资源
│
├── 📁 tests/                           # 测试目录
│   ├── 📁 unit_tests/                  # 单元测试
│   │   ├── 📄 __init__.py
│   │   └── 📄 test_configuration.py   # 配置测试
│   ├── 📁 integration_tests/           # 集成测试
│   │   ├── 📄 __init__.py
│   │   └── 📄 test_graph.py           # 图集成测试
│   ├── 📄 conftest.py                  # pytest 配置
│   ├── 📄 my_test.py                   # 测试示例
│   └── 📄 my_test_async.py             # 异步测试示例
│
├── 📁 static/                          # 静态资源目录
│   └── 🖼️ studio_ui.png                # LangGraph Studio 截图
│
├── 📄 .env                             # 环境变量（不提交，参考 .env.example）
├── 📄 .gitignore                       # Git 忽略配置
├── 📄 langgraph.json                   # LangGraph 配置文件
├── 📄 pyproject.toml                   # 项目依赖和配置
├── 📄 README.md                        # 项目说明文档
├── 📄 Makefile                         # 构建和测试脚本
└── 📄 PROJECT_DESIGN.md               # 本文档
```

### 3.2 关键文件说明

| 文件路径 | 重要性 | 说明 |
|---------|--------|------|
| `src/agent/my_agent.py` | ⭐⭐⭐⭐⭐ | 代理核心，定义工作流图 |
| `src/agent/my_llm.py` | ⭐⭐⭐⭐ | LLM 配置，管理模型实例 |
| `src/agent/tools/tool_demo3.py` | ⭐⭐⭐⭐ | 当前使用的 calculate3 工具 |
| `pyproject.toml` | ⭐⭐⭐⭐⭐ | 项目依赖、构建配置 |
| `langgraph.json` | ⭐⭐⭐⭐⭐ | LangGraph 部署配置 |
| `README.md` | ⭐⭐⭐ | 快速开始指南 |
| `tests/integration_tests/test_graph.py` | ⭐⭐⭐ | 集成测试示例 |

---

## 4. 核心功能设计

### 4.1 代理工作流

#### 4.1.1 React Agent 模式
项目使用 LangGraph 提供的 `create_react_agent` 工厂函数创建代理，采用经典的 ReAct（Reasoning + Acting）模式：

```
用户输入
    ↓
[思考] LLM 分析问题，决定是否调用工具
    ↓
[决策] 选择工具并生成参数
    ↓
[执行] 调用选定的工具
    ↓
[观察] 获取工具执行结果
    ↓
[循环] 重复思考-决策-执行，直到得到最终答案
    ↓
最终回答
```

#### 4.1.2 当前工作流配置

```python
graph = create_react_agent(
    deepseek_llm,                    # 使用的 LLM 模型
    tools=[calculate3],               # 可用工具列表
    prompt="你是一个智能助手，尽可能的调用工具回答用户的问题",
)
```

### 4.2 工具系统

#### 4.2.1 工具定义方式比较

**方式 1: 基础装饰器（tool_demo1.py）**
```python
@tool
def function_name(param: type) -> type:
    """工具描述"""
    # 实现
```
- ✅ 最简单
- ❌ 参数描述有限

**方式 2: Annotated 参数（tool_demo3.py）⭐ 当前使用**
```python
@tool('calculate')
def calculate3(
    a: Annotated[float, '第一个需要输入的数字'],
    b: Annotated[float, '第二个需要输入的数字'],
    operation: Annotated[str, '运算类型，只能是add、subtract、multiply、divide中的任意一个']
) -> float:
    """工具函数：计算两个数字的运算结果"""
```
- ✅ 参数描述清晰
- ✅ 类型安全
- ✅ 推荐使用

**方式 3: StructuredTool（tool_demo5.py）**
```python
calculater = StructuredTool.from_function(
    func=calculate5,
    name="calculater",
    description='工具函数：计算两个数字的运算结果',
    coroutine=calculate6  # 异步版本
)
```
- ✅ 最大灵活性
- ✅ 支持同步/异步双版本
- ❌ 代码较多

### 4.3 配置管理

#### 4.3.1 环境变量（.env）
```env
# DeepSeek 配置
DEEPSEEK_API_KEY=your_deepseek_key
DEEPSEEK_BASE_URL=https://api.deepseek.com

# Ark/OpenAI 配置
ARK_API_KEY=your_ark_key
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3

# MySQL 配置（预留）
MYSQL_CONNECTION=mysql://user:pass@host/db

# LangSmith 追踪（可选）
LANGSMITH_API_KEY=lsv2_...
```

#### 4.3.2 LangGraph 配置（langgraph.json）
```json
{
  "$schema": "https://langgra.ph/schema.json",
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/agent/my_agent.py:graph"
  },
  "env": ".env",
  "image_distro": "wolfi"
}
```

---

## 5. 扩展指南

### 5.1 添加新工具

#### 步骤 1: 创建工具文件
在 `src/agent/tools/` 下创建新文件，例如 `my_tool.py`：

```python
from typing import Annotated
from langchain_core.tools import tool

@tool('my_tool_name')
def my_tool(
    param1: Annotated[str, '参数1的描述'],
    param2: Annotated[int, '参数2的描述']
) -> str:
    """工具的整体描述"""
    # 实现工具逻辑
    result = f"处理结果: {param1}, {param2}"
    return result
```

#### 步骤 2: 在 my_agent.py 中注册
```python
from agent.tools.my_tool import my_tool

graph = create_react_agent(
    deepseek_llm,
    tools=[calculate3, my_tool],  # 添加新工具
    prompt="...",
)
```

### 5.2 更换 LLM 模型

修改 `src/agent/my_llm.py` 添加新模型：

```python
from langchain.chat_models import init_chat_model

# 添加新模型
gpt4_llm = init_chat_model(
    model="gpt-4",
    model_provider="openai",
    api_key=os.getenv("OPENAI_API_KEY")
)
```

然后在 `my_agent.py` 中使用：

```python
from agent.my_llm import gpt4_llm

graph = create_react_agent(
    gpt4_llm,  # 使用新模型
    tools=[...],
    prompt="...",
)
```

### 5.3 自定义系统提示词

在 `my_agent.py` 中修改：

```python
graph = create_react_agent(
    deepseek_llm,
    tools=[calculate3],
    prompt="""你是一个专业的数学助手，擅长解决各种数学问题。

要求：
1. 总是先理解问题
2. 需要计算时使用 calculate 工具
3. 用简洁易懂的语言回答
4. 如果问题超出能力范围，诚实告知""",
)
```

### 5.4 添加运行时 Context

参考注释代码实现动态配置：

```python
def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:
    user_name = config['configurable'].get('user_name', 'zs')
    system_message = f'你是一个智能助手，当前用户的名字是: {user_name}'
    return [{'role': 'system', 'content': system_message}] + state['messages']
```

调用时传入配置：

```python
res = graph.invoke(
    {"messages": [{"role": "user", "content": "你好"}]},
    config={"configurable": {"user_name": "张三"}},
)
```

---

## 6. 开发工作流

### 6.1 本地开发

#### 6.1.1 环境准备
```bash
# 1. 克隆项目
cd langgraph_demo

# 2. 安装依赖
pip install -e . "langgraph-cli[inmem]"

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 API keys

# 4. 启动开发服务器
langgraph dev
```

#### 6.1.2 使用 LangGraph Studio
访问 `http://localhost:8123` 进入 Studio UI：
- 可视化查看图结构
- 调试执行状态
- 重放历史执行
- 热重载代码变更

### 6.2 测试

#### 6.2.1 运行测试
```bash
# 单元测试
pytest tests/unit_tests/

# 集成测试
pytest tests/integration_tests/

# 所有测试
pytest

# 带覆盖率
pytest --cov=agent
```

#### 6.2.2 编写新测试
在 `tests/unit_tests/` 或 `tests/integration_tests/` 添加测试文件：

```python
import pytest
from agent import graph

pytestmark = pytest.mark.anyio

async def test_my_feature():
    inputs = {"messages": [{"role": "user", "content": "测试"}]}
    res = await graph.ainvoke(inputs)
    assert res is not None
```

### 6.3 代码质量

#### 6.3.1 格式化和检查
```bash
# Ruff 检查
ruff check src/ tests/

# Ruff 自动修复
ruff check --fix src/ tests/

# MyPy 类型检查
mypy src/
```

#### 6.3.2 CI/CD
项目配置了 GitHub Actions：
- `unit-tests.yml`: 每次 push 运行单元测试
- `integration-tests.yml`: 运行集成测试（可选 LangSmith）

---

## 7. 部署指南

### 7.1 LangGraph Server 部署

项目已配置好 `langgraph.json`，可以直接部署到 LangGraph Cloud 或自托管。

#### 7.1.1 本地生产运行
```bash
langgraph up
```

#### 7.1.2 Docker 部署
参考 LangGraph 官方文档构建镜像。

### 7.2 环境变量清单

| 变量名 | 必填 | 说明 | 示例 |
|-------|------|------|------|
| DEEPSEEK_API_KEY | 是 | DeepSeek API 密钥 | sk-xxxx |
| DEEPSEEK_BASE_URL | 是 | DeepSeek 服务地址 | https://api.deepseek.com |
| ARK_API_KEY | 否 | Ark API 密钥 | - |
| ARK_BASE_URL | 否 | Ark 服务地址 | - |
| MYSQL_CONNECTION | 否 | MySQL 连接串 | mysql://... |
| LANGSMITH_API_KEY | 否 | LangSmith 追踪密钥 | lsv2_... |

---

## 8. 监控与调试

### 8.1 LangSmith 追踪

启用 LangSmith 可以详细追踪代理执行：

1. 在 `.env` 中添加：
```env
LANGSMITH_API_KEY=lsv2_your_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=langgraph-demo
```

2. 访问 https://smith.langchain.com 查看追踪

### 8.2 日志调试

在工具中添加打印语句：
```python
@tool
def my_tool(param):
    print(f"[调试] 接收到参数: {param}")
    result = do_something(param)
    print(f"[调试] 返回结果: {result}")
    return result
```

---

## 9. 最佳实践

### 9.1 工具设计
1. ✅ 每个工具只做一件事（单一职责）
2. ✅ 使用清晰的参数名称和描述
3. ✅ 提供完整的类型注解
4. ✅ 处理异常情况
5. ✅ 保持工具函数纯净化

### 9.2 提示词设计
1. ✅ 明确角色定位
2. ✅ 列出可用工具
3. ✅ 给出输出格式要求
4. ✅ 提供示例（Few-shot）
5. ✅ 约束行为边界

### 9.3 代码组织
1. ✅ 工具按功能分类
2. ✅ 配置与代码分离
3. ✅ 测试覆盖核心逻辑
4. ✅ 保持提交历史清晰
5. ✅ 使用语义化版本

---

## 10. 常见问题

### Q1: 如何添加记忆功能？
A: LangGraph 的 StateGraph 天然支持状态管理，可以通过扩展 State 添加记忆。

### Q2: 如何实现多轮对话？
A: 使用相同的 thread_id 即可保持对话上下文，LangGraph Server 会自动管理。

### Q3: 工具调用失败怎么办？
A: 在工具中添加 try-catch，返回友好的错误信息，LLM 会根据错误重新尝试。

### Q4: 如何限制工具调用次数？
A: 可以自定义图结构，在节点中添加计数器逻辑。

---

## 11. 参考资源

- 📚 [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
- 📚 [LangGraph Server 指南](https://langchain-ai.github.io/langgraph/concepts/langgraph_server/)
- 📚 [LangGraph Studio](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/)
- 📚 [LangSmith 文档](https://docs.smith.langchain.com/)
- 📚 [工具调用最佳实践](https://python.langchain.com/docs/modules/tools/)

---

## 12. 版本历史

| 版本 | 日期 | 变更说明 |
|-----|------|---------|
| 0.0.1 | 2026-04-13 | 初始版本，项目结构重组 |

---

## 附录

### A. 快速参考命令

```bash
# 开发
langgraph dev          # 启动开发服务器
langgraph up           # 启动生产服务器

# 测试
pytest                 # 运行所有测试
pytest -v              # 详细输出
pytest tests/unit_tests/  # 仅单元测试

# 代码质量
ruff check src/        # Ruff 检查
ruff check --fix src/  # Ruff 自动修复
mypy src/              # 类型检查

# 安装
pip install -e .       # 开发模式安装
```

### B. 项目依赖树（核心）

```
agent==0.0.1
├── langgraph>=1.0.0
│   ├── langchain-core
│   └── langgraph-checkpoint
└── python-dotenv>=1.0.1

[dev]
├── pytest>=8.3.5
├── ruff>=0.8.2
├── mypy>=1.13.0
├── anyio>=4.7.0
└── langgraph-cli>=0.4.14
```

---

**文档结束**

如有问题或建议，请联系项目维护者。
