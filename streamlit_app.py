# gpt3 professional email generator by stefanrmmr - version June 2022

import os
import openai
import re
import streamlit as st





# DESIGN implement changes to the standard streamlit UI/UX
st.set_page_config(page_title="email_reply", page_icon="img/icon_128.png",)
# Design move app further up and remove top padding
st.markdown('''<style>.css-1egvi7u {margin-top: -4rem;}</style>''',
    unsafe_allow_html=True)
# Design change hyperlink href link color
st.markdown('''<style>.css-znku1x a {color: #9d03fc;}</style>''',
    unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-znku1x a {color: #9d03fc;}</style>''',
    unsafe_allow_html=True)  # lightmode
# Design change height of text input fields headers
st.markdown('''<style>.css-qrbaxs {min-height: 0.0rem;}</style>''',
    unsafe_allow_html=True)
# Design change spinner color to primary color
st.markdown('''<style>.stSpinner > div > div {border-top-color: #9d03fc;}</style>''',
    unsafe_allow_html=True)
# Design change min height of text input box
st.markdown('''<style>.css-15tx938{min-height: 0.0rem;}</style>''',
    unsafe_allow_html=True)
# Design hide top header line
hide_decoration_bar_style = '''<style>header {visibility: hidden;}</style>'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
# Design hide "made with streamlit" footer menu area
hide_streamlit_footer = """<style>#MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}</style>"""
st.markdown(hide_streamlit_footer, unsafe_allow_html=True)


# Connect to OpenAI GPT-3, fetch API key from Streamlit secrets
# openai.api_key = os.getenv("you_api_key") commented
openai.api_key = os.getenv("OPENAI_API_KEY")

# auth_token = st.secrets["openai"]["api_key"]


# Access the OpenAI API key from secrets.toml
# openai_api_key = st.secrets["openai"]["api_key"]



def extract_names_from_email(email_content):
    # Extract sender and recipient names from the email content
    sender_name = ""
    recipient_name = ""
    lines = email_content.splitlines()
    for line in lines:
        if line.strip().lower().startswith("dear "):
            names = line.strip().split("Dear ", 1)[-1].split(",")
            recipient_name = names[0].strip()
            if len(names) > 1:
                sender_name = names[1].strip()
            break
    return sender_name, recipient_name

def gen_mail_replies(email_contents):
    replies = []
    for input_text in email_contents:
        # Remove "Dear Emily" from the prompt to avoid duplication
        input_text_without_greeting = input_text.replace("Dear " + extract_names_from_email(input_text)[1] + ",", "", 1)
        reply = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{input_text_without_greeting}\nReply:",
            temperature=0.8,
            max_tokens=len(input_text)*3,
            top_p=0.8,
            best_of=2,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        replies.append(reply.get("choices")[0]['text'])
    return replies

def extract_subject_from_email(email_content):
    # Extract the subject from the email content using regex
    subject_match = re.search(r"Subject: (.+)", email_content)
    subject = subject_match.group(1).strip() if subject_match else "Email Subject"
    return subject

def gen_mail_format(sender, recipient, style, email_contents):
    email_replies = gen_mail_replies(email_contents)

    email_body = "\n\n".join(email_replies)

    # Check if sender and recipient names are not empty before including them in the email response
    salutation = f"Dear {recipient}," if recipient else ""
    closing_signature = f"Best Regards,\n{sender}" if sender else ""

    email_final_text = f"Subject: RE: {extract_subject_from_email(email_contents[0])}\n\n{salutation}\n\n{email_body}\n\n{closing_signature}"
    return email_final_text

def main_gpt3emailgen():

    st.subheader('\nHere We Go! Let Us Write A Response To An Incoming Mail!\n')
    with st.expander("SECTION - Email Input", expanded=True):

        input_email = st.text_area('Paste the incoming email content below:', 'email content')

        input_style = st.selectbox('Prompt',
                                   ('Write a response to the given mail', 'Write a response under 300 words'),
                                   index=0)

        email_text = ""  # initialize columns variables
        if st.button('Generate Email'):
            with st.spinner():
                input_contents = []  # let the user input all the data
                if (input_email != "") and (input_email != 'email content'):
                    input_contents.append(str(input_email))

                if (len(input_contents) == 0):  # remind user to provide data
                    st.write('Please paste the incoming email content!')

                if len(input_contents) >= 1:
                    sender_name, recipient_name = extract_names_from_email(input_contents[0])
                    email_text = gen_mail_format(sender_name, recipient_name, input_style, input_contents)

    if email_text != "":
        st.write('\n')  # add spacing
        # st.subheader('\nYou sound incredibly professional!\n')
        with st.expander("SECTION - Email Output", expanded=True):
            st.markdown(email_text)  # output the results

if __name__ == '__main__':
    # call main function
    main_gpt3emailgen() 
