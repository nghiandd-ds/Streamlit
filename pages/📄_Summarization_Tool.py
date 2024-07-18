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

st.set_page_config(
    page_title="AI Summary", 
    page_icon="🤖",
)

st.write("# Summarization Tool 📄")

# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")


# if not openai_api_key:
#     st.info("Please add your OpenAI API key to continue.")
#     st.stop()
    
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


a = 'sk-proj-50i25Vf5uMtQ8EpYF'
b = 'AyaT3BlbkFJ2B9b6oBxsJpx058Zxocv'

# Connect to Openai API
client = OpenAI(api_key=a+b)

# Upload file to OpenAI and take ID
gpt_file = client.files.create(
    file=uploaded_file,
    purpose='assistants').id

assistant = client.beta.assistants.create(
    model="gpt-3.5-turbo-0125",
    instructions="You are a bank employee who works in the Risk Management department. \
                  Your job is to read and understand the attached document and summarize it for your manager.",
    name="Summary Assistant",
    tools=[{"type": "file_search"}]
).id

# Create thread
my_thread = client.beta.threads.create()

# add message
my_thread_message = client.beta.threads.messages.create(
  thread_id=my_thread.id,
  role = "user",
  content = prompt,
  attachments = [{ "file_id": gpt_file, "tools": [{"type": "file_search"}]}]
)

# Run
my_run = client.beta.threads.runs.create(
    thread_id = my_thread.id,
    assistant_id = assistant,
    instructions="Return the final report and do not report as a file."
)

while my_run.status in ["queued", "in_progress"]:
    keep_retrieving_run = client.beta.threads.runs.retrieve(
        thread_id=my_thread.id,
        run_id=my_run.id
    )
    print(f"Run status: {keep_retrieving_run.status}")

    if keep_retrieving_run.status == "completed":
        print("\n")

        all_messages = client.beta.threads.messages.list(
            thread_id=my_thread.id
        )

        st.header('Output:', divider='green')

        #print(f"User: {my_thread_message.content[0].text.value}")
        # print(all_messages.data)
        output = []
        for txt in all_messages.data:
            if txt.role == 'assistant':
                output.append(txt.content[0].text.value)
                # st.markdown(body=txt.content[0].text.value)
                print(output)
                # print(txt.content[0].text.value)
        
        break
    elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
        pass
    else:
        print(f"Run status: {keep_retrieving_run.status}")
        st.write(f"Run status: {keep_retrieving_run.status}")
        break

# Delete file and agent
client.files.delete(gpt_file)
client.beta.assistants.delete(assistant)
client.beta.threads.delete(my_thread.id)

# Define styles
styles = getSampleStyleSheet()
normal_style = ParagraphStyle(
    name='Normal',
    fontSize=12,
    leading=14,
    spaceAfter=6,
    allowWidows=0,
    allowOrphans=0
)

# Function to replace \n with <br/> and bold text within **...**
def format_text(text):
    # Remove   patterns
    text = re.sub(r'【.*?†source】', '', text)
    # Replace **...** with <b>...</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Replace newlines with <br/> tags
    text = text.replace('\n', '<br/>')
    return text

# Create the document
buffer = BytesIO()

doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
elements = []

formatted_output = format_text(output[0])
paragraph = Paragraph(formatted_output, normal_style)
elements.append(paragraph)

# Build the PDF
doc.build(elements)


@st.experimental_fragment
def download_file():
    st.download_button(
            label="Download PDF",
            data=buffer,
            file_name="report.pdf",
            mime="application/pdf"
        )
download_file()

st.markdown(body=output[0])

st.stop() 