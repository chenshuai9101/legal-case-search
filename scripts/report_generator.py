#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
法律类案检索报告生成器
Legal Case Search Report Generator
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid


class ReportGenerator:
    """检索报告生成器"""
    
    def __init__(self):
        self.templates = {
            'standard': self._standard_template,
            'detailed': self._detailed_template,
            'summary': self._summary_template
        }
    
    def generate_report(self, case_list: List[Dict], template: str = 'standard') -> str:
        """
        生成检索报告
        
        Args:
            case_list: 检索到的案例列表
            template: 报告模板类型 ('standard', 'detailed', 'summary')
        
        Returns:
            格式化的检索报告（Markdown格式）
        """
        if template not in self.templates:
            template = 'standard'
        
        return self.templates[template](case_list)
    
    def _standard_template(self, case_list: List[Dict]) -> str:
        """标准报告模板"""
        report_id = str(uuid.uuid4())[:8]
        current_date = datetime.now().strftime('%Y年%m月%d日')
        
        report = f"""# 类案检索报告

**报告编号**：LCR-{report_id}  
**生成时间**：{current_date}  
**检索案例数**：{len(case_list)} 个

---

## 一、检索概述

本报告基于关键词检索获取 **{len(case_list)}** 个相关案例，涵盖合同纠纷、劳动争议等常见案件类型。

### 1.1 检索结果统计

| 指标 | 数值 |
|------|------|
| 案例总数 | {len(case_list)} |
| 平均相似度 | {sum(c.get('similar_score', 0) for c in case_list) / len(case_list):.1f}% |
| 最高相似度 | {max(c.get('similar_score', 0) for c in case_list):.1f}% |

---

## 二、案例详情

"""
        
        for i, case in enumerate(case_list, 1):
            report += f"""### {i}. {case.get('title', '未命名案例')}

| 项目 | 内容 |
|------|------|
| 案号 | {case.get('case_number', '未知')} |
| 审理法院 | {case.get('court', '未知')} |
| 裁判日期 | {case.get('judge_date', '未知')} |
| 案件类型 | {case.get('case_type', '未知')} / {case.get('case_area', '未知')} |
| 相似度 | {case.get('similar_score', 0)}% |

**案情摘要**：  
{case.get('summary', '暂无')}

**裁判结果**：  
{case.get('judgment', '暂无')}

**裁判要点**：  
"""
            for point in case.get('key_points', []):
                report += f"- {point}\n"
            report += "\n---\n"
        
        report += self._add_footer()
        return report
    
    def _detailed_template(self, case_list: List[Dict]) -> str:
        """详细报告模板（适用于法院提交）"""
        report_id = str(uuid.uuid4())[:8]
        current_date = datetime.now().strftime('%Y年%m月%d日')
        
        report = f"""# 类案检索报告（详细版）

**报告编号**：LCR-{report_id}  
**生成时间**：{current_date}  
**检索案例数**：{len(case_list)} 个  
**报告用途**：供法院提交/学术研究参考

---

## 第一部分 检索背景与目的

本检索报告旨在为案件办理提供类案参考，通过检索最高人民法院及各地方法院公开案例，分析类案裁判要旨，为案件处理提供参考依据。

---

## 第二部分 类案统计概览

"""
        
        # 统计各类案件分布
        case_types = {}
        for case in case_list:
            area = case.get('case_area', '其他')
            case_types[area] = case_types.get(area, 0) + 1
        
        report += "### 2.1 案件类型分布\n\n"
        report += "| 案件类型 | 数量 | 占比 |\n|---------|------|------|\n"
        for area, count in case_types.items():
            pct = count / len(case_list) * 100
            report += f"| {area} | {count} | {pct:.1f}% |\n"
        
        report += "\n### 2.2 相似度分布\n\n"
        high_sim = len([c for c in case_list if c.get('similar_score', 0) >= 80])
        medium_sim = len([c for c in case_list if 50 <= c.get('similar_score', 0) < 80])
        low_sim = len([c for c in case_list if c.get('similar_score', 0) < 50])
        
        report += f"| 相似度等级 | 数量 | 占比 |\n|---------|------|------|\n"
        report += f"| 高相似度 (≥80%) | {high_sim} | {high_sim/len(case_list)*100:.1f}% |\n"
        report += f"| 中相似度 (50-80%) | {medium_sim} | {medium_sim/len(case_list)*100:.1f}% |\n"
        report += f"| 低相似度 (<50%) | {low_sim} | {low_sim/len(case_list)*100:.1f}% |\n"
        
        report += "\n---\n\n## 第三部分 案例详细分析\n\n"
        
        for i, case in enumerate(case_list, 1):
            report += f"""### 3.{i} {case.get('title', '未命名案例')}

**基本信息**

| 项目 | 内容 |
|------|------|
| 案例编号 | {case.get('case_id', '未知')} |
| 案号 | {case.get('case_number', '未知')} |
| 审理法院 | {case.get('court', '未知')} |
| 裁判日期 | {case.get('judge_date', '未知')} |
| 案件类型 | {case.get('case_type', '未知')} / {case.get('case_area', '未知')} |
| 相似度评分 | {case.get('similar_score', 0)}% |

**案情描述**  
{case.get('summary', '暂无')}

**裁判结果**  
{case.get('judgment', '暂无')}

**裁判要点分析**

"""
            for j, point in enumerate(case.get('key_points', []), 1):
                report += f"{j}. {point}\n"
            
            report += f"""
**适用法律分析**  
本案体现了以下法律原则：
- 合同严守原则
- 过错责任原则
- 损失填补原则

---
"""
        
        report += "\n## 第四部分 检索结论与建议\n\n"
        report += "### 4.1 类案裁判倾向\n\n"
        report += "通过分析上述类案，可以看出法院在处理此类案件时具有以下倾向：\n\n"
        report += "1. **注重合同约定**：在合同纠纷中，法院会优先尊重当事人之间的约定\n"
        report += "2. **强调证据规则**：当事人应当提供充分证据证明其主张\n"
        report += "3. **保护守约方**：在违约情形下，法院通常会保护守约方的合法权益\n\n"
        
        report += "### 4.2 办案建议\n\n"
        report += "基于类案检索结果，提出以下建议：\n\n"
        report += "1. 建议收集和保存完整的合同文本及履行证据\n"
        report += "2. 注意诉讼时效，避免权利失效\n"
        report += "3. 如有需要，可申请诉讼财产保全\n\n"
        
        report += self._add_footer()
        return report
    
    def _summary_template(self, case_list: List[Dict]) -> str:
        """简版报告模板（快速概览）"""
        current_date = datetime.now().strftime('%Y年%m月%d日')
        
        report = f"""# 类案检索摘要

**日期**：{current_date} | **案例数**：{len(case_list)}

"""
        
        for i, case in enumerate(case_list[:5], 1):
            report += f"""### {i}. {case.get('title', '未命名')}
- 案号：{case.get('case_number', '未知')} | 法院：{case.get('court', '未知')}
- 相似度：{case.get('similar_score', 0)}%
- 要点：{'；'.join(case.get('key_points', [])[:2])}

"""
        
        report += self._add_footer()
        return report
    
    def _add_footer(self) -> str:
        """添加报告页脚"""
        return """
---

## 声明

本报告仅供参考使用，不作为法律意见。案例数据来源于公开裁判文书，实际适用时请结合具体案情判断。

**生成工具**：法律类案检索系统 v1.0  
**生成时间**：{time}
""".format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


# 全局报告生成器实例
_generator = ReportGenerator()


def generate_report(case_list: List[Dict], template: str = 'standard') -> str:
    """
    生成检索报告接口
    
    Args:
        case_list: 检索到的案例列表
        template: 报告模板 ('standard', 'detailed', 'summary')
    
    Returns:
        格式化的报告（Markdown格式）
    """
    return _generator.generate_report(case_list, template)


if __name__ == "__main__":
    # 测试报告生成
    from search_engine import search_cases
    
    # 检索案例
    cases = search_cases("建设工程合同纠纷 拖欠工程款", limit=3)
    
    # 生成标准报告
    print("=== 生成标准报告 ===\n")
    report = generate_report(cases, 'standard')
    print(report[:500] + "...")
    
    # 生成详细报告
    print("\n\n=== 生成详细报告 ===\n")
    report = generate_report(cases, 'detailed')
    print(report[:500] + "...")
