import streamlit as st 
import pandas as pd
import os
from io import BytesIO
import time  # Added for loading animations

st.set_page_config(page_title="Data Sweeper", layout="wide")

# 🎨 Custom CSS for Styling
st.markdown(
    """
    <style>
    .stApp{
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🧹 **Data Sweeper: Clean & Organize Your Data Efficiently!**
st.title("✨ Data Sweeper 🧹")
st.write("A tool to help you clean and organize your data easily.")

# 📂 **Upload Data File**
uploaded_file = st.file_uploader("📤 Upload your data file (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=False)

if uploaded_file:
    file_ext = os.path.splitext(uploaded_file.name)[-1].lower()
    
    if file_ext == ".csv":
        df = pd.read_csv(uploaded_file)
    elif file_ext == ".xlsx":
        df = pd.read_excel(uploaded_file)
    else:
        st.error(f"❌ Unsupported file type: {file_ext}")
        st.stop()
    
    # 🔍 **Preview Uploaded Data**
    st.subheader("🔍 Preview of the Data Frame")
    st.dataframe(df.head())
    
    # 🛠 **Data Cleaning Options**
    st.subheader("🛠 Data Cleaning Options")
    if st.checkbox(f"✅ Clean Data for {uploaded_file.name}"):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"🚀 Remove Duplicates from {uploaded_file.name}"):
                df.drop_duplicates(inplace=True)
                st.success("✅ Duplicates Removed Successfully!")
                time.sleep(1)  # Animation effect
                st.experimental_rerun()

        with col2:
            if st.button(f"🔧 Fill Missing Values for {uploaded_file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("✅ Missing Values Filled Successfully!")
                time.sleep(1)
                st.experimental_rerun()

    # 🎯 **Column Selection**
    st.subheader("🎯 Select Columns to Keep")
    selected_columns = st.multiselect(f"📝 Choose columns for {uploaded_file.name}", df.columns, default=df.columns)
    df = df[selected_columns]
    
    # 📊 **Data Visualization**
    st.subheader("📊 Data Visualization")
    if st.checkbox(f"📈 Show Visualization for {uploaded_file.name}"):
        st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
    
    # 🔄 **Conversion Options**
    st.subheader("🔄 Convert & Download")
    conversion_type = st.radio(f"📥 Convert {uploaded_file.name} to:", ["CSV", "Excel"], key=uploaded_file.name)
    
    if st.button(f"📤 Convert & Download {uploaded_file.name}"):
        buffer = BytesIO()
        if conversion_type == "CSV":
            df.to_csv(buffer, index=False)
            file_name = uploaded_file.name.replace(file_ext, ".csv")
            mime_type = "text/csv"
        elif conversion_type == "Excel":
            df.to_excel(buffer, index=False)
            file_name = uploaded_file.name.replace(file_ext, ".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        
        buffer.seek(0)
        
        st.download_button(
            label=f"⬇️ Download {file_name} as {conversion_type}",
            data=buffer,
            filename=file_name,
            mime_type=mime_type
        )
        
        st.success("✅ File Ready for Download!")