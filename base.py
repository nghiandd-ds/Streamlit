import streamlit as st
from openai import OpenAI
from io import BytesIO
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph

def request_gpt(input_file, prompt, output_filename):
    # Connect to Openai API
    a = 'sk-proj-50i25Vf5uMtQ8EpYF'
    b = 'AyaT3BlbkFJ2B9b6oBxsJpx058Zxocv'
    client = OpenAI(api_key=a+b)

    # Upload file to OpenAI and take ID
    gpt_file = client.files.create(
        file=input_file,
        purpose='assistants').id

    assistant = client.beta.assistants.create(
        # model="gpt-3.5-turbo-0125",
        model="gpt-4o-mini-2024-07-18",
        instructions="You are a researcher",
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
            # output = []
            for txt in all_messages.data:
                if txt.role == 'assistant':
                    # output.append(txt.content[0].text.value)
                    # st.markdown(body=txt.content[0].text.value)
                    output = txt.content[0].text.value

                    # Remove patterns
                    output = re.sub(r'【.*?†source】', '', output)
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

    formatted_output = format_text(output)
    paragraph = Paragraph(formatted_output, normal_style)
    elements.append(paragraph)

    # Build the PDF
    doc.build(elements)


    @st.experimental_fragment
    def download_file():
        st.download_button(
                label="Download PDF",
                data=buffer,
                file_name=f"{output_filename}.pdf",
                mime="application/pdf"
            )
    download_file()

    st.markdown(body=output)

    st.stop() 
