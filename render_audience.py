"""Render the audience registration copy into Xiumi-compatible HTML."""

from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re

SOURCE = Path("audience_registration_2026.md")
OUTPUT_XIUMI = Path("audience_registration_2026_秀米设计稿.html")
OUTPUT_PREVIEW = Path("audience_registration_2026_秀米设计稿_预览.html")
LOGO_ASSET = Path("assets/xinban-logo.png")
QR_ASSET = Path("assets/registration-qr.png")
QR_URL = "https://img.xiumi.us/xmi/ua/5bkMf/i/ee7417ed6d6b8a86564c172b2da9b253-sz_13157.png"


def leaf(text):
    return '<span leaf="">' + escape(text, quote=False) + "</span>"


def rich(text):
    parts = re.split(r"(\*\*.*?\*\*|\*.*?\*)", text)
    res = []
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            res.append('<strong style="color:#713C49;font-weight:800;">' + leaf(part[2:-2]) + "</strong>")
        elif part.startswith("*") and part.endswith("*"):
            res.append('<em style="color:#8A5460;font-style:italic;">' + leaf(part[1:-1]) + "</em>")
        else:
            res.append(leaf(part))
    return "".join(res)


def paragraph(text, blank=True):
    html = '<p style="margin:0;color:#59434A;font-size:15px;line-height:1.9;text-align:justify;">' + rich(text) + "</p>"
    if blank:
        html += '<p style="margin:0;font-size:15px;line-height:1.9;"><span leaf=""><br></span></p>'
    return html


ART = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 146" width="100%" style="display:block;height:auto;margin:8px 0 18px;" aria-hidden="true">
<path d="M0 113 H150 L201 57 H399 L450 113 H600" fill="none" stroke="#C78E97" stroke-width="2"/>
<path d="M0 132 H170 L217 80 H383 L430 132 H600" fill="none" stroke="#D9ADB3" stroke-width="1.5"/>
<rect x="240" y="21" width="120" height="104" rx="11" fill="#F8EBE9" stroke="#A76570" stroke-width="2"/>
<path d="M255 51 H345 M255 68 H345 M255 85 H345 M255 102 H345" stroke="#D4A0A8" stroke-width="2"/>
<path d="M300 18 V126" stroke="#9C5965" stroke-width="5" stroke-linecap="round"/>
<circle cx="300" cy="73" r="10" fill="#B76F7B"><animate attributeName="opacity" values=".3;1;.3" dur="2.8s" repeatCount="indefinite"/></circle>
<circle r="5" fill="#9C5965"><animateMotion dur="5s" repeatCount="indefinite" path="M0 113 H150 L201 57 H399 L450 113 H600"/></circle>
<path d="M0 143 H600" fill="none" stroke="#C78E97" stroke-width="1" stroke-dasharray="5 12"><animate attributeName="stroke-dashoffset" from="0" to="-68" dur="4s" repeatCount="indefinite"/></path>
</svg>"""


def parse(markdown):
    blocks = []
    lines = markdown.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        if not line:
            i += 1
            continue
        if line.startswith("# "):
            blocks.append(("title", line[2:]))
            i += 1
        elif line.startswith("## "):
            blocks.append(("heading", line[3:]))
            i += 1
        elif line.startswith("### "):
            blocks.append(("subheading", line[4:]))
            i += 1
        elif line.startswith("> "):
            # Multi-line quotes
            quote_lines = [line[2:]]
            while i + 1 < len(lines) and lines[i + 1].strip().startswith("> "):
                i += 1
                quote_lines.append(lines[i].strip()[2:])
            blocks.append(("quote", "<br>".join(quote_lines)))
            i += 1
        elif line.startswith("- "):
            blocks.append(("item", line[2:]))
            i += 1
        elif line.startswith("|") and line.endswith("|"):
            # Table block
            table_lines = [line]
            while i + 1 < len(lines) and lines[i + 1].strip().startswith("|") and lines[i + 1].strip().endswith("|"):
                i += 1
                table_lines.append(lines[i].strip())
            blocks.append(("table", table_lines))
            i += 1
        elif line in ("_" * 40, "---"):
            blocks.append(("rule", ""))
            i += 1
        elif line.startswith("![](") and line.endswith(")"):
            blocks.append(("image", line[4:-1]))
            i += 1
        else:
            blocks.append(("paragraph", line))
            i += 1
    return blocks


def render_table(table_lines):
    if len(table_lines) < 2:
        return ""
    headers = [c.strip() for c in table_lines[0].strip("|").split("|")]
    rows = []
    for r in table_lines[2:]:
        rows.append([c.strip() for c in r.strip("|").split("|")])

    html = ['<section style="margin:20px 0 24px;overflow-x:auto;">']
    html.append('<table style="width:100%;border-collapse:collapse;font-size:14px;color:#513941;border:1px solid #E9D6D7;background:#FFFFFF;">')
    html.append('<thead><tr style="background:#F5E5E5;color:#713C49;font-weight:700;">')
    for h in headers:
        html.append(f'<th style="padding:10px 12px;border:1px solid #E9D6D7;text-align:left;">{rich(h)}</th>')
    html.append('</tr></thead><tbody>')
    for row in rows:
        html.append('<tr style="border-bottom:1px solid #E9D6D7;">')
        for c in row:
            html.append(f'<td style="padding:9px 12px;border:1px solid #E9D6D7;line-height:1.6;">{rich(c)}</td>')
        html.append('</tr>')
    html.append('</tbody></table></section>')
    return "".join(html)


def render(blocks):
    out = ['<section style="max-width:677px;margin:0 auto;background:#FFF9F7;font-family:-apple-system,BlinkMacSystemFont,\'PingFang SC\',\'Microsoft YaHei\',sans-serif;color:#513941;line-height:1.8;overflow:hidden;">']
    if not LOGO_ASSET.is_file():
        raise FileNotFoundError(LOGO_ASSET)
    for kind, value in blocks:
        if kind == "title":
            out.append(
                '<section style="background:#EED3D5;padding:27px 24px 28px;overflow:hidden;border-bottom:4px solid #B77680;">'
                + '<img src="assets/xinban-logo.png" alt="北京大学电子信息科学类实验班与 FET² 标志" style="display:block;width:236px;max-width:100%;height:auto;margin:0 0 18px;">'
                + ART + '<h3 style="color:#633D48;font-size:26px;font-weight:900;line-height:1.42;letter-spacing:.5px;margin:0;">'
                + leaf(value) + '</h3></section><section style="padding:27px 22px 42px;">'
            )
        elif kind == "heading":
            out.append(
                '<section style="margin:28px 0 20px;padding:16px 0 0;border-top:1px solid #E8D5D5;">'
                '<h3 style="margin:0;padding-left:13px;border-left:4px solid #B77680;color:#713C49;font-size:22px;line-height:1.4;font-weight:850;">'
                + leaf(value) + '</h3></section>'
            )
        elif kind == "subheading":
            out.append(
                '<section style="margin:20px 0 14px;">'
                '<h4 style="margin:0;color:#8B4E5A;font-size:17px;line-height:1.5;font-weight:800;letter-spacing:0.3px;">'
                '✦ ' + leaf(value) + '</h4></section>'
            )
        elif kind == "quote":
            lines = value.split("<br>")
            rendered_lines = "<br>".join(rich(l) for l in lines)
            out.append(
                '<section style="background:#F5E5E5;border-left:4px solid #B77680;padding:18px;margin:8px 0 24px;border-radius:0 8px 8px 0;">'
                '<p style="margin:0;color:#633D48;font-size:15px;font-weight:700;line-height:1.85;">'
                + rendered_lines + '</p></section>'
            )
        elif kind == "item":
            out.append(
                '<section style="background:#FFFFFF;border:1px solid #E9D6D7;border-left:4px solid #C2868E;padding:16px 18px;margin:0 0 16px;box-shadow:0 3px 12px rgba(105,58,67,.04);border-radius:0 6px 6px 0;">'
                + paragraph(value, blank=False) + '</section>'
            )
        elif kind == "table":
            out.append(render_table(value))
        elif kind == "image":
            out.append(
                '<section style="background:#FFFFFF;border:1px solid #E9D6D7;'
                'padding:20px 12px;text-align:center;margin:16px 0 20px;border-radius:6px;">'
                '<span leaf=""><img src="' + QR_URL + '" style="width:190px;max-width:100%;'
                'height:auto;display:block;margin:0 auto;image-rendering:pixelated;"></span>'
                '</section>'
            )
        elif kind == "rule":
            out.append('<section style="border-top:1px solid #DCC6C8;margin:30px 0 24px;"><span leaf=""><br></span></section>')
        elif value.startswith(("- **时间：**", "- **地点：**", "- **招募对象：**", "- **报名截止时间：**", "- **报名方式：**")):
            out.append(
                '<section style="background:#F9EEEE;border-left:4px solid #B77680;padding:15px 18px;margin:0 0 16px;border-radius:0 6px 6px 0;">'
                + paragraph(value, blank=False) + '</section>'
            )
        else:
            out.append(paragraph(value))
    out.extend(["</section>", "</section>"])
    return "\n".join(out)


def render_preview(html_body):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FET² 2026 听众报名推文预览</title>
<style>
  body {{
    background-color: #EDE4E2;
    margin: 0;
    padding: 30px 10px;
    display: flex;
    justify-content: center;
  }}
  .preview-wrapper {{
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    background: #FFF9F7;
    border-radius: 8px;
    overflow: hidden;
  }}
</style>
</head>
<body>
<div class="preview-wrapper">
{html_body}
</div>
</body>
</html>"""


def main():
    content = SOURCE.read_text(encoding="utf-8")
    blocks = parse(content)
    html = render(blocks)
    OUTPUT_XIUMI.write_text(html, encoding="utf-8")
    preview_html = render_preview(html)
    OUTPUT_PREVIEW.write_text(preview_html, encoding="utf-8")
    print(f"Rendered {len(blocks)} blocks successfully to:\n- {OUTPUT_XIUMI}\n- {OUTPUT_PREVIEW}")


if __name__ == "__main__":
    main()
