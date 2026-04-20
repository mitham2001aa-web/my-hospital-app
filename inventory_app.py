import streamlit as st
import pandas as pd
from datetime import date, datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="مستودع الزهراء الرقمي", layout="centered")

# --- التنسيق الاحترافي (تركيز على اليمين والخطوط الكبيرة) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Cairo', sans-serif !important;
        direction: RTL !important;
        text-align: right !important;
    }

    /* رأس الصفحة */
    .header-box {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
    }

    /* تكبير عناوين حقول الإضافة */
    .stTextInput label, .stDateInput label {
        font-size: 24px !important; /* خط كبير جداً */
        font-weight: 900 !important; /* عريض جداً */
        color: #1e3a8a !important;
        display: block !important;
        text-align: right !important;
        margin-bottom: 10px !important;
    }

    /* تصميم البطاقة القديم المحسن (بداية من اليمين) */
    .item-card {
        background-color: white;
        border-right: 8px solid #1e3a8a; 
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: right;
    }

    .item-name {
        color: #1e3a8a;
        font-size: 24px;
        font-weight: 900;
        border-bottom: 1px solid #eee;
        padding-bottom: 8px;
        margin-bottom: 10px;
        display: block;
    }

    .info-line {
        font-size: 18px;
        margin-bottom: 5px;
        color: #334155;
    }

    .info-label {
        font-weight: bold;
        color: #64748b;
    }

    /* محاذاة العناوين الجانبية (البحث والجرد) لليمين */
    .right-align-text {
        text-align: right !important;
        direction: rtl !important;
        width: 100%;
        display: block;
        font-weight: 900;
        font-size: 22px;
        color: #1e3a8a;
        margin-bottom: 10px;
    }

    /* زر الحفظ */
    .stButton > button {
        font-size: 20px !important;
        font-weight: bold !important;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- العنوان الرئيسي ---
st.markdown("""
    <div class="header-box">
        <h1 style='margin:0; font-size: 28px;'>🏢 مستودع الزهراء التعليمي</h1>
    </div>
    """, unsafe_allow_html=True)

if 'inventory' not in st.session_state:
    st.session_state.inventory = []

# --- قسم الإضافة (عناوين كبيرة وواضحة) ---
with st.expander("➕ إضافة مادة جديدة للمخزن", expanded=True):
    name = st.text_input("اسم المادة")
    comp = st.text_input("الشركة المصنعة")
    batch = st.text_input("رقم الوجبة")
    exp = st.date_input("تاريخ النفاذ")
    
    if st.button("💾 حفظ البيانات الآن", use_container_width=True):
        if name and comp:
            st.session_state.inventory.append({"n": name, "c": comp, "b": batch, "e": str(exp)})
            st.success("تم الحفظ!")
            st.rerun()

st.divider()

# --- قسم البحث (محاذاة يمين) ---
st.markdown('<span class="right-align-text">🔍 ابحث عن مادة أو شركة</span>', unsafe_allow_html=True)
search = st.text_input("", placeholder="اكتب هنا للبحث...", label_visibility="collapsed")

# --- قسم الجرد (محاذاة يمين) ---
st.markdown(f'<span class="right-align-text">📋 جرد المواد الحالي ({len(st.session_state.inventory)})</span>', unsafe_allow_html=True)

items = st.session_state.inventory
if search:
    items = [i for i in items if search in i['n'] or search in i['c']]

if items:
    for idx, item in enumerate(items):
        exp_date = datetime.strptime(item['e'], '%Y-%m-%d').date()
        date_color = "red" if (exp_date - date.today()).days < 30 else "green"
        
        # البطاقة بتصميمها القديم مع ضمان اليمين
        st.markdown(f"""
            <div class="item-card">
                <span class="item-name">📦 {item['n']}</span>
                <div class="info-line"><span class="info-label">الشركة:</span> {item['c']}</div>
                <div class="info-line"><span class="info-label">الوجبة:</span> {item['b']}</div>
                <div class="info-line"><span class="info-label">تاريخ النفاذ:</span> <span style="color:{date_color}; font-weight:bold;">{item['e']}</span></div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"🗑️ حذف {item['n']}", key=f"del_{idx}", use_container_width=True):
            st.session_state.inventory.pop(idx)
            st.rerun()
else:
    st.info("لا توجد مواد حالياً.")