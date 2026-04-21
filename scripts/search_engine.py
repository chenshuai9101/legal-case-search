#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
法律类案检索引擎
Legal Case Search Engine
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class Case:
    """案例数据结构"""
    case_id: str
    case_number: str
    title: str
    court: str
    judge_date: str
    case_type: str
    case_area: str
    content: str
    judgment: str
    key_points: List[str]
    similar_score: float = 0.0


class LegalSearchEngine:
    """法律类案检索引擎"""
    
    def __init__(self):
        self.cases: List[Case] = []
        self._load_sample_cases()
    
    def _load_sample_cases(self):
        """加载示例案例库"""
        self.cases = [
            Case(
                case_id="case_001",
                case_number="(2023)最高法民终1234号",
                title="建设工程施工合同纠纷案",
                court="最高人民法院",
                judge_date="2023-06-15",
                case_type="民事",
                case_area="合同纠纷",
                content="原告与被告签订建设工程施工合同，因工程款支付问题产生争议...",
                judgment="支持原告诉求，判决被告支付工程款及利息",
                key_points=[
                    "建设工程合同应当采用书面形式",
                    "工程款支付应以竣工验收合格为前提",
                    "逾期付款应支付相应利息"
                ]
            ),
            Case(
                case_id="case_002",
                case_number="(2023)沪01民终5678号",
                title="房屋买卖合同纠纷案",
                court="上海市第一中级人民法院",
                judge_date="2023-05-20",
                case_type="民事",
                case_area="合同纠纷",
                content="买受人购买房屋后，发现房屋存在质量问题...",
                judgment="判决解除合同，返还购房款",
                key_points=[
                    "房屋质量不符合约定标准可以解除合同",
                    "出卖人应当承担瑕疵担保责任",
                    "买受人有权要求返还购房款及赔偿损失"
                ]
            ),
            Case(
                case_id="case_003",
                case_number="(2022)京03民终9012号",
                title="劳动争议纠纷案",
                court="北京市第三中级人民法院",
                judge_date="2022-11-10",
                case_type="民事",
                case_area="劳动争议",
                content="劳动者与用人单位因解除劳动合同经济补偿金问题产生争议...",
                judgment="判决用人单位支付经济补偿金",
                key_points=[
                    "用人单位违法解除劳动合同应支付赔偿金",
                    "经济补偿金按工作年限计算",
                    "劳动者有权主张双倍赔偿"
                ]
            ),
            Case(
                case_id="case_004",
                case_number="(2023)粤01刑初345号",
                title="合同诈骗案",
                court="广州市中级人民法院",
                judge_date="2023-04-18",
                case_type="刑事",
                case_area="经济犯罪",
                content="被告人以非法占有为目的，在签订合同过程中骗取对方财物...",
                judgment="判处有期徒刑十年，并处罚金",
                key_points=[
                    "合同诈骗罪以非法占有为目的",
                    "虚构事实或隐瞒真相是构成要件",
                    "涉案金额影响量刑档次"
                ]
            ),
            Case(
                case_id="case_005",
                case_number="(2023)浙02行初78号",
                title="行政处罚复议案",
                court="宁波市中级人民法院",
                judge_date="2023-07-22",
                case_type="行政",
                case_area="行政处罚",
                content="原告不服行政机关作出的行政处罚决定，申请行政复议...",
                judgment="维持原行政处罚决定",
                key_points=[
                    "行政处罚应当事实清楚、证据充分",
                    "程序合法是行政行为有效的要件",
                    "当事人享有陈述申辩权"
                ]
            )
        ]
    
    def _calculate_similarity(self, query: str, case: Case) -> float:
        """计算查询与案例的语义相似度"""
        query_keywords = self._extract_keywords(query)
        case_keywords = self._extract_keywords(case.title + " " + case.content)
        
        # 计算交集
        common = set(query_keywords) & set(case_keywords)
        if not common:
            return 0.0
        
        # TF-IDF风格相似度计算
        score = len(common) / len(query_keywords) * 0.6
        score += len(common) / len(case_keywords) * 0.4
        
        # 标题匹配加权
        if any(kw in case.title for kw in query_keywords):
            score *= 1.2
        
        return min(score, 1.0)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 法律领域常用词
        stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '与'}
        
        # 简单分词
        words = re.findall(r'[\u4e00-\u9fa5]+', text)
        keywords = [w for w in words if len(w) >= 2 and w not in stop_words]
        
        # 法律专业术语加权
        legal_terms = ['合同', '纠纷', '判决', '赔偿', '责任', '权利', '义务', '侵权', '违约', '解除', '支付', '建设工程', '劳动', '刑事', '行政']
        for term in legal_terms:
            if term in text:
                keywords.extend([term] * 2)
        
        return keywords
    
    def _apply_filters(self, cases: List[Case], filters: Dict[str, Any]) -> List[Case]:
        """应用筛选条件"""
        result = cases
        
        if filters.get('court'):
            court = filters['court']
            result = [c for c in result if court in c.court]
        
        if filters.get('case_area'):
            area = filters['case_area']
            result = [c for c in result if area in c.case_area]
        
        if filters.get('case_type'):
            case_type = filters['case_type']
            result = [c for c in result if case_type == c.case_type]
        
        if filters.get('date_range'):
            start, end = filters['date_range']
            result = [c for c in result if start <= c.judge_date <= end]
        
        return result
    
    def search_cases(self, query: str, filters: Optional[Dict] = None, limit: int = 10) -> List[Dict]:
        """
        类案检索
        
        Args:
            query: 自然语言查询，如"建设工程施工合同纠纷 拖欠工程款"
            filters: 筛选条件 {'court': '北京', 'case_area': '合同纠纷', 'date_range': ('2020-01-01', '2023-12-31')}
            limit: 返回结果数量限制
        
        Returns:
            检索结果列表，按相似度降序排列
        """
        filters = filters or {}
        
        # 1. 语义检索
        for case in self.cases:
            case.similar_score = self._calculate_similarity(query, case)
        
        # 2. 筛选
        filtered = self._apply_filters(self.cases, filters)
        
        # 3. 排序
        sorted_cases = sorted(filtered, key=lambda x: x.similar_score, reverse=True)
        
        # 4. 截取并返回
        results = []
        for case in sorted_cases[:limit]:
            result = {
                'case_id': case.case_id,
                'case_number': case.case_number,
                'title': case.title,
                'court': case.court,
                'judge_date': case.judge_date,
                'case_type': case.case_type,
                'case_area': case.case_area,
                'summary': case.content[:100] + '...' if len(case.content) > 100 else case.content,
                'judgment': case.judgment,
                'key_points': case.key_points,
                'similar_score': round(case.similar_score * 100, 2)
            }
            results.append(result)
        
        return results
    
    def analyze_case(self, case_id: str) -> Optional[Dict]:
        """
        案例分析
        
        Args:
            case_id: 案例ID
        
        Returns:
            案例详细分析
        """
        case = next((c for c in self.cases if c.case_id == case_id), None)
        if not case:
            return None
        
        # 统计该类型案件的胜诉率（模拟数据）
        win_rate = 65.5
        
        # 裁判趋势分析（模拟数据）
        trend = {
            'favor_plaintiff': 0.55,
            'favor_defendant': 0.35,
            'compromise': 0.10
        }
        
        return {
            'case_id': case.case_id,
            'case_number': case.case_number,
            'title': case.title,
            'court': case.court,
            'judge_date': case.judge_date,
            'case_type': case.case_type,
            'case_area': case.case_area,
            'full_content': case.content,
            'judgment': case.judgment,
            'key_points': case.key_points,
            'statistics': {
                'win_rate': win_rate,
                'trend': trend
            },
            'legal_basis': self._extract_legal_basis(case)
        }
    
    def _extract_legal_basis(self, case: Case) -> List[str]:
        """提取法律依据"""
        # 模拟法律依据
        basis_map = {
            '合同纠纷': ['《中华人民共和国民法典》第五百零九条', '《中华人民共和国民法典》第五百七十七条'],
            '劳动争议': ['《中华人民共和国劳动法》第四十四条', '《中华人民共和国劳动合同法》第四十六条'],
            '经济犯罪': ['《中华人民共和国刑法》第二百二十四条', '《中华人民共和国刑法》第六十四条'],
            '行政处罚': ['《中华人民共和国行政处罚法》第三十二条', '《中华人民共和国行政复议法》第二十八条']
        }
        
        return basis_map.get(case.case_area, ['《中华人民共和国民法典》第一百一十九条'])
    
    def get_search_stats(self) -> Dict:
        """获取检索统计信息"""
        return {
            'total_cases': len(self.cases),
            'case_types': list(set(c.case_type for c in self.cases)),
            'case_areas': list(set(c.case_area for c in self.cases)),
            'courts': list(set(c.court for c in self.cases))
        }


# 全局检索引擎实例
_engine = LegalSearchEngine()


def search_cases(query: str, filters: Optional[Dict] = None, limit: int = 10) -> List[Dict]:
    """
    类案检索接口
    
    Args:
        query: 自然语言查询，如"建设工程施工合同纠纷 拖欠工程款"
        filters: 筛选条件
        limit: 返回结果数量
    
    Returns:
        检索结果列表
    """
    return _engine.search_cases(query, filters, limit)


def analyze_case(case_id: str) -> Optional[Dict]:
    """
    案例分析接口
    
    Args:
        case_id: 案例ID
    
    Returns:
        案例详细分析
    """
    return _engine.analyze_case(case_id)


def get_search_stats() -> Dict:
    """获取检索统计"""
    return _engine.get_search_stats()


if __name__ == "__main__":
    # 测试检索
    print("=== 法律类案检索测试 ===\n")
    
    # 1. 测试语义检索
    results = search_cases("建设工程合同纠纷 拖欠工程款", limit=3)
    print(f"检索到 {len(results)} 个相关案例:")
    for i, r in enumerate(results, 1):
        print(f"\n{i}. {r['title']}")
        print(f"   案号: {r['case_number']}")
        print(f"   法院: {r['court']}")
        print(f"   相似度: {r['similar_score']}%")
        print(f"   裁判要点: {r['key_points'][:2]}")
    
    # 2. 测试案例分析
    print("\n\n=== 案例分析测试 ===")
    analysis = analyze_case("case_001")
    if analysis:
        print(f"\n案例: {analysis['title']}")
        print(f"胜诉率统计: {analysis['statistics']['win_rate']}%")
        print(f"法律依据: {analysis['legal_basis']}")
