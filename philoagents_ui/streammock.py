import streamlit as st
import requests
import asyncio


# The base URL for your FastAPI server
# This URL is used to send requests to the API running on your local machine.
API_BASE_URL = "http://localhost:8000"

# --- MOCK DATA FOR TESTING WITHOUT THE BACKEND ---
# This dictionary simulates the response from the API's /philosophers endpoint.
MOCK_PHILOSOPHER_NAMES = {
    "socrates": "Socrates",
    "plato": "Plato",
    "aristotle": "Aristotle",
    "descartes": "Rene Descartes",
    "leibniz": "Gottfried Wilhelm Leibniz",
    "ada_lovelace": "Ada Lovelace",
    "turing": "Alan Turing",
    "chomsky": "Noam Chomsky",
    "searle": "John Searle",
    "dennett": "Daniel Dennett",
}


# --- SET UP PAGE ---
st.set_page_config(page_title="Philosophical Agent", layout="centered")
st.title("Philosophical Agent")

st.sidebar.title("Select a Philosopher")

# --- INITIALIZE SESSION STATE ---
# The session state stores information across user interactions,
# so the app remembers the conversation history and selections.
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_philosopher_id" not in st.session_state:
    st.session_state.selected_philosopher_id = "socrates"
if "philosophers" not in st.session_state:
    st.session_state.philosophers = {}


# --- FETCH PHILOSOPHER LIST (MOCK VERSION) ---
# This mock function bypasses the API call for frontend-only testing.
@st.cache_data(show_spinner="Loading philosophers...")
def get_philosopher_list():
    # Return the mock data instead of trying to connect to the server
    return MOCK_PHILOSOPHER_NAMES


philosophers = get_philosopher_list()
st.session_state.philosophers = philosophers

# --- UI COMPONENTS ---
philosopher_names = list(st.session_state.philosophers.values())
philosopher_ids = list(st.session_state.philosophers.keys())

# A selectbox allows the user to choose a philosopher from the list
try:
    current_index = philosopher_ids.index(st.session_state.selected_philosopher_id)
except ValueError:
    current_index = 0

selected_philosopher_name = st.sidebar.selectbox(
    "Choose your conversational partner:",
    options=philosopher_names,
    index=current_index
)

# Reverse lookup the ID from the selected name
selected_philosopher_id = next(
    (key for key, value in st.session_state.philosophers.items() if value == selected_philosopher_name),
    "socrates"
)

# Reset conversation and rerun app if a new philosopher is selected
if st.session_state.selected_philosopher_id != selected_philosopher_id:
    st.session_state.selected_philosopher_id = selected_philosopher_id
    st.session_state.messages = []
    st.experimental_rerun()

# A "Reset Conversation" button to clear the chat history
# Note: This button will only clear the UI, not reset the backend's memory.
if st.sidebar.button("Reset Conversation"):
    st.session_state.messages = []
    st.sidebar.success("Conversation reset successfully!")
    st.experimental_rerun()

# --- DISPLAY CHAT MESSAGES ---
# This loop displays all messages currently stored in the session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- HANDLE USER INPUT (MODIFIED FOR OLDER VERSIONS) ---
# This part replaces st.chat_input
# Using a form to submit the text input
with st.form(key='my_form', clear_on_submit=True):
    prompt = st.text_input("What is your question?", key="input_text")
    submit_button = st.form_submit_button(label='Send')

if submit_button and prompt:
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and display a mock AI response
    with st.spinner("Thinking..."):
        full_response = f"This is a mock response from {selected_philosopher_name}. You asked: '{prompt}'"
    
    with st.chat_message("assistant"):
        st.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

st.write("Hello, Streamlit is working!")