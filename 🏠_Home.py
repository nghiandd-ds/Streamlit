import streamlit as st

st.set_page_config(
    page_title="Quant Retail AI",
    page_icon="🤖",
)

st.write("# Quant Retail AI 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Giới thiệu: 
    -    Bản Beta Quant Retail AI được xây dựng với mục đích thử nghiệm.
    -    Các chức năng hiện có:
            + Tóm tắt văn bản.
            + Kiểm tra code python.
    Hướng dẫn sử dụng:
        B1: Chọn chức năng muốn sử dụng
        B2: Upfile theo chức năng từ máy tính/điện thoại
        B3: Download file kết quả
    Powered by:
        OpenAI
        Streamlit
"""
)
