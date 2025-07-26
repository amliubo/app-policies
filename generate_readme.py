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

        match = re.match(r"(.+?)-(privacy|user-agreement|support)\.html$", file)
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
        support = f"[技术支持]({items['support']})" if "support" in items else "*无技术支持*"
        lines.append(f"- **{app}**: {privacy} ｜ {user_agreement} ｜ {support}")
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
  <title>协议合集</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
      margin: 0;
      padding: 0;
      background-color: #f7f7f8;
      color: #333;
      font-size: 15px;
      line-height: 1.6;
    }

    .container {
      max-width: 720px;
      margin: 40px auto;
      background: #fff;
      padding: 32px 24px;
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    h1 {
      font-size: 22px;
      color: #222;
      margin-bottom: 24px;
      text-align: center;
    }

    .app-entry {
      margin-bottom: 20px;
      padding: 16px 20px;
      background: #fafafa;
      border: 1px solid #eee;
      border-radius: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
    }

    .app-name {
      font-weight: 600;
      font-size: 16px;
      margin-bottom: 8px;
    }

    .links a {
      margin-right: 16px;
      color: #007aff;
      text-decoration: none;
      font-size: 14px;
    }

    .links a:last-child {
      margin-right: 0;
    }

    .footer {
      text-align: center;
      margin-top: 40px;
      font-size: 13px;
      color: #888;
    }

    @media (max-width: 500px) {
      .app-entry {
        flex-direction: column;
        align-items: flex-start;
      }
      .links {
        margin-top: 6px;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>应用隐私与用户协议合集</h1>
"""

    for app, items in policies.items():
        html += '    <div class="app-entry">\n'
        html += f'      <div class="app-name">{app}</div>\n'
        html += '      <div class="links">\n'
        if "privacy" in items:
            html += f'        <a href="{items["privacy"]}">隐私政策</a>\n'
        else:
            html += f'        <span style="color:#aaa;">无隐私政策</span>\n'
        if "user-agreement" in items:
            html += f'        <a href="{items["user-agreement"]}">用户协议</a>\n'
        else:
            html += f'        <span style="color:#aaa;">无用户协议</span>\n'
        if "support" in items:
            html += f'        <a href="{items["support"]}">技术支持</a>\n'
        else:
            html += f'        <span style="color:#aaa;">无技术支持</span>\n'
        html += '      </div>\n'
        html += '    </div>\n'

    html += """
    <div class="footer">
      本页面由脚本自动生成！
    </div>
  </div>
</body>
</html>
"""
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ index.html 已生成")


if __name__ == "__main__":
    policies = find_policies()
    readme_text = generate_readme(policies)
    update_readme(readme_text)
    generate_index(policies)
