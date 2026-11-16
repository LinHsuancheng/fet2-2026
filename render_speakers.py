"""Render the approved speaker recruitment copy without changing its text."""

from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re

SOURCE = Path("recruitment_for_speakers.md")
OUTPUT = Path("recruitment_for_speakers_秀米设计稿.html")
QR_ASSET = Path("assets/registration-qr.png")
QR_URL = "https://img.xiumi.us/xmi/ua/5bkMf/i/ee7417ed6d6b8a86564c172b2da9b253-sz_13157.png"


def leaf(text):
    return '<span leaf="">' + escape(text, quote=False) + "</span>"


def rich(text):
    parts = re.split(r"(\*\*.*?\*\*)", text)
    return "".join(
        '<strong style="color:#713C49;font-weight:800;">' + leaf(part[2:-2]) + "</strong>"
        if part.startswith("**") and part.endswith("**") else leaf(part)
        for part in parts if part
    )


def paragraph(text, blank=True):
    html = '<p style="margin:0;color:#59434A;font-size:15px;line-height:1.9;text-align:justify;">' + rich(text) + "</p>"
    # Xiumi strips paragraph margins; a real empty paragraph survives saving.
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
    for raw in markdown.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# "):
            blocks.append(("title", line[2:]))
        elif line.startswith("## "):
            blocks.append(("heading", line[3:]))
        elif line.startswith("> "):
            blocks.append(("quote", line[2:]))
        elif line.startswith("- "):
            blocks.append(("item", line[2:]))
        elif line in ("_" * 40, "---"):
            blocks.append(("rule", ""))
        elif line.startswith("![](") and line.endswith(")"):
            blocks.append(("image", line[4:-1]))
        else:
            blocks.append(("paragraph", line))
    return blocks


def render(blocks):
    out = ['<section style="max-width:677px;margin:0 auto;background:#FFF9F7;font-family:-apple-system,BlinkMacSystemFont,\'PingFang SC\',\'Microsoft YaHei\',sans-serif;color:#513941;line-height:1.8;overflow:hidden;">']
    for kind, value in blocks:
        if kind == "title":
            out.append(
                '<section style="background:#EED3D5;padding:27px 24px 28px;overflow:hidden;border-bottom:4px solid #B77680;">'
                + ART + '<h3 style="color:#633D48;font-size:29px;font-weight:900;line-height:1.42;letter-spacing:.5px;margin:0;">'
                + leaf(value) + '</h3></section><section style="padding:27px 22px 42px;">'
            )
        elif kind == "heading":
            out.append(
                '<section style="margin:24px 0 23px;padding:16px 0 0;border-top:1px solid #E8D5D5;">'
                '<h3 style="margin:0;padding-left:13px;border-left:4px solid #B77680;color:#713C49;font-size:24px;line-height:1.4;font-weight:850;">'
                + leaf(value) + '</h3></section>'
            )
        elif kind == "quote":
            out.append(
                '<section style="background:#F5E5E5;border-left:4px solid #B77680;padding:18px;margin:1px 0 29px;">'
                '<p style="margin:0;color:#633D48;font-size:16px;font-weight:700;line-height:1.85;">'
                + rich(value) + '</p></section>'
            )
        elif kind == "item":
            out.append(
                '<section style="background:#FFFFFF;border:1px solid #E9D6D7;border-left:4px solid #C2868E;padding:16px 18px;margin:0 0 18px;box-shadow:0 4px 14px rgba(105,58,67,.05);">'
                + paragraph(value, blank=False) + '</section>'
            )
        elif kind == "image":
            if value != QR_ASSET.as_posix() or not QR_ASSET.is_file():
                raise ValueError(f"Missing or unexpected image: {value}")
            out.append(
                '<section style="background:#FFFFFF;border:1px solid #E9D6D7;'
                'padding:20px 12px;text-align:center;margin:16px 0 26px;">'
                '<span leaf=""><img src="' + QR_URL + '" style="width:190px;max-width:100%;'
                'height:auto;display:block;margin:0 auto;image-rendering:pixelated;"></span>'
                '</section>'
            )
        elif kind == "rule":
            out.append('<section style="border-top:1px solid #DCC6C8;margin:34px 0 21px;"><span leaf=""><br></span></section>')
        elif value.startswith(("**Orals（", "**Posters（", "本次论坛将于", "论坛设有", "报名截止时间：")):
            out.append(
                '<section style="background:#F9EEEE;border-left:4px solid #B77680;padding:17px 18px;margin:0 0 24px;">'
                + paragraph(value, blank=False) + '</section>'
            )
        else:
            out.append(paragraph(value))
    out.extend(["</section>", "</section>"])
    return "\n".join(out)


class LeafText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "span" and ("leaf", "") in attrs:
            self.depth += 1

    def handle_endtag(self, tag):
        if tag == "span" and self.depth:
            self.depth -= 1

    def handle_data(self, data):
        if self.depth:
            self.parts.append(data)


def main():
    blocks = parse(SOURCE.read_text(encoding="utf-8"))
    html = render(blocks)
    text = LeafText()
    text.feed(html)
    expected = "".join(value.replace("**", "") for kind, value in blocks if kind not in ("rule", "image"))
    if "".join(text.parts) != expected:
        raise ValueError("Rendered text differs from the approved Markdown")
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Rendered {len(blocks)} blocks; article text matches source exactly: {OUTPUT}")


if __name__ == "__main__":
    main()
