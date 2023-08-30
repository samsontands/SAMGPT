import openai
import streamlit as st

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

# Sidebar - let user choose model
model_name = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4", "Fine-Tuned Model"))

# Map model names to OpenAI model IDs
if model_name == "GPT-3.5":
    model = "gpt-3.5-turbo"
elif model_name == "GPT-4":
    model = "gpt-4"
else:
    model = fine_tuned_model_id

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

# Generate a response
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(
        model=model,
        messages=st.session_state['messages']
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})
    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens

# Main app logic
st.title("SAMGPT - Your Neighborhood Bot 😬")

# Text input and button
with st.form(key='my_form', clear_on_submit=True):
    user_input = st.text_area("You:", key='input', height=100)
    submit_button = st.form_submit_button(label='Send')

if submit_button and user_input:
    output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)
    st.session_state['model_name'].append(model_name)
    st.session_state['total_tokens'].append(total_tokens)

    # Calculate cost
    if model_name == "GPT-3.5":
        cost = total_tokens * 0.002 / 1000
    else:
        cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000

    st.session_state['cost'].append(cost)
    st.session_state['total_cost'] += cost

# Display chat history
for i in range(len(st.session_state['generated'])):
    message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
    message(st.session_state["generated"][i], key=str(i))
    st.write(f"Model used: {st.session_state['model_name'][i]}; Number of tokens: {st.session_state['total_tokens'][i]}; Cost: ${st.session_state['cost'][i]:.5f}")

# Display total cost
st.sidebar.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
