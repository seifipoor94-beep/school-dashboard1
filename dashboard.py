import streamlit as st
import pandas as pd
import os
from PIL import Image

st.set_page_config(page_title="📊 داشبورد گزارش نمرات", layout="wide")
st.title("📊 داشبورد گزارش نمرات دانش‌آموز")

# بارگذاری اطلاعات کاربران
users_df = pd.read_excel("data/users.xlsx")
users_df.columns = users_df.columns.str.strip().str.replace('\u200c', ' ').str.replace('\xa0', ' ')

# فرم ورود
st.sidebar.title("🔐 ورود به داشبورد")
entered_role = st.sidebar.selectbox("نقش خود را انتخاب کنید:", ["والد", "آموزگار", "مدیر"])
entered_code = st.sidebar.text_input("رمز ورود:", type="password")

# بررسی اعتبار
valid_user = users_df[(users_df["نقش"] == entered_role) & (users_df["رمز ورود"] == entered_code)]

if valid_user.empty:
    st.warning("❌ رمز یا نقش اشتباه است.")
    st.stop()

user_name = valid_user.iloc[0]["نام کاربر"]
st.success(f"✅ خوش آمدید {user_name} عزیز! شما به‌عنوان {entered_role} وارد شده‌اید.")

# انتخاب درس
lesson_dirs = [d for d in os.listdir("charts") if os.path.isdir(os.path.join("charts", d))]
selected_lesson = st.selectbox("درس مورد نظر را انتخاب کنید:", lesson_dirs)

chart_dir = os.path.join("charts", selected_lesson)
report_dir = os.path.join("reports", selected_lesson)

# انتخاب دانش‌آموز بر اساس نقش
student_files = [f for f in os.listdir(chart_dir) if f.endswith("_chart.png") and not f.startswith("class")]
student_names = sorted(list(set([f.split("_")[0] for f in student_files])))

if entered_role == "والد":
    selected_student = user_name
else:
    selected_student = st.selectbox("دانش‌آموز را انتخاب کنید:", student_names)

# نمایش نمودارهای کلی کلاس
st.subheader("📈 نمودارهای کلی کلاس")
scatter_path = os.path.join(chart_dir, f"class_scatter_{selected_lesson}.png")
pie_path = os.path.join(chart_dir, f"class_pie_{selected_lesson}.png")

col1, col2 = st.columns(2)
with col1:
    if os.path.exists(scatter_path):
        st.image(Image.open(scatter_path), caption="نمودار پراکندگی نمرات کلاس")
with col2:
    if os.path.exists(pie_path):
        st.image(Image.open(pie_path), caption="نمودار دایره‌ای دسته‌بندی نمرات")

# نمایش رتبه‌بندی درس
rank_path = os.path.join(report_dir, f"rank_{selected_lesson}.txt")
if os.path.exists(rank_path):
    st.subheader("🏆 رتبه‌بندی دانش‌آموزها در این درس")
    with open(rank_path, encoding='utf-8') as f:
        st.text(f.read())

# نمایش نمودار فردی
student_chart_path = os.path.join(chart_dir, f"{selected_student}_{selected_lesson}_chart.png")
if os.path.exists(student_chart_path):
    st.subheader(f"📊 نمودار نمرات {selected_student}")
    st.image(Image.open(student_chart_path))

# نمایش گزارش متنی فردی
student_report_path = os.path.join(report_dir, f"{selected_student}_{selected_lesson}.txt")
if os.path.exists(student_report_path):
    st.subheader("📝 گزارش متنی نمرات")
    with open(student_report_path, encoding='utf-8') as f:
        st.text(f.read())

# نمایش رتبه‌بندی کلی فقط برای مدیر
if entered_role == "مدیر" and st.checkbox("نمایش رتبه‌بندی کلی همه درس‌ها"):
    if os.path.exists("reports/rank_kolli.txt"):
        st.subheader("🏆 رتبه‌بندی کلی دانش‌آموزها")
        with open("reports/rank_kolli.txt", encoding='utf-8') as f:
            st.text(f.read())
