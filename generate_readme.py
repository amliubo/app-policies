import os
import re
from pathlib import Path

README_PATH = "README.md"
INDEX_PATH = "index.html"
HTML_DIR = "."

START_MARKER = "<!-- AUTO-GENERATED-LIST:START -->"
END_MARKER = "<!-- AUTO-GENERATED-LIST:END -->"

def find_policies():
    """扫描所有 HTML 文件并整理出应用名及其协议链接"""
    policies = {}

    for file in os.listdir(HTML_DIR):
        if not file.endswith(".html") or file.startswith("index"):
            continue

        match = re.match(r"(.+?)-(privacy|user-agreement)\.html$", file)
        if match:
            app_key, policy_type = match.groups()
            app_name = app_key.replace("-", " ").title()
            if app_name not in policies:
                policies[app_name] = {}
            policies[app_name][policy_type] = file

    return dict(sorted(policies.items()))

def generate_readme(policies):
    lines = []
    for app, items in policies.items():
        privacy = f"[隐私协议]({items['privacy']})" if "privacy" in items else "*无隐私协议*"
        user_agreement = f"[用户协议]({items['user-agreement']})" if "user-agreement" in items else "*无用户协议*"
        lines.append(f"- **{app}**: {privacy} ｜ {user_agreement}")
    return "\n".join(lines)

def update_readme(auto_text):
    if not os.path.exists(README_PATH):
        print("❌ 未找到 README.md，跳过更新")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    updated = re.sub(
        f"{START_MARKER}.*?{END_MARKER}",
        f"{START_MARKER}\n{auto_text}\n{END_MARKER}",
        content,
        flags=re.DOTALL
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated)
    print("✅ README.md 已更新")

def generate_index(policies):
    html = """<!DOCTYPE html>
        <html lang="zh">
        <head>
        <meta charset="UTF-8">
        <title>隐私与用户协议合集</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: sans-serif; padding: 40px; max-width: 700px; margin: auto; line-height: 1.6; }
            h1 { color: #007AFF; }
            ul { padding-left: 1em; }
            a { text-decoration: none; color: #007AFF; }
            li { margin-bottom: 1em; }
        </style>
        </head>
        <body>
        <h1>应用隐私协议 / 用户协议列表</h1>
        <ul>
        """
    for app, items in policies.items():
        html += f'    <li><strong>{app}</strong>: '
        html += f'<a href="{items["privacy"]}">隐私协议</a> ｜ ' if "privacy" in items else "无隐私协议 ｜ "
        html += f'<a href="{items["user-agreement"]}">用户协议</a>' if "user-agreement" in items else "无用户协议"
        html += "</li>\n"

    html += """  </ul>
  <p style="margin-top: 2em; font-size: 0.9em; color: gray;">本页面自动生成，用于展示各应用协议文件。</p>
</body>
</html>"""

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ index.html 已生成")

if __name__ == "__main__":
    policies = find_policies()
    readme_text = generate_readme(policies)
    update_readme(readme_text)
    generate_index(policies)
