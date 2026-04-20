import streamlit as st
import pandas as pd
from datetime import date, datetime

# --- إعدادات الصفحة للموبايل ---
st.set_page_config(page_title="مستودع الزهراء", layout="centered")

# --- تنسيق CSS مخصص للموبايل والحاسبة ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Cairo', sans-serif;
        direction: RTL;
        text-align: right;
    }
    
    /* تصميم البطاقة الاحترافية */
    .inventory-card {
        background-color: white;
        border: 2px solid #1e3a8a;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    
    .card-title {
        color: #1e3a8a;
        font-size: 22px;
        font-weight: 900;
        border-bottom: 1px solid #eee;
        padding-bottom: 5px;
        margin-bottom: 10px;
    }
    
    .card-detail {
        font-size: 18px;
        margin-bottom: 5px;
    }
    
    .label {
        font-weight: bold;
        color: #555;
    }

    /* تنسيق العناوين الكبيرة */
    .stTextInput label, .stDateInput label {
        font-size: 24px !important;
        font-weight: 900 !important;
        color: #1e3a8a !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📦 مستودع الزهراء الرقمي")

# --- الاتصال بالبيانات (استخدمنا هنا مثال بسيط، تأكد من ربط جدولك) ---
# سأضع هنا كود تجريبي، استبدله بكود الربط الخاص بك إذا كان جاهزاً
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["اسم المادة", "الشركة", "رقم الوجبة", "تاريخ الانتهاء"])

# --- قسم الإضافة ---
with st.expander("➕ إضافة مادة جديدة", expanded=False):
    name = st.text_input("اسم المادة")
    comp = st.text_input("اسم الشركة")
    batch = st.text_input("رقم الوجبة")
    expiry = st.date_input("تاريخ الانتهاء")
    
    if st.button("💾 حفظ البيانات"):
        if name and comp:
            new_row = pd.DataFrame([{"اسم المادة": name, "الشركة": comp, "رقم الوجبة": batch, "تاريخ الانتهاء": str(expiry)}])
            st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
            st.success("تم الحفظ!")
            st.rerun()

st.divider()

# --- قسم البحث ---
search_query = st.text_input("🔍 ابحث عن مادة...")

df = st.session_state.data
if search_query:
    df = df[df['اسم المادة'].str.contains(search_query, na=False)]

# --- عرض البيانات بنظام البطاقات (Card System) ---
if not df.empty:
    for i, row in df.iterrows():
        # تنبيه التاريخ
        try:
            days_left = (datetime.strptime(row["تاريخ الانتهاء"], '%Y-%m-%d').date() - date.today()).days
            date_color = "red" if days_left < 30 else "#1e3a8a"
        except: date_color = "black"

        st.markdown(f"""
            <div class="inventory-card">
                <div class="card-title">📦 {row['اسم المادة']}</div>
                <div class="card-detail"><span class="label">الشركة:</span> {row['الشركة']}</div>
                <div class="card-detail"><span class="label">الوجبة:</span> {row['رقم الوجبة']}</div>
                <div class="card-detail" style="color: {date_color};">
                    <span class="label">تاريخ النفاذ:</span> {row['تاريخ الانتهاء']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # زر الحذف تحت كل بطاقة
        if st.button(f"❌ حذف {row['اسم المادة']}", key=f"del_{i}"):
            st.session_state.data = st.session_state.data.drop(i)
            st.rerun()
else:
    st.info("لا توجد مواد حالياً.")