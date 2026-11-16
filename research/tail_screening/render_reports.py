"""Render the two saved Fable reports using locally installed CJK fonts.

Run --check to validate sources and fonts without writing PDFs. Supply
--font-regular and --font-bold on hosts without the default Windows fonts.
"""
from pathlib import Path
import argparse
import html
import re
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader

root = Path(__file__).resolve().parent
out = root / 'output/pdf'
INK = colors.HexColor('#172A3A')
BLUE = colors.HexColor('#195F91')

def inline(value):
    value = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', value)
    value = value.replace('`', '').replace('—', '-').replace('–', '-')
    value = html.escape(value)
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', value)

def render(source, compact=False):
    body = 9.5 if compact else 10
    lead = 14 if compact else 16
    styles = {
        'body': ParagraphStyle('Body', fontName='CJK', fontSize=body, leading=lead, textColor=INK,
                               wordWrap='CJK', spaceAfter=7 if compact else 9),
        'title': ParagraphStyle('Title', fontName='CJKBold', fontSize=17 if compact else 21,
                                leading=25 if compact else 30, textColor=INK, spaceAfter=14, keepWithNext=True),
        'h2': ParagraphStyle('H2', fontName='CJKBold', fontSize=13, leading=20, textColor=BLUE,
                            spaceBefore=12, spaceAfter=7, keepWithNext=True),
        'h3': ParagraphStyle('H3', fontName='CJKBold', fontSize=11, leading=17, textColor=INK,
                            spaceBefore=9, spaceAfter=6, keepWithNext=True),
        'cell': ParagraphStyle('Cell', fontName='CJK', fontSize=8 if compact else 8.2, leading=12.5,
                              wordWrap='CJK', textColor=INK),
    }
    target = out / (source.stem + '.pdf')
    doc = SimpleDocTemplate(str(target), pagesize=A4, leftMargin=43, rightMargin=43,
                            topMargin=42, bottomMargin=40, title=source.stem,
                            author='Theodore / Codex research execution')
    width = A4[0] - 86
    story=[]
    lines=source.read_text(encoding='utf8').splitlines()
    i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:
            i+=1
            continue
        if line.startswith('!['):
            match=re.fullmatch(r'!\[([^\]]*)\]\(([^)]+)\)',line)
            if match:
                imgpath=source.parent/match[2]
                iw,ih=ImageReader(str(imgpath)).getSize()
                h=width*ih/iw
                story.append(KeepTogether([Image(str(imgpath),width=width,height=h),Spacer(1,6)]))
                i+=1
                continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                row=[v.strip() for v in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[:\- ]+',v) for v in row):
                    rows.append(row)
                i+=1
            cols=len(rows[0])
            if cols==4:
                weights=[.26,.23,.23,.28]
            elif cols==6:
                weights=[.25,.15,.15,.16,.15,.14]
            elif cols==3:
                weights=[.20,.56,.24]
            elif cols==5:
                weights=[.22,.20,.20,.20,.18]
            else:
                weights=[1/cols]*cols
            data=[[Paragraph(('<b>'+inline(v)+'</b>') if ri==0 else inline(v),styles['cell'])
                   for v in row] for ri,row in enumerate(rows)]
            table=Table(data,colWidths=[width*w for w in weights],repeatRows=1,hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E8F0F6')),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F6F8FA')]),
                ('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#9AB4C8')),
                ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),
                ('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),6),
                ('BOTTOMPADDING',(0,0),(-1,-1),6),
            ]))
            story.extend([table,Spacer(1,10)])
            continue
        if line.startswith('# '):
            style='title'; line=line[2:]
        elif line.startswith('## '):
            style='h2'; line=line[3:]
        elif line.startswith('### '):
            style='h3'; line=line[4:]
        else:
            style='body'
        story.append(Paragraph(inline(line),styles[style]))
        i+=1
    def footer(canvas, document):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor('#D8E1E8'))
        canvas.line(43,31,A4[0]-43,31)
        canvas.setFont('CJK',7.2)
        canvas.setFillColor(colors.HexColor('#5D6A75'))
        canvas.drawString(43,20,'Fable 研究交付 | 2026-11-16 | 配套 Markdown 含出处与原始文件链接')
        canvas.drawRightString(A4[0]-43,20,str(document.page))
        canvas.restoreState()
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    reader=PdfReader(str(target))
    texts=[p.extract_text() or '' for p in reader.pages]
    assert all(t.strip() for t in texts)
    assert '78.6' in '\n'.join(texts)
    if compact:
        assert len(reader.pages)==1, f'One-page report produced {len(reader.pages)} pages'
    print(target.name,'pages',len(reader.pages),'characters',sum(map(len,texts)))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font-regular', type=Path,
                        default=Path('C:/Windows/Fonts/msyh.ttc'),
                        help='Path to a local regular CJK TrueType font or collection (face 0)')
    parser.add_argument('--font-bold', type=Path,
                        default=Path('C:/Windows/Fonts/msyhbd.ttc'),
                        help='Path to a local bold CJK TrueType font or collection (face 0)')
    parser.add_argument('--check', action='store_true',
                        help='Validate report sources, images, and fonts without writing PDFs')
    args = parser.parse_args()
    for name, path in [('CJK', args.font_regular), ('CJKBold', args.font_bold)]:
        if not path.is_file():
            parser.error(f'Font file not found: {path}; supply --font-regular / --font-bold')
        pdfmetrics.registerFont(TTFont(name, str(path), subfontIndex=0))
    pdfmetrics.registerFontFamily('CJK', normal='CJK', bold='CJKBold', italic='CJK', boldItalic='CJKBold')
    sources = [(root/'FABLE_CURRENT_REPORT.md', False), (root/'FABLE_ONE_PAGE.md', True)]
    for source, _ in sources:
        text = source.read_text(encoding='utf8')
        for match in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', text):
            ImageReader(str(source.parent/match[1])).getSize()
    if args.check:
        print('Validated two report sources, referenced images, and configured fonts; no PDFs written.')
        return
    out.mkdir(parents=True, exist_ok=True)
    for source, compact in sources:
        render(source, compact)


if __name__ == '__main__':
    main()
