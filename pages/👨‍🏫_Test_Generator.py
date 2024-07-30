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
import PyPDF2

st.set_page_config(
    page_title="Test Generator", 
    page_icon="🤖",
)

st.write("# Test Generator 👨‍🏫")

uploaded_file = st.file_uploader("Upload file")

if not uploaded_file:
    st.stop()

num_question = st.selectbox(
   "Choose number of question:",
    ("5", "10", "15", "20"),
     index=None
)

if not num_question:
    st.stop()

question_type = st.selectbox(
    "Choose question type:",
     ("Multiple choice", "True/False", "Fill in the blank"),
      index=None
    )

if not question_type:
    st.stop()

difficulty = st.selectbox(
    "Choose difficulty level:",
     ("Easy", "Medium", "Hard"),
      index=None
    )

if not difficulty:
    st.stop()

limit = st.selectbox(
    "Limit the content in the file?",
    ('Yes', 'No'),
    index=None
)

if not limit:
    st.stop()

prompt = f"From the input file, generate a test with {num_question} questions of type {question_type} with difficulty level {difficulty}."

if limit == 'Yes':
    # file = open(uploaded_file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(BytesIO(uploaded_file.read()))
    num_pages = pdfReader.getNumPages()

    # st.markdown(f"Number of pages in the file: {num_pages}")

    limit_range = st.slider("Choose the page range of the file:", 1, num_pages, (1, num_pages))
    st.markdown(f"Content range: {limit_range[0]} - {limit_range[1]}")
    extra_prompt = f" Limit the content in the file from page {limit_range[0]} to page {limit_range[1]}."
    prompt = prompt + extra_prompt

prompt = prompt + " At the end of the test, add a new section to provide the correct answer and detailed explanation for each question. Also refer to the page number in the file for each question and quote the relevant text."
st.markdown(prompt)

if st.button("Generate Test"):
    request_gpt(uploaded_file, prompt, "test")
    