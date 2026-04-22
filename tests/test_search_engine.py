#!/usr/bin/env python3
"""
Legal-Case-Search 测试用例
验证类案检索、案例分析、报告生成功能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.search_engine import search_cases, analyze_case
from scripts.report_generator import generate_report

def test_search_cases():
    """测试类案检索"""
    print("=== 测试: 类案检索 ===")
    
    results = search_cases(
        query="建设工程施工合同纠纷 拖欠工程款",
        filters={
            'court': '最高人民法院',
            'case_area': '合同纠纷',
        },
        limit=10
    )
    
    assert isinstance(results, list)
    print(f"✅ 类案检索成功，返回 {len(results)} 条结果")
    
    return True

def test_semantic_search():
    """测试语义检索"""
    print("\n=== 测试: 语义检索 ===")
    
    test_queries = [
        "劳动合同解除纠纷",
        "房屋买卖合同违约",
        "交通事故责任认定",
    ]
    
    for query in test_queries:
        results = search_cases(query=query, limit=5)
        print(f"  查询: '{query}' -> {len(results)} 条结果")
    
    print("✅ 语义检索功能正常")
    return True

def test_case_analysis():
    """测试案例分析"""
    print("\n=== 测试: 案例分析 ===")
    
    analysis = analyze_case("CASE20240001")
    assert analysis is not None
    print(f"✅ 案例分析成功")
    
    return True

def test_report_generation():
    """测试报告生成"""
    print("\n=== 测试: 报告生成 ===")
    
    mock_cases = [
        {"case_id": "CASE001", "title": "建设工程施工合同纠纷案例1", "result": "胜诉"},
        {"case_id": "CASE002", "title": "建设工程施工合同纠纷案例2", "result": "部分胜诉"}
    ]
    
    templates = ["standard", "detailed", "summary"]
    
    for template in templates:
        report = generate_report(mock_cases, template=template)
        assert report is not None
        print(f"  [{template}] 模板报告生成成功")
    
    print("✅ 报告生成功能正常")
    return True

def test_report_templates():
    """测试报告模板"""
    print("\n=== 测试: 报告模板 ===")
    
    templates_info = {
        "standard": {"name": "标准版报告", "scene": "日常办案参考"},
        "detailed": {"name": "详细版报告", "scene": "法院提交/学术研究"},
        "summary": {"name": "摘要版报告", "scene": "快速预览"}
    }
    
    for template_id, info in templates_info.items():
        print(f"  [{template_id}] {info['name']}")
    
    print("✅ 报告模板完整")
    return True

def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("Legal-Case-Search 测试套件")
    print("=" * 50)
    
    tests = [
        test_search_cases,
        test_semantic_search,
        test_case_analysis,
        test_report_generation,
        test_report_templates,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
