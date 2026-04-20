import streamlit as st
import streamlit.components.v1 as components

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="مستودع الزهراء - النسخة النهائية", layout="centered")

# 2. تصميم رأس الصفحة (نفس الألوان اللي تحبها)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="css"], .stApp {
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
        <p style='margin:0; font-size: 14px;'>نسخة الحفظ الدائم (أوفلاين 100%)</p>
    </div>
    """, unsafe_allow_html=True)

# 3. كود التطبيق المتكامل (HTML + JS + CSS)
# ملاحظة: هذا الجزء هو اللي يحتوي على البحث والإضافة القابلة للطي
html_code = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Cairo', sans-serif; background-color: #f4f7fa; padding: 10px; direction: rtl; }
        .label-big { font-size: 22px; font-weight: 900; color: #1e3a8a; display: block; }
        
        /* تصميم حقول الإدخال */
        input { width: 100%; padding: 15px; margin-bottom: 10px; border-radius: 10px; border: 2px solid #1e3a8a; font-size: 18px; box-sizing: border-box; text-align: right; }
        
        /* تصميم الأزرار */
        .btn-save { width: 100%; padding: 15px; background: #1e3a8a; color: white; border: none; border-radius: 10px; font-weight: 900; font-size: 20px; cursor: pointer; }
        .btn-toggle { cursor:pointer; background:#fff; padding:15px; border-radius:10px; margin-bottom:10px; border-right:10px solid #1e3a8a; box-shadow: 0 2px 5px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; }
        
        /* تصميم البطاقات */
        .card { background: white; border-right: 10px solid #1e3a8a; padding: 15px; margin-top: 15px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align: right; }
        .card-title { font-size: 24px; font-weight: 900; color: #1e3a8a; display: block; border-bottom: 1px solid #eee; padding-bottom: 5px; }
        .card-info { font-size: 19px; color: #334155; margin-top: 5px; font-weight: bold; }
        .del-btn { color: #dc2626; font-weight: bold; background: #fff; border: 1px solid #dc2626; padding: 8px 15px; border-radius: 5px; margin-top: 10px; cursor: pointer; font-size: 16px; }
    </style>
</head>
<body>

    <div class="btn-toggle" onclick="toggleAdd()">
        <span class="label-big">➕ إضافة مادة جديدة</span>
        <span id="arrow">▼</span>
    </div>

    <div id="addSection" style="display:none; background:#fff; padding:15px; border-radius:10px; border:1px solid #ccc; margin-bottom:20px;">
        <input type="text" id="n" placeholder="اسم المادة">
        <input type="text" id="c" placeholder="اسم الشركة">
        <input type="text" id="b" placeholder="رقم الوجبة">
        <input type="text" id="e" placeholder="تاريخ النفاذ (مثلاً 2026/04/20)">
        <button class="btn-save" onclick="add()">💾 حفظ في الموبايل</button>
    </div>

    <hr>

    <span class="label-big" style="margin-top:20px;">🔍 ابحث عن مادة أو شركة:</span>
    <input type="text" id="searchInput" onkeyup="render()" placeholder="اكتب هنا للبحث...">

    <span class="label-big" style="margin-top:20px;">📋 جرد المواد الحالي:</span>
    <div id="list"></div>

    <script>
        // وظيفة الإخفاء والإظهار
        function toggleAdd() {
            const section = document.getElementById('addSection');
            const arrow = document.getElementById('arrow');
            if (section.style.display === "none") {
                section.style.display = "block";
                arrow.innerHTML = "▲";
            } else {
                section.style.display = "none";
                arrow.innerHTML = "▼";
            }
        }

        // وظيفة إضافة مادة
        function add() {
            const name = document.getElementById('n').value;
            const comp = document.getElementById('c').value;
            const batch = document.getElementById('b').value;
            const exp = document.getElementById('e').value;

            if(!name) { alert("الرجاء كتابة اسم المادة"); return; }

            const item = { name, comp, batch, exp, id: Date.now() };
            let data = JSON.parse(localStorage.getItem('hosp_data') || '[]');
            data.push(item);
            localStorage.setItem('hosp_data', JSON.stringify(data));
            
            render(); // تحديث القائمة
            toggleAdd(); // إغلاق القائمة بعد الحفظ
            
            // تفريغ الحقول
            document.getElementById('n').value=''; document.getElementById('c').value=''; 
            document.getElementById('b').value=''; document.getElementById('e').value='';
        }

        // وظيفة العرض والبحث
        function render() {
            const data = JSON.parse(localStorage.getItem('hosp_data') || '[]');
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            
            const filteredData = data.filter(i => 
                i.name.toLowerCase().includes(searchTerm) || 
                i.comp.toLowerCase().includes(searchTerm)
            );

            document.getElementById('list').innerHTML = filteredData.map(i => `
                <div class="card">
                    <span class="card-title">📦 ${i.name}</span>
                    <div class="card-info">🏢 الشركة: ${i.comp}</div>
                    <div class="card-info">🔢 الوجبة: ${i.batch}</div>
                    <div class="card-info">📅 النفاذ: <span style="color:red">${i.exp}</span></div>
                    <button class="del-btn" onclick="del(${i.id})">🗑️ حذف المادة</button>
                </div>
            `).reverse().join('');
        }

        // وظيفة الحذف
        function del(id) {
            if(confirm("هل أنت متأكد من حذف هذه المادة؟")) {
                let data = JSON.parse(localStorage.getItem('hosp_data') || '[]');
                data = data.filter(i => i.id !== id);
                localStorage.setItem('hosp_data', JSON.stringify(data));
                render();
            }
        }

        // تشغيل العرض عند فتح الصفحة
        render();
    </script>
</body>
</html>
"""

# 4. تشغيل الكود في Streamlit
components.html(html_code, height=1200, scrolling=True)