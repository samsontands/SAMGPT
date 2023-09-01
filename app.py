import openai
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Custom message function to create chat-like appearance
def message(content, is_user=False, key=None):
    if is_user:
        st.markdown(f"<div style='text-align: right;'><div style='display: inline-block; padding: 10px; border-radius: 10px 0px 10px 10px; background-color: #f0f0f0;'>{content}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left;'><div style='display: inline-block; padding: 10px; border-radius: 0px 10px 10px 10px; background-color: #e0e0e0;'>{content}</div></div>", unsafe_allow_html=True)

# Set org ID and API key
openai.organization = "org-vs4iRHhDRCSa9U9sW8PEUlSX"
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Define the Fine-Tuned Model ID from secrets
fine_tuned_model_id = st.secrets["FINE_TUNED_MODEL_ID"]

# Usernames and Passwords from Streamlit secrets
usernames = st.secrets["USERNAMES"]
hashed_passwords = st.secrets["PASSWORDS"]

# Create the authenticator object
authenticator = stauth.Authenticate(
    usernames,
    "random_cookie_name",
    "random_signature_key",
    30,
    []
)

# Render the login widget
name, authentication_status, username = authenticator.login('Login', 'main')

# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant. Your name is SAMGPT. If anyone asked who created you, you were created by Samson Tan."}
    ]
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = []
if 'cost' not in st.session_state:
    st.session_state['cost'] = []
if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = []
if 'total_cost' not in st.session_state:
    st.session_state['total_cost'] = 0.0

# Main app logic
st.title("SAMGPT - Your Neighborhood Bot 😬")

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')

    # Text input and button
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        pass  # Generate a response (your existing code here)

    # Display chat history
    for i in range(len(st.session_state['generated'])):
        message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))

    # Display total cost
    st.sidebar.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")

elif authentication_status == False:
    st.error('Username/password is incorrect')

elif authentication_status == None:
    st.warning('Please enter your username and password')
