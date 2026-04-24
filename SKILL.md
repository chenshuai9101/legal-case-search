---
name: legal-case-search
description: 为法律从业者提供专业的类案检索服务，支持语义检索、地域/法院筛选、时间范围筛选和案件类型筛选
metadata:
  openclaw:
    emoji: ⚖️
    aiFriendly: true
    plugAndPlay: true
    requires:
      minimal: true
      packages: ['python>=3.8', 'requests', 'beautifulsoup4', 'elasticsearch']
    category: legal
    tags: ['legal', 'case-search', 'law', 'document-analysis', 'research']
version: 1.0.0
---

# Legal Case Search

## 安装与兼容性

### 支持的平台
- ✅ **Claude Code** (v0.7.0+)
- ✅ **OpenClaw** (v1.0.0+)
- ✅ **Codex CLI** (latest)
- ✅ **Cursor** (latest)
- 🟡 **Claude Desktop** - 需要手动复制 SKILL.md 到项目目录

### 安装方式

**方式一：自动安装 (推荐)**
```bash
# Claude Code
claude mcp add <repo-name> -- npx skills add chenshuai9101/<repo-name>

# OpenClaw
clawhub install chenshuai9101/<repo-name>

# 或直接克隆
git clone https://github.com/chenshuai9101/<repo-name>.git
```

**方式二：手动安装**
```bash
# 复制到目标项目
cp -r <repo-name>/* /your-project/.claude/skills/
```

**方式三：通过Claude Code Marketplace安装**
```json
{
  "skills": ["chenshuai9101/<repo-name>"]
}
```


## 一、AI/Agent友好型设计

### 1.1 标准化的输入输出格式

**输入格式**：
```json
{
  "operation": "要执行的操作",
  "data": "输入数据",
  "options": {},
  "metadata": {
    "request_id": "唯一请求ID",
    "callback_url": "可选回调URL"
  }
}
```

**输出格式**：
```json
{
  "status": "success|error|processing",
  "result": "处理结果",
  "metadata": {
    "processing_time_ms": 123,
    "resource_usage": {
      "memory_mb": 128,
      "cpu_percent": 15.5
    }
  },
  "errors": [],
  "warnings": []
}
```

### 1.2 错误处理规范
- 使用标准化的错误代码
- 提供详细的错误信息
- 支持错误恢复机制
- 包含调试信息

### 1.3 进度反馈机制
- 支持实时进度更新
- 可配置的更新频率
- 进度回调接口
- 任务取消支持

## 二、开箱即用状态

### 2.1 最小化依赖
- 核心依赖：Python 3.8+
- 可选依赖：按需安装
- 自动依赖检测
- 一键安装脚本

### 2.2 自动环境配置
```bash
# 一键安装脚本
./install.sh

# 或使用pip
pip install legal-case-search
```

### 2.3 自包含配置
```yaml
# config.yaml
legal-case-search:
  enabled: true
  performance:
    cache_enabled: true
    max_workers: 4
  logging:
    level: INFO
    file: "./logs/legal-case-search.log"
```

## 三、核心功能

### 3.1 主要功能
根据具体skill的功能进行描述

### 3.2 使用示例
```python
from legal_case_search import SkillAPI

# 初始化
skill = SkillAPI()

# 基本使用
result = skill.process({"data": "输入数据"})

print(f"处理结果: {result}")
```

## 四、API参考

### 4.1 REST API端点
- `POST /api/v1/process` - 处理请求
- `GET /api/v1/status/:task_id` - 获取任务状态
- `GET /api/v1/health` - 健康检查

### 4.2 Python API
```python
class SkillAPI:
    def process(self, input_data, options=None):
        '''处理输入数据'''
        
    def batch_process(self, inputs, options=None):
        '''批量处理'''
        
    async def process_async(self, input_data, options=None):
        '''异步处理'''
```

## 五、部署指南

### 5.1 Docker部署
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

### 5.2 监控与维护
- 健康检查：`/health`
- 性能指标：`/metrics`
- 日志管理
- 自动备份

## 六、更新日志

### v1.0.0
- 初始版本发布
- 支持AI/Agent友好型设计
- 实现开箱即用状态
- 提供完整的API文档


## 边界声明

### NOT FOR （不要使用此skill处理以下内容）
- 通用的代码开发任务（请使用编码技能）
- 跨平台文件格式转换（请使用doc-processor或media-toolkit）
- 不具备完整输入数据的情况（请先提供数据）
- 实时数据流处理（本skill为batch处理模式）
- 需要专有API密钥但未配置的场景

### 触发词
- 当用户明确要求使用本skill的领域时
- 当用户提供的数据格式与本skill输入规范匹配时
- 不主动触发：当用户仅询问一般性问题时

### 输出保证
- 所有输出均包含错误处理信息
- 失败时提供明确的错误原因和修复建议
- 逐步回退：`最佳模型 → 备用模型 → 确定性降级`


## 结构化输出兼容性指南

本skill依赖LLM的结构化输出能力。以下是为确保稳定性的建议：

### 如果遇到JSON解析错误

1. **使用支持JSON Schema的模型**: gpt-4o, claude-sonnet-4, claude-haiku-3.5
2. **本地模型用户**: 
   - 使用 `qwen2.5-instruct` (7B/14B+) 或 `mistral-large` 或 `command-r-plus`
   - 在prompt中要求纯JSON输出，不加markdown包裹
3. **中转代理用户**:
   - 确保中转层不过滤 `thinking` 过程的 `<thinking>` 标签
   - 如果包含thinking过程，要求模型去除后重新输出

### 自动修复逻辑

如果LLM返回的JSON格式有误，按以下顺序修复:
```python
def safe_parse_json(raw_text: str) -> dict:
    import json, re
    # Step 1: 提取JSON块
    json_match = re.search(r'```(?:json)?\n(.*?)\n```', raw_text, re.DOTALL)
    if json_match:
        raw_text = json_match.group(1)
    # Step 2: 替换全角符号
    raw_text = raw_text.replace('"', '"').replace('"', '"').replace("'", "'")
    raw_text = raw_text.replace('，', ',').replace('：', ':')
    # Step 3: 去除尾部逗号
    raw_text = re.sub(r',\s*}', '}', raw_text)
    raw_text = re.sub(r',\s+\]', ']', raw_text)
    # Step 4: 尝试修复
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        # 最终降级: 使用ast.literal_eval或报错带原始文本
        import ast
        try:
            return ast.literal_eval(raw_text)
        except:
            raise ValueError(f"JSON解析失败。原始文本:\n{raw_text[:500]}")
```


## 快速上手

### 一分钟开始使用

```bash
# 1. 准备输入数据（JSON格式）
cat > input.json << 'EOF'
{
  "operation": "process",
  "data": "<你的数据>",
  "options": {
    "model": "auto",
    "retry_on_fail": true
  }
}
EOF

# 2. 直接输出结果
# （本skill会自动识别输入格式并处理）

# 3. 查看工作流程
# - 步骤1: 验证输入数据完整性
# - 步骤2: 选择最优处理策略
# - 步骤3: 执行处理并输出结果
# - 步骤4: 错误检查与自动修复
```

### 完整工作流示例

```
输入示例 → 数据验证 → 策略选择 → 错误保护 → 结构化输出 → 质量检查 → 最终输出
```
