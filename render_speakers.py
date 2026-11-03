from pathlib import Path
from html import escape
import re
source=Path('recruitment_for_speakers.md').read_text(encoding='utf-8')
lines=source.splitlines()
TITLE=lines[0][2:]
ACC='#D9AFB0'; DARK='#462B32'; INK='#4A3238'; CYAN='#D6A9AE'; PAPER='#F9F5F2'

def leaf(t): return '<span leaf="">'+escape(t,quote=False)+'</span>'
def txt(t,marks=(),strong_color="#462B32"):
    # Preserve the approved copy, with just presentation markup around phrases.
    tokens=re.split(r'(\*\*.*?\*\*|\*[^*]+\*)',t)
    out=[]
    for token in tokens:
        if not token: continue
        if token.startswith('**') and token.endswith('**'):
            out.append('<strong style="font-weight:800;color:'+strong_color+';">'+leaf(token[2:-2])+'</strong>')
        elif token.startswith('*') and token.endswith('*'):
            out.append('<em style="font-style:normal;color:#87757A;font-size:13px;">'+leaf(token[1:-1])+'</em>')
        else:
            # Mark only the first occurrence of each selected phrase.
            pieces=[token]
            for mark in marks:
                next_p=[]
                for piece in pieces:
                    if isinstance(piece,tuple): next_p.append(piece); continue
                    a,found,b=piece.partition(mark)
                    if found: next_p += [a,('mark',mark),b]
                    else: next_p.append(piece)
                pieces=next_p
            for piece in pieces:
                if not piece: continue
                if isinstance(piece,tuple): out.append('<span style="border-bottom:2px solid #D9AFB0;font-weight:650;">'+leaf(piece[1])+'</span>')
                else: out.append(leaf(piece))
    return ''.join(out)

def para(t,marks=(),margin_bottom=31):
    body='<p style="font-size:15px;line-height:1.9;color:#5D484D;margin:0;text-align:justify;">'+txt(t,marks)+'</p>'
    spacer='<p style="margin:0;font-size:15px;line-height:1.9;"><span leaf=""><br></span></p>' if margin_bottom else ''
    return body+spacer

def section_head(n,en,zh):
    return f'<section style="margin:30px 0 22px;border-top:1px solid #E2D4D2;padding-top:19px;"><p style="font-size:11px;color:#9F676E;letter-spacing:2.2px;font-weight:800;margin:0 0 6px;">{leaf(f"{n:02d} / {en}")}</p><h3 style="font-size:26px;line-height:1.35;color:#432A31;margin:0;font-weight:900;letter-spacing:1px;">{leaf(zh)}</h3></section>'

# Decorative SVG only; all article text remains editable HTML.
poster_svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 170" width="100%" style="display:block;height:auto;margin:12px 0 8px;" aria-hidden="true">
<path d="M0 132 H155 L205 76 H395 L445 132 H600" fill="none" stroke="#76545C" stroke-width="2"/>
<path d="M0 148 H184 L229 97 H371 L416 148 H600" fill="none" stroke="#89646C" stroke-width="1"/>
<rect x="234" y="22" width="132" height="126" rx="10" fill="#52343B" stroke="#C79DA3" stroke-width="2"/>
<path d="M250 57 H350 M250 75 H350 M250 93 H350 M250 111 H350" stroke="#A8777E" stroke-width="2"/>
<path d="M300 20 V148" stroke="#D9AFB0" stroke-width="5" stroke-linecap="round"/>
<circle cx="300" cy="85" r="11" fill="#D9AFB0"><animate attributeName="opacity" values=".35;1;.35" dur="2.8s" repeatCount="indefinite"/></circle>
<circle r="5" fill="#D6A9AE"><animateMotion dur="5s" repeatCount="indefinite" path="M0 132 H155 L205 76 H395 L445 132 H600"/></circle>
<path d="M0 160 H600" fill="none" stroke="#D6A9AE" stroke-opacity=".5" stroke-width="1.5" stroke-dasharray="5 12"><animate attributeName="stroke-dashoffset" from="0" to="-68" dur="4s" repeatCount="indefinite"/></path>
</svg>'''

out=['<section style="max-width:677px;margin:0 auto;background:#F9F5F2;font-family:-apple-system,BlinkMacSystemFont,\'PingFang SC\',\'Microsoft YaHei\',sans-serif;color:#4A3238;line-height:1.8;overflow:hidden;">']
out.append('<section style="background:#462B32;padding:27px 24px 28px;overflow:hidden;">')
out.append('<p style="margin:0 0 22px;color:#D6A9AE;font-size:10px;font-weight:800;letter-spacing:2.8px;">'+leaf('FRONTIER ELECTRONICS TECHNOLOGY TALK  /  PKU')+'</p>')
out.append('<p style="margin:0;color:#D9AFB0;font-size:70px;font-weight:900;line-height:1;letter-spacing:-4px;">'+leaf('FET²')+'<span style="color:#F8ECEB;font-size:20px;letter-spacing:1px;margin-left:17px;vertical-align:baseline;">'+leaf('2026')+'</span></p>')
out.append(poster_svg)
out.append('<p style="margin:0 0 6px;color:#D9AFB0;font-size:11px;font-weight:800;letter-spacing:3px;">'+leaf('CALL FOR SPEAKERS')+'</p>')
out.append('<p style="margin:0;color:#FFFFFF;font-size:30px;font-weight:900;line-height:1.37;letter-spacing:1px;">'+leaf('把你的研究，')+'<br>'+leaf('带到下一场对话')+'</p>')
out.append('<section style="border-top:1px solid #92747A;margin-top:23px;padding-top:12px;"><p style="margin:0;color:#F4E9E7;font-size:12px;letter-spacing:1px;">'+leaf('11.28 SAT  ·  13:30—18:00  ·  线下举行')+'</p></section>')
out.append('</section>')
out.append('<section style="padding:25px 22px 42px;">')
quote=lines[2][2:]
out.append('<section style="background:#F2E8E5;border-left:4px solid #AF767D;padding:17px 18px;margin:0 0 24px;"><p style="font-size:16px;line-height:1.78;font-weight:750;color:#533A40;margin:0;">'+txt(quote,('开环测试',))+'</p></section>')
# Iterate the actual Markdown blocks so no paragraph or attribution is dropped.
blocks=[]; i=3
while i<len(lines):
    s=lines[i].strip()
    if not s: i+=1;continue
    if s=='---': blocks.append(('footer_start',''));i+=1;continue
    if s.startswith('## '): blocks.append(('heading',s[3:]));i+=1;continue
    if s.startswith('* '):
        items=[]
        while i<len(lines) and lines[i].strip().startswith('* '): items.append(lines[i].strip()[2:]);i+=1
        blocks.append(('list',items));continue
    if s.startswith('【报名问卷二维码示意'): blocks.append(('qr',s));i+=1;continue
    blocks.append(('p',s));i+=1

sec=0; j=0; footer=False
marks={
'电子信息领域的光谱很宽：有人向下深潜，在材料、器件与工艺的物理极限处试探；有人向上构建，在芯片架构、光电系统、量子通信与 6G 网络中寻找最优解。平时大家各自在不同的抽象层里耕耘，FET² 则提供一个下午的带宽，让做底层器件的人和做上层系统的人实现一次面对面的“阻抗匹配”。':['面对面的“阻抗匹配”'],
}
while j<len(blocks):
    kind,value=blocks[j]
    if kind=='heading':
        if sec==0:
            out.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 26" width="100%" style="display:block;height:auto;margin:19px 0 0;" aria-hidden="true"><path d="M0 13 H200 L218 13 L226 5 L235 21 L245 13 H600" fill="none" stroke="#C69BA1" stroke-width="2" stroke-dasharray="650" stroke-dashoffset="650"><animate attributeName="stroke-dashoffset" from="650" to="0" dur="2.5s" repeatCount="indefinite"/></path></svg>')
        sec+=1
        out.append(section_head(sec,['ABOUT','FORMAT','AWARDS','APPLY'][sec-1],value))
        j+=1;continue
    if kind=='footer_start':
        footer=True
        out.append('<section style="border-top:1px solid #E2D4D2;margin-top:40px;padding-top:20px;">')
        out.append('<p style="margin:0 0 13px;color:#8A777B;font-size:11px;font-weight:800;letter-spacing:2px;">'+leaf('ORGANIZING TEAM')+'</p>')
        j+=1;continue
    if kind=='list':
        for n,item in enumerate(value):
            out.append('<section style="background:#FFFFFF;border:1px solid #E6D9D7;border-left:4px solid #D9AFB0;padding:15px 16px;margin:0 0 20px;box-shadow:0 4px 14px rgba(70,43,50,.05);"><p style="margin:0 0 4px;color:#9F676E;font-size:10px;font-weight:800;letter-spacing:2px;">'+leaf('OPEN / '+str(n+1).zfill(2))+'</p><p style="font-size:14px;line-height:1.8;color:#5D484D;margin:0;">'+txt(item)+'</p></section>')
        j+=1;continue
    if kind=='qr':
        out.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 28" width="100%" style="display:block;height:28px;margin:4px 0 0;" aria-hidden="true"><g><path d="M286 8 L300 20 L314 8" fill="none" stroke="#9F676E" stroke-width="2"/><animateTransform attributeName="transform" type="translate" values="0 0;0 5;0 0" dur="1.7s" repeatCount="indefinite"/></g></svg>')
        out.append('<section style="background:#FFFFFF;border:1.5px dashed #BE9FA2;padding:26px 12px;text-align:center;margin:20px 0 10px;"><p style="font-size:28px;color:#9F676E;margin:0 0 5px;">'+leaf('▦')+'</p><p style="font-size:13px;color:#8A7478;margin:0;">'+leaf(value)+'</p></section>')
        j+=1;continue
    if kind=='p':
        # The paired report formats become two consistent cards.
        if value.startswith('**Orals（') or value.startswith('**Posters（'):
            desc=blocks[j+1][1] if j+1<len(blocks) and blocks[j+1][0]=='p' else ''
            label='ORALS' if value.startswith('**Orals') else 'POSTERS'
            color='#462B32' if label=='ORALS' else '#704A51'
            out.append(f'<section style="background:{color};padding:18px 19px;margin:0 0 20px;border-radius:10px;"><p style="font-size:10px;color:#D9AFB0;letter-spacing:2px;font-weight:800;margin:0 0 5px;">{leaf(label)}</p><p style="font-size:17px;color:#FFFFFF;font-weight:850;line-height:1.5;margin:0 0 9px;">{leaf(value.strip("*"))}</p><p style="font-size:14px;color:#F2E6E4;line-height:1.8;margin:0;">{txt(desc)}</p></section>')
            j+=2;continue
        if footer:
            out.append('<p style="font-size:12px;line-height:1.8;color:#8D7A7E;margin:0 0 5px;">'+txt(value)+'</p>')
        elif value.startswith('本次论坛将于'):
            out.append('<section style="background:#F1E6E3;border-top:3px solid #AF767D;padding:15px 17px;margin:0 0 20px;">'+para(value,margin_bottom=0)+'</section>')
        elif value.startswith('论坛设有'):
            out.append('<section style="background:#F1E6E3;border-left:4px solid #AF767D;padding:18px;margin:0 0 18px;">'+para(value,margin_bottom=0)+'</section>')
        elif value.startswith('**报名截止时间**'):
            out.append('<section style="background:#462B32;padding:17px 18px;margin:16px 0 14px;"><p style="color:#F9EFED;font-size:16px;font-weight:800;margin:0;line-height:1.7;">'+txt(value,strong_color='#F9EFED')+'</p></section>')
        elif value.startswith('*注：'):
            out.append('<section style="border-left:3px solid #B9A0A3;padding:8px 14px;margin:10px 0 20px;">'+para(value,margin_bottom=0)+'</section>')
        else: out.append(para(value,marks.get(value,())))
        j+=1;continue
out.append('</section>') # footer
out.append('</section>') # padded body
out.append('</section>') # root
Path('recruitment_for_speakers_秀米设计稿.html').write_text('\n'.join(out),encoding='utf-8')
