import os
import re
from pathlib import Path

# 配置：HTML 文件路径、README 路径、生成列表的标记
HTML_DIR = "."  # 扫描当前目录的 HTML 文件
README_PATH = "README.md"
# 用于替换的标记（README 中用这个标记包裹自动生成的内容）
START_MARKER = "<!-- AUTO-GENERATED-LIST:START -->"
END_MARKER = "<!-- AUTO-GENERATED-LIST:END -->"

def get_app_name(html_file):
    """从 HTML 文件名或内容中提取应用名"""
    # 方案1：从文件名提取（如 "rungo-privacy.html" → "RunGo"）
    file_name = os.path.basename(html_file)
    app_name = re.sub(r"-privacy\.html$", "", file_name).replace("-", " ").title()
    
    # 方案2（可选）：从 HTML 的 <title> 标签提取（更准确）
    # try:
    #     with open(html_file, "r", encoding="utf-8") as f:
    #         content = f.read()
    #         title_match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
    #         if title_match:
    #             app_name = title_match.group(1).replace("隐私协议", "").strip()
    # except:
    #     pass
    
    return app_name

def generate_readme():
    # 1. 扫描所有 HTML 文件（排除 README 中不需要的文件）
    html_files = [f for f in os.listdir(HTML_DIR) 
                 if f.endswith(".html") 
                 and not f.startswith("index")  # 排除主页（如果有的话）
                 and os.path.isfile(f)]
    
    # 2. 生成应用列表 Markdown
    if not html_files:
        app_list = "暂无隐私政策文件，请添加 HTML 文件到仓库。"
    else:
        app_list = "\n".join([
            f"- [{get_app_name(file)}]({file})" 
            for file in sorted(html_files)  # 按文件名排序
        ])
    
    # 3. 读取原 README 内容，替换自动生成部分
    with open(README_PATH, "r", encoding="utf-8") as f:
        readme_content = f.read()
    
    # 替换标记之间的内容
    new_content = re.sub(
        f"{START_MARKER}.*?{END_MARKER}",
        f"{START_MARKER}\n{app_list}\n{END_MARKER}",
        readme_content,
        flags=re.DOTALL
    )
    
    # 4. 写入更新后的 README
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README 自动更新完成！")

if __name__ == "__main__":
    generate_readme()