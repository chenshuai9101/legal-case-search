# 法律类案检索系统 (Legal Case Search)

专业的法律类案检索与报告生成工具，为律师、法律从业者提供分钟级类案检索服务。

## 功能特性

### 🔍 类案检索
- 语义检索：自然语言查询，无需精确关键词
- 多维度筛选：地域、法院、案件类型、时间范围
- 智能排序：基于TF-IDF和语义相似度

### 📊 案例分析
- 裁判要点自动提取
- 胜诉率统计分析
- 裁判趋势分析

### 📝 报告生成
- 标准版报告：适用于日常办案参考
- 详细版报告：符合法院提交格式要求
- 摘要版报告：快速概览

## 安装使用

```bash
# 克隆项目
git clone https://github.com/chenshuai9101/legal-case-search.git
cd legal-case-search

# 安装依赖
pip install -r requirements.txt

# 运行检索测试
python scripts/search_engine.py

# 生成报告示例
python scripts/report_generator.py
```

## 快速开始

```python
from scripts.search_engine import search_cases, analyze_case
from scripts.report_generator import generate_report

# 1. 类案检索
results = search_cases(
    query="建设工程施工合同纠纷 拖欠工程款",
    filters={
        'court': '最高人民法院',
        'case_area': '合同纠纷',
        'date_range': ('2020-01-01', '2023-12-31')
    },
    limit=10
)

# 2. 案例详情分析
case_detail = analyze_case(results[0]['case_id'])

# 3. 生成检索报告
report = generate_report(results, template='detailed')
print(report)
```

## 报告模板

| 模板类型 | 适用场景 | 特点 |
|---------|---------|------|
| standard | 日常办案参考 | 结构清晰，要点突出 |
| detailed | 法院提交/学术研究 | 全面详尽，格式规范 |
| summary | 快速预览 | 简洁精炼，要言不烦 |

## 数据来源

- 中国裁判文书网
- 最高人民法院案例库
- 各地方法院公开案例

## 验收标准

| 指标 | 标准 |
|------|------|
| 类案召回率 | ≥85% |
| Top-10命中率 | ≥90% |
| 单次检索耗时 | ≤2分钟 |
| 报告生成耗时 | ≤1分钟 |

## 适用人群

- 🔹 执业律师
- 🔹 法律顾问
- 🔹 企业法务
- 🔹 法学研究人员
- 🔹 司法机关工作人员

## License

MIT License - 详见 [LICENSE](LICENSE) 文件

## 联系方式

如有问题或建议，请提交 Issue 或联系维护者。
