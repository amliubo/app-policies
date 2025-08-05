import os
import re
from collections import defaultdict

README_PATH = "README.md"
INDEX_PATH = "index.html"
HTML_DIR = "."

START_MARKER = "<!-- AUTO-GENERATED-LIST:START -->"
END_MARKER = "<!-- AUTO-GENERATED-LIST:END -->"

def find_policies():
    """扫描所有 HTML 文件，构建多语言协议结构"""
    policies = defaultdict(lambda: defaultdict(dict))  # app -> policy_type -> lang -> filename

    for file in os.listdir(HTML_DIR):
        if not file.endswith(".html") or file.startswith("index"):
            continue

        match = re.match(r"(.+?)-(privacy|user-agreement|support)\.(\w+)\.html$", file)
        if match:
            app_key, policy_type, lang = match.groups()
            app_name = app_key.replace("-", " ").title()
            policies[app_name][policy_type][lang] = file

    return dict(sorted(policies.items()))

def generate_readme(policies):
    """生成 README 中的简要列表内容"""
    lines = []
    for app, items in policies.items():
        parts = []
        for policy_type in ["privacy", "user-agreement", "support"]:
            if policy_type in items:
                langs = " / ".join(
                    f"[{lang}]({items[policy_type][lang]})"
                    for lang in sorted(items[policy_type])
                )
                name = {
                    "privacy": "隐私协议",
                    "user-agreement": "用户协议",
                    "support": "技术支持"
                }[policy_type]
                parts.append(f"{name}: {langs}")
            else:
                parts.append(f"*无{policy_type}*")
        lines.append(f"- **{app}**: {' ｜ '.join(parts)}")
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
    """生成 index.html，展示所有协议多语言链接"""
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
    }

    .app-name {
      font-weight: 600;
      font-size: 16px;
      margin-bottom: 8px;
    }

    .links {
      margin-left: 10px;
    }

    .policy-type {
      margin-bottom: 6px;
    }

    .policy-type span {
      font-weight: 500;
      margin-right: 6px;
    }

    .policy-type a {
      margin-right: 10px;
      font-size: 14px;
      color: #007aff;
      text-decoration: none;
    }

    .footer {
      text-align: center;
      margin-top: 40px;
      font-size: 13px;
      color: #888;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>应用隐私与用户协议合集</h1>
"""

    for app, items in policies.items():
        html += f'    <div class="app-entry">\n'
        html += f'      <div class="app-name">{app}</div>\n'
        for policy_type in ["privacy", "user-agreement", "support"]:
            html += f'      <div class="policy-type">\n'
            label = {
                "privacy": "隐私政策",
                "user-agreement": "用户协议",
                "support": "技术支持"
            }[policy_type]
            html += f'        <span>{label}:</span>\n'
            if policy_type in items:
                for lang in sorted(items[policy_type]):
                    filename = items[policy_type][lang]
                    html += f'        <a href="{filename}">{lang}</a>\n'
            else:
                html += f'        <span style="color:#aaa;">无</span>\n'
            html += f'      </div>\n'
        html += f'    </div>\n'

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
