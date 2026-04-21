#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub仓库推送脚本
使用GitHub Personal Access Token进行认证

使用方法:
    export GITHUB_TOKEN="your_pat_token_here"
    python push_to_github.py
"""

import base64
import os
import requests
from pathlib import Path

# 从环境变量获取Token
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO_OWNER = "chenshuai9101"
REPO_NAME = "legal-case-search"
GITHUB_API = "https://api.github.com"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}


def get_file_sha(path):
    """获取文件SHA"""
    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get('sha')
    return None


def upload_file(path, content):
    """上传文件到GitHub"""
    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
    sha = get_file_sha(path)
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    
    data = {
        "message": f"Add {path}",
        "content": encoded_content
    }
    if sha:
        data["sha"] = sha
    
    response = requests.put(url, headers=HEADERS, json=data)
    
    if response.status_code in [200, 201]:
        print(f"  ✓ {path}")
        return True
    else:
        print(f"  ✗ {path}: {response.status_code}")
        return False


def push_to_github():
    """推送项目到GitHub"""
    if not GITHUB_TOKEN:
        print("错误: 请设置环境变量 GITHUB_TOKEN")
        print("  export GITHUB_TOKEN='your_token_here'")
        return False
    
    print("=" * 50)
    print("法律类案检索系统 - GitHub推送")
    print("=" * 50)
    
    # 扫描文件
    print("\n[1/2] 扫描本地文件...")
    project_root = Path(".")
    files_to_upload = []
    
    for file_path in project_root.rglob("*"):
        if file_path.is_file() and '__pycache__' not in str(file_path):
            rel_path = file_path.relative_to(project_root)
            if rel_path.suffix in ['.md', '.py', '.txt']:
                files_to_upload.append(str(rel_path))
    
    print(f"  发现 {len(files_to_upload)} 个文件")
    
    # 上传文件
    print("\n[2/2] 上传文件到GitHub...")
    success_count = 0
    
    for file_path in files_to_upload:
        full_path = project_root / file_path
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if upload_file(file_path, content):
            success_count += 1
    
    # 完成
    print("\n" + "=" * 50)
    print(f"推送完成！成功 {success_count}/{len(files_to_upload)} 个文件")
    print(f"仓库地址: https://github.com/{REPO_OWNER}/{REPO_NAME}")
    print("=" * 50)
    
    return success_count == len(files_to_upload)


if __name__ == "__main__":
    push_to_github()
