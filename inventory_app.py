import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة
st.set_page_config(page_title="مستودع الزهراء - أوفلاين 100%", layout="centered")

# التصميم اللي تحبه (نفس الألوان والخطوط العريضة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, .stApp {
        font-family: 'Cairo', sans-serif !important;
        direction: RTL !important;
        text-align: right !important;
    }
    .header-box {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 10px;
    }
    </style>
    <div class="header-box">
        <h1 style='margin:0; font-size: 26px;'>🏢 مستودع الزهراء التعليمي</h1>
        <p style='margin:0; font-size: 14px;'>نسخة الحفظ الدائم (أوفلاين)</p>
    </div>
    """, unsafe_allow_html=True)

# كود التطبيق المتكامل (يعمل داخل الآيفون بدون سيرفر)
html_code = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Cairo', sans-serif; background-color: #f4f7fa; padding: 10px; }
        .label-big { font-size: 24px; font-weight: 900; color: #1e3a8a; margin: 15px 0 5px 0; display: block; }
        input { width: 100%; padding: 15px; margin-bottom: 10px; border-radius: 10px; border: 2px solid #1e3a8a; font-size: 18px; box-sizing: border-box; }
        button { width: 100%; padding: 15px; background: #1e3a8a; color: white; border: none; border-radius: 10px; font-weight: 900; font-size: 20px; cursor: pointer; }
        .card { background: white; border-right: 10px solid #1e3a8a; padding: 15px; margin-top: 15px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .card-title { font-size: 24px; font-weight: 900; color: #1e3a8a; display: block; border-bottom: 1px solid #eee; padding-bottom: 5px; }
        .card-info { font-size: 19px; color: #334155; margin-top: 5px; font-weight: bold; }
        .del-btn { color: #dc2626; font-weight: bold; background: none; border: 1px solid #dc2626; padding: 5px 10px; border-radius: 5px; margin-top: 10px; width: auto; font-size: 14px; }
    </style>
</head>
<body>
    <span class="label-big">➕ إضافة مادة جديدة:</span>
    <input type="text" id="n" placeholder="اسم المادة">
    <input type="text" id="c" placeholder="اسم الشركة">
    <input type="text" id="b" placeholder="رقم الوجبة">
    <input type="text" id="e" placeholder="تاريخ النفاذ (مثلاً 2026/04/20)">
    <button onclick="add()">💾 حفظ في ذاكرة الموبايل</button>

    <span class="label-big" style="margin-top:30px;">📋 جرد المواد الحالي:</span>
    <div id="list"></div>

    <script>
        function add() {
            const item = {
                name: document.getElementById('n').value,
                comp: document.getElementById('c').value,
                batch: document.getElementById('b').value,
                exp: document.getElementById('e').value,
                id: Date.now()
            };
            if(!item.name) return;
            let data = JSON.parse(localStorage.getItem('hosp_data') || '[]');
            data.push(item);
            localStorage.setItem('hosp_data', JSON.stringify(data));
            render();
            document.getElementById('n').value=''; document.getElementById('c').value=''; document.getElementById('b').value=''; document.getElementById('e').value='';
        }

        function render() {
            const data = JSON.parse(localStorage.getItem('hosp_data') || '[]');
            document.getElementById('list').innerHTML = data.map(i => `
                <div class="card">
                    <span class="card-title">📦 ${i.name}</span>
                    <div class="card-info">🏢 الشركة: ${i.comp}</div>
                    <div class="card-info">🔢 الوجبة: ${i.batch}</div>
                    <div class="card-info">📅 النفاذ: <span style="color:red">${i.exp}</span></div>
                    <button class="del-btn" onclick="del(${i.id})">🗑️ حذف</button>
                </div>
            `).reverse().join('');
        }

        function del(id) {
            let data = JSON.parse(localStorage.getItem('hosp_data') || '[]');
            data = data.filter(i => i.id !== id);
            localStorage.setItem('hosp_data', JSON.stringify(data));
            render();
        }
        render();
    </script>
</body>
</html>
"""

# عرض الكود داخل Streamlit
components.html(html_code, height=1000, scrolling=True)