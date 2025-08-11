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

        match = re.match(r"(.+?)-(privacy|user-agreement|support)\.([a-zA-Z\-]+)\.html$", file)
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
    """生成 index.html，展示所有协议多语言链接，使用新简洁大气风格"""
    lang_map = {
        "de": "德语",
        "en": "英语",
        "ja": "日语",
        "ko": "韩语",
        "zh-Hans": "简体中文",
        "zh-Hant": "繁体中文"
    }
    html = """<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <title>协议合集</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    /* Reset and base */
    body {
      margin: 0; padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
      background: #f5f7fa;
      color: #222;
      font-size: 16px;
      line-height: 1.6;
    }
    .container {
      max-width: 680px;
      margin: 48px auto;
      padding: 0 24px;
    }
    h1 {
      font-weight: 800;
      font-size: 2.4rem;
      color: #0b2545;
      margin-bottom: 48px;
      text-align: center;
      letter-spacing: 0.06em;
    }
    .app-entry {
      margin-bottom: 56px;
    }
    .app-name {
      font-weight: 700;
      font-size: 1.5rem;
      color: #0b2545;
      margin-bottom: 24px;
      border-bottom: 1px solid #d9e2ec;
      padding-bottom: 8px;
    }
    .policy-type {
      margin-bottom: 18px;
      display: flex;
      align-items: center;
      flex-wrap: wrap;
    }
    .policy-label {
      flex-shrink: 0;
      font-weight: 600;
      color: #334e68;
      width: 90px;
      letter-spacing: 0.04em;
    }
    .policy-links {
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
    }
    .policy-links a {
      color: #1c7ed6;
      font-weight: 500;
      text-decoration: none;
      font-size: 1rem;
      padding: 4px 10px;
      border-radius: 4px;
      transition: background-color 0.25s ease, color 0.25s ease;
    }
    .policy-links a:hover {
      background-color: #1c7ed6;
      color: #fff;
    }
    .policy-links .no-link {
      color: #aab8c2;
      font-style: italic;
      cursor: default;
    }
    .footer {
      text-align: center;
      font-size: 14px;
      color: #768390;
      padding-bottom: 24px;
      user-select: none;
    }
    @media (max-width: 480px) {
      .app-name {
        font-size: 1.3rem;
      }
      .policy-label {
        width: 100%;
        margin-bottom: 6px;
      }
      .policy-type {
        flex-direction: column;
        align-items: flex-start;
        margin-bottom: 28px;
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
        for policy_type in ["privacy", "user-agreement", "support"]:
            html += '      <div class="policy-type">\n'
            label = {
                "privacy": "隐私政策",
                "user-agreement": "用户协议",
                "support": "技术支持"
            }[policy_type]
            html += f'        <div class="policy-label">{label}</div>\n'
            html += '        <div class="policy-links">\n'
            if policy_type in items:
                for lang in sorted(items[policy_type]):
                    filename = items[policy_type][lang]
                    lang_label = lang_map.get(lang, lang)
                    html += f'          <a href="{filename}">{lang_label}</a>\n'
            else:
                html += '          <span class="no-link">无</span>\n'
            html += '        </div>\n'
            html += '      </div>\n'
        html += '    </div>\n'

    html += """
  <div class="footer">页面由脚本自动生成</div>
  </div>
</body>
</html>
"""
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ index.html 索引已生成！")

if __name__ == "__main__":
    policies = find_policies()
    readme_text = generate_readme(policies)
    update_readme(readme_text)
    generate_index(policies)
