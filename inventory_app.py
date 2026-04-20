import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة
st.set_page_config(page_title="مستودع الزهراء - أوفلاين", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="css"], .stApp {
        font-family: 'Cairo', sans-serif !important;
        direction: RTL !important;
        text-align: right !important;
    }
    .header { background: #1e3a8a; color: white; padding: 20px; border-radius: 15px; text-align: center; }
    .big-label { font-size: 22px; font-weight: 900; color: #1e3a8a; margin: 15px 0; display: block; }
    </style>
    <div class="header"><h1>🏢 مستودع الزهراء (نسخة الموبايل)</h1></div>
    """, unsafe_allow_html=True)

# كود السحر (JavaScript) لحفظ البيانات داخل ذاكرة الموبايل بدون إنترنت
st.markdown('<span class="big-label">📦 إضافة وجرد المواد</span>', unsafe_allow_html=True)

custom_js = """
<div dir="rtl" style="font-family: 'Cairo';">
    <input type="text" id="itemName" placeholder="اسم المادة" style="width:100%; padding:15px; margin-bottom:10px; border-radius:10px; border:1px solid #ccc; font-size:18px;"><br>
    <input type="text" id="itemComp" placeholder="الشركة" style="width:100%; padding:15px; margin-bottom:10px; border-radius:10px; border:1px solid #ccc; font-size:18px;"><br>
    <input type="text" id="itemBatch" placeholder="الوجبة" style="width:100%; padding:15px; margin-bottom:10px; border-radius:10px; border:1px solid #ccc; font-size:18px;"><br>
    <button onclick="saveItem()" style="width:100%; padding:15px; background:#1e3a8a; color:white; border:none; border-radius:10px; font-weight:bold; font-size:20px;">💾 حفظ في ذاكرة الموبايل</button>
    
    <h3 style="margin-top:20px; color:#1e3a8a;">📋 المواد المحفوظة:</h3>
    <div id="displayArea"></div>
</div>

<script>
    function saveItem() {
        const name = document.getElementById('itemName').value;
        const comp = document.getElementById('itemComp').value;
        const batch = document.getElementById('itemBatch').value;
        
        if(name) {
            const newItem = { name, comp, batch, id: Date.now() };
            let items = JSON.parse(localStorage.getItem('hospital_inventory') || '[]');
            items.push(newItem);
            localStorage.setItem('hospital_inventory', JSON.stringify(items));
            displayItems();
            document.getElementById('itemName').value = '';
        }
    }

    function displayItems() {
        const items = JSON.parse(localStorage.getItem('hospital_inventory') || '[]');
        const area = document.getElementById('displayArea');
        area.innerHTML = items.map(item => `
            <div style="background:white; border-right:8px solid #1e3a8a; padding:15px; margin-bottom:10px; border-radius:10px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
                <b style="font-size:20px; color:#1e3a8a;">📦 ${item.name}</b><br>
                <span>🏢 الشركة: ${item.comp}</span> | <span>🔢 الوجبة: ${item.batch}</span>
                <br><button onclick="deleteItem(${item.id})" style="color:red; background:none; border:none; cursor:pointer; margin-top:5px;">🗑️ حذف</button>
            </div>
        `).join('');
    }

    function deleteItem(id) {
        let items = JSON.parse(localStorage.getItem('hospital_inventory') || '[]');
        items = items.filter(item => item.id !== id);
        localStorage.setItem('hospital_inventory', JSON.stringify(items));
        displayItems();
    }

    // تشغيل العرض عند فتح الصفحة
    displayItems();
</script>
"""

components.html(custom_js, height=800, scrolling=True)