import sqlite3
from datetime import date, datetime
import streamlit as st

# --- إعداد قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS materials
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  company TEXT,
                  batch_number TEXT,
                  expiry_date DATE)''')
    conn.commit()
    conn.close()

def add_material(name, company, batch, expiry):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("INSERT INTO materials (name, company, batch_number, expiry_date) VALUES (?,?,?,?)",
              (name, company, batch, expiry))
    conn.commit()
    conn.close()

def delete_material(material_id):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("DELETE FROM materials WHERE id = ?", (material_id,))
    conn.commit()
    conn.close()

def view_all_materials():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT id, name, company, expiry_date, batch_number FROM materials ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المستودع الذكي", layout="wide")

# --- تنسيق CSS المطور ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;700;900&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Cairo', sans-serif;
        direction: RTL;
        text-align: right;
        background-color: #f8fafc;
    }

    /* العنوان الرئيسي يمين تماماً */
    .header-container {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: right; /* ضمان الاتجاه لليمين */
    }

    /* تكبير عناوين الحقول */
    .stTextInput label, .stDateInput label {
        font-size: 32px !important;
        font-weight: 900 !important;
        color: #1e293b !important;
        margin-bottom: 15px !important;
        display: block;
    }

    /* إلغاء تعليمات Enter */
    div[data-testid="stInstructions"] {
        display: none !important;
    }

    input {
        border-radius: 10px !important;
        border: 2px solid #cbd5e1 !important;
        padding: 15px !important;
        font-size: 20px !important;
        text-align: right !important;
    }

    /* تنسيق البطاقات للجرد */
    .data-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 8px;
        text-align: right;
        font-size: 18px;
    }

    .column-header {
        font-weight: 900;
        color: #475569;
        font-size: 18px;
        padding: 10px;
        text-align: center;
    }

    /* زر الحذف */
    .stButton > button {
        border-radius: 10px;
        font-weight: bold;
    }
    
    .del-btn-container button {
        background-color: #fee2e2 !important;
        color: #ef4444 !important;
        border: 1px solid #fecaca !important;
    }
    </style>
    """, unsafe_allow_html=True)

init_db()

# --- واجهة المستخدم ---
st.markdown("""
    <div class="header-container">
        <h1 style='margin:0; font-size: 40px;'>📦 نظام إدارة المستودع الذكي</h1>
        <p style='margin:0; opacity: 0.9; font-size: 20px;'>مستشفى الزهراء التعليمي - الإدارة الرقمية</p>
    </div>
    """, unsafe_allow_html=True)

# قسم الإدخال
with st.expander("➕ إضافة مادة جديدة", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("اسم المادة")
        company = st.text_input("اسم الشركة")
    with col2:
        batch = st.text_input("رقم الوجبة")
        expiry = st.date_input("تاريخ الانتهاء")
    
    if st.button("💾 حفظ البيانات في المستودع", type="primary", use_container_width=True):
        if name and company and batch:
            add_material(name, company, batch, expiry)
            st.success(f"تم حفظ {name} بنجاح")
            st.rerun()

st.write("---")

# --- جرد المواد ---
st.markdown("<h2 style='text-align: right; font-size: 35px; color: #1e3a8a;'>🔍 جرد المواد الحالي</h2>", unsafe_allow_html=True)
search_query = st.text_input("", placeholder="ابحث هنا عن أي مادة أو شركة...")

data = view_all_materials()
if search_query:
    filtered_data = [row for row in data if search_query.lower() in str(row[1]).lower() or search_query.lower() in str(row[2]).lower()]
else:
    filtered_data = data

# رؤوس الجدول
h1, h2, h3, h4, h5, h6 = st.columns([0.5, 2.5, 2, 2, 2, 0.8])
h1.markdown('<div class="column-header">ت</div>', unsafe_allow_html=True)
h2.markdown('<div class="column-header">اسم المادة</div>', unsafe_allow_html=True)
h3.markdown('<div class="column-header">الشركة</div>', unsafe_allow_html=True)
h4.markdown('<div class="column-header">تاريخ النفاذ</div>', unsafe_allow_html=True)
h5.markdown('<div class="column-header">الوجبة</div>', unsafe_allow_html=True)
h6.markdown('<div class="column-header">حذف</div>', unsafe_allow_html=True)

if filtered_data:
    for r in filtered_data:
        # تنبيه التاريخ
        expiry_date = datetime.strptime(str(r[3]), '%Y-%m-%d').date()
        is_expired = (expiry_date - date.today()).days < 30
        date_style = "color: red; font-weight: bold;" if is_expired else "color: black;"
        
        c1, c2, c3, c4, c5, c6 = st.columns([0.5, 2.5, 2, 2, 2, 0.8])
        c1.markdown(f'<div class="data-card" style="text-align:center">{r[0]}</div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="data-card"><b>{r[1]}</b></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="data-card">{r[2]}</div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="data-card" style="{date_style}">{r[3]}</div>', unsafe_allow_html=True)
        c5.markdown(f'<div class="data-card">{r[4]}</div>', unsafe_allow_html=True)
        
        if c6.button("❌", key=f"del_{r[0]}"):
            delete_material(r[0])
            st.rerun()
else:
    st.info("لا توجد بيانات مسجلة حالياً.")