import streamlit as st
from openai import OpenAI
import numpy as np
import pandas as pd
import os

st.set_page_config(
    page_title="AI Summary", 
    page_icon="🤖",
)

st.write("# Summarization Tool 📄")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")


if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()
    
# upload file by streamlit
uploaded_file = st.file_uploader("Upload file")


if not uploaded_file:
    st.stop()    
    
# Connect to Openai API
client = OpenAI(api_key=openai_api_key)

# Upload file to OpenAI and take ID
gpt_file = client.files.create(
    file=uploaded_file,
    purpose='assistants').id

# Create agent
# Coder = client.beta.assistants.create(
#   name="Check code Assistant",
#   instructions="You are an expert in coding and specialize in python and relevent packages. \
#                 Your job is to read and understand codes of junior-level employees and then, explain it briefly and correctly to \
#                 manager who is trained as a data scientist but not specialized in coding",
#   model="gpt-3.5-turbo-0125", tools=[{"type": "code_interpreter"}]).id


assistant = client.beta.assistants.create(
    model="gpt-3.5-turbo-0125",
    instructions="You are a bank employee who works in the Risk Management department. \
                  Your job is to read and understand the attached document and summarize it for your manager.",
    name="Summary Assistant",
    tools=[{"type": "file_search"}]
).id


# ChatGPT promt
promt = """Provide a summary of the article."""
# Create thread
my_thread = client.beta.threads.create()

# add message
my_thread_message = client.beta.threads.messages.create(
  thread_id=my_thread.id,
  role = "user",
  content = promt,
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
        for txt in all_messages.data:
            if txt.role == 'assistant':
                st.markdown(body=txt.content[0].text.value)
                print(txt.content[0].text.value)
        break
    elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
        pass
    else:
        print(f"Run status: {keep_retrieving_run.status}")
        break
# Delete file and agent
client.files.delete(gpt_file)
client.beta.assistants.delete(assistant)
client.beta.threads.delete(my_thread.id)
