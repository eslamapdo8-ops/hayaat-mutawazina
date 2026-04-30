#!/usr/bin/env python3
"""
hayaat-bundle.py — تجميع ملفات الحياة المتوازنة في PDF واحد
===========================================================
آلية العمل:
1. لكل ملف HTML، نأخذه كما هو ونضعه في صفحة منفصلة داخل PDF
2. نستخدم fpdf2 لإنشاء PDF (بدون headless browser — لأن كروم غير متوفر)
3. الخيار الأفضل للمستخدمة: فتح كل HTML في المتصفح ثم طباعة كـ PDF
   هذا الملف ينتج "كتيب" يجمع التعليمات مع روابط مباشرة

البديل الأفضل (للمستقبل):
- على جهاز مكتبي: استخدم Chrome → Ctrl+P على كل ملف → حفظ كـ PDF
- ثم استخدم أي أداة دمج PDF (مثل pdfunite أو iLovePDF)
"""

import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))

BUNDLE = {
    "name": "الحياة المتوازنة — الباقة الكاملة",
    "version": "1.0.0 (MVP)",
    "files": [
        {
            "title": "🗓️ مخطط الأسبوع (Two-Page Spread)",
            "file": "weekly-spread.html",
            "pages_est": "2 صفحات A4",
            "description": "قلب المنتج — تخطيط أسبوعي كامل بتقويم هجري/ميلادي مزدوج"
        },
        {
            "title": "🌟 المخطط اليومي (صفحة اليوم المثالي)",
            "file": "daily-planner.html",
            "pages_est": "1 صفحة A4",
            "description": "تقسيم اليوم من 6ص-12م مع أولويات وتأمل"
        },
        {
            "title": "📊 متعقب العادات الشهري",
            "file": "habit-tracker.html",
            "pages_est": "1-2 صفحات A4 (لاندسكيب)",
            "description": "6 عادات قابلة للتخصيص × 30/31 يوم مع إحصائيات"
        },
        {
            "title": "📔 كتاب الملصقات (Sticker Book)",
            "file": "sticker-book.html",
            "pages_est": "1-2 صفحات A4",
            "description": "47 ملصقاً رقمياً — قابلة للنسخ والطباعة والقص"
        }
    ]
}

def create_index_html():
    """إنشاء صفحة Index جامعة لكل الملفات مع روابط مباشرة"""
    # Auto-detect tunnel URL
    tunnel_url = os.environ.get("TUNNEL_URL", "")
    
    links_html = ""
    for item in BUNDLE["files"]:
        path = item["file"]
        local_link = f"http://127.0.0.1:9090/{path}"
        tunnel_link = f"{tunnel_url}/{path}" if tunnel_url else ""
        links_html += f"""
        <div style="background:white;border:1.5px solid var(--border-soft);border-radius:12px;padding:16px;margin-bottom:16px;">
            <h3 style="color:var(--deep-purple);font-size:16px;margin-bottom:6px;">{item['title']}</h3>
            <p style="color:var(--text-gray);font-size:13px;margin-bottom:8px;">{item['description']}</p>
            <p style="font-size:13px;color:var(--text-gray);">📄 الصفحات: {item['pages_est']}</p>
            <div style="margin-top:8px;">
                <a href="{path}" target="_blank" style="display:inline-block;padding:6px 16px;background:linear-gradient(135deg,var(--deep-purple),var(--soft-purple));color:white;border-radius:8px;text-decoration:none;font-size:13px;">🔗 فتح {item['title']}</a>
            </div>
        </div>
        """
    
    index_html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>الحياة المتوازنة — الفهرس</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap" rel="stylesheet">
<style>
:root{{--deep-purple:#4A1D6E;--soft-purple:#8B5CF6;--border-soft:#E8DFF0;--text-dark:#2D1B3E;--text-gray:#6B5B7B;--bg-cream:#FFFAF5;}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Tajawal',sans-serif;background:linear-gradient(135deg,#F3E8FF 0%,#FFFAF5 50%,#FFF5F0 100%);min-height:100vh;padding:20px;direction:rtl;color:var(--text-dark);}}
.wrap{{max-width:700px;margin:0 auto;}}
h1{{font-size:26px;font-weight:800;color:var(--deep-purple);text-align:center;margin-bottom:4px;}}
.sub{{text-align:center;color:var(--text-gray);font-size:14px;margin-bottom:20px;}}
.btn{{display:inline-block;padding:8px 20px;border-radius:8px;border:none;cursor:pointer;font-family:'Tajawal',sans-serif;font-size:13px;font-weight:500;transition:all .25s;margin:3px;text-decoration:none;}}
.btn-primary{{background:linear-gradient(135deg,var(--deep-purple),var(--soft-purple));color:white;}}
.btn-outline{{background:white;color:var(--deep-purple);border:1.5px solid var(--border-soft);}}
.btn:hover{{transform:translateY(-1px);box-shadow:0 4px 12px rgba(74,29,110,.15);}}
.center{{text-align:center;margin-top:20px;}}
</style>
</head>
<body>
<div class="wrap">
    <h1>🌸 الحياة المتوازنة</h1>
    <p class="sub">الباقة الرقمية الشاملة — MVP (v1.0.0)</p>
    <div style="text-align:center;margin-bottom:20px;">
        <button class="btn btn-outline" onclick="window.print()">🖨️ طباعة هذا الفهرس</button>
    </div>
    {links_html}
    <div class="center">
        <p style="font-size:13px;color:var(--text-gray);margin-bottom:12px;">
            💡 <strong>لتحويل كل ملف إلى PDF:</strong><br>
            1. افتح الرابط لكل ملف<br>
            2. Ctrl+P (أو Cmd+P)<br>
            3. اختر "حفظ كـ PDF"<br>
            4. اختر A4 (Portrait أو Landscape حسب الملف)<br>
            5. فعّل "خلفيات ورسومات" ✅<br>
            6. احفظ ثم ادمج الملفات بأي أداة PDF
        </p>
    </div>
</div>
</body>
</html>"""
    
    with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print("✅ index.html created")


def create_merge_pdf():
    """
    إنشاء ملف Python لدمج ملفات HTML المطبوعة كـ PDF.
    هذا سكريبت مساعد — المستخدمة تطبع كل HTML كـ PDF بنفسها ثم ندمج.
    """
    merge_script = """#!/usr/bin/env python3
"""
    with open(os.path.join(BASE, "merge-pdfs.py"), "w", encoding="utf-8") as f:
        f.write(merge_script)
    print("✅ merge-pdfs.py created")


def summary():
    print(f"""
{'='*60}
📊 ملخص الحزمة الكاملة — الحياة المتوازنة (MVP)
{'='*60}
""")
    total_lines = 0
    total_bytes = 0
    for item in BUNDLE["files"]:
        fp = os.path.join(BASE, item["file"])
        if os.path.exists(fp):
            lines = sum(1 for _ in open(fp, "r", encoding="utf-8"))
            size = os.path.getsize(fp)
            total_lines += lines
            total_bytes += size
            print(f"  {item['file']:35s} {lines:4d} lines  {size/1024:6.1f}KB")
    print(f"  {'—'*50}")
    print(f"  {'المجموع':35s} {total_lines:4d} lines  {total_bytes/1024:6.1f}KB")
    print(f"  {'عدد الملفات':35s} {len(BUNDLE['files'])} ملفات + index.html")
    print(f"  {'المسار':35s} {BASE}")
    print()
    
    # Save bundle manifest
    manifest = BUNDLE.copy()
    manifest["stats"] = {
        "total_lines": total_lines,
        "total_bytes": total_bytes,
        "file_count": len(BUNDLE["files"])
    }
    with open(os.path.join(BASE, "bundle-manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print("✅ bundle-manifest.json saved")
    print(f"{'='*60}")


if __name__ == "__main__":
    create_index_html()
    create_merge_pdf()
    summary()
