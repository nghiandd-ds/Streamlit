import streamlit as st
from openai import OpenAI
import numpy as np
import pandas as pd
import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from io import BytesIO
from base import request_gpt

st.set_page_config(
    page_title="AI Summary", 
    page_icon="🤖",
)

st.write("# Summarization Tool 📄")
    
# upload file by streamlit
uploaded_file = st.file_uploader("Upload file")

if not uploaded_file:
    st.stop()    

option = st.selectbox(
   "What type of document do you want to summarize?",
   ("Default", "Book", "Paper", "Article"),
    index=None
)

if not option:
    st.stop()

if option == "Default":
    prompt = """Provide a summary of the document."""
elif option == "Book":
    prompt = """Provide a summary of the book."""
elif option == "Paper":
    option_2 = st.selectbox(
        "What part do you want to focus on?",
        ("Abstract", "Introduction", "Methodology", "Results", "Conclusion"),
        index=None)
    
    if not option_2:
        st.stop()
    
    prompt = f"""
    Provide a long, detailed summary of the paper with the following format:
        1. Authors:
        2. Published date:
        3. Title:
        4. Abstract:
        5. Introduction:
        6. Methodology:
        7. Results:
        8. Conclusion:
        9. References:
    Must be very detailed in part {option_2}, be brief in other parts.
    Must be very precise, must not make up words, use the words in the paper.
    """
elif option == "Article":
    prompt = """Provide a summary of the article."""

print(prompt)

request_gpt(uploaded_file, prompt, "summary")
