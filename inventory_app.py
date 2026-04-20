import streamlit as st
import pandas as pd
from datetime import date, datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="نظام إدارة المواد", layout="wide")

# --- التنسيق الاحترافي (بدون تمرير عرضي) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Cairo', sans-serif;
        direction: RTL;
        text-align: right;
        background-color: #f4f7f9;
    }

    /* الحاوية الرئيسية */
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }

    /* تنسيق العناوين للحقول */
    .stTextInput label, .stDateInput label {
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #1e3a8a !important;
    }

    /* تنسيق الصفوف لتبدو كجدول متناسق بدون تمرير */
    .table-row {
        background-color: white;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 5px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: nowrap; /* يمنع التمرير */
    }

    .cell {
        font-size: 14px; /* تصغير الخط للموبايل */
        padding: 2px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    /* إخفاء الزوائد */
    div[data-testid="stVerticalBlock"] > div {
        padding: 0px !important;
    }

    /* تحسين شكل الأزرار */
    .stButton > button {
        border-radius: 10px;
        font-size: 14px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- واجهة المستخدم ---
st.markdown("""
    <div class="main-header">
        <h2 style='margin:0; font-size: 28px;'>📦 مستودع الزهراء الرقمي</h2>
        <p style='margin:0; font-size: 14px;'>الإدارة الذكية للمخزون</p>
    </div>
    """, unsafe_allow_html=True)

# إدارة البيانات
if 'inventory' not in st.session_state:
    st.session_state.inventory = []

# قسم الإضافة (مختصر للموبايل)
with st.expander("➕ إضافة مادة"):
    n = st.text_input("المادة")
    c = st.text_input("الشركة")
    b = st.text_input("الوجبة")
    e = st.date_input("النفاذ")
    if st.button("حفظ", use_container_width=True):
        if n and c:
            st.session_state.inventory.append({"n": n, "c": c, "b": b, "e": str(e)})
            st.rerun()

st.markdown("### 📋 جرد المواد")
search = st.text_input("", placeholder="ابحث هنا...")

# عرض البيانات بنظام الأعمدة المرنة
items = st.session_state.inventory
if search:
    items = [i for i in items if search in i['n'] or search in i['c']]

if items:
    # رؤوس الأعمدة - توزيع المساحة بذكاء (الاسم يأخذ مساحة أكبر)
    h1, h2, h3, h4 = st.columns([2.5, 2, 2, 0.8])
    with h1: st.caption("المادة")
    with h2: st.caption("الشركة")
    with h3: st.caption("النفاذ")
    with h4: st.caption("حذف")

    for idx, item in enumerate(items):
        col1, col2, col3, col4 = st.columns([2.5, 2, 2, 0.8])
        
        # تنسيق لون التاريخ
        exp_date = datetime.strptime(item['e'], '%Y-%m-%d').date()
        date_color = "red" if (exp_date - date.today()).days < 30 else "black"

        with col1: st.markdown(f"**{item['n']}**")
        with col2: st.write(f"{item['c']}")
        with col3: st.markdown(f"<span style='color:{date_color}; font-size:12px;'>{item['e']}</span>", unsafe_allow_html=True)
        with col4: 
            if st.button("🗑️", key=f"d_{idx}"):
                st.session_state.inventory.pop(idx)
                st.rerun()
        st.divider()
else:
    st.info("لا توجد بيانات")