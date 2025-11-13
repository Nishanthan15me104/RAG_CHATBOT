import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"

# --- PAGE CONFIG ---
st.set_page_config(page_title="Philosophical Agent", layout="centered")
st.title("Philosophical Agent")

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_philosopher_id" not in st.session_state:
    st.session_state.selected_philosopher_id = "socrates"
if "philosophers" not in st.session_state:
    st.session_state.philosophers = {}

# --- FETCH PHILOSOPHERS ---
@st.cache_data(show_spinner="Loading philosophers...")
def get_philosopher_list():
    try:
        response = requests.get(f"{API_BASE_URL}/philosophers")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching philosophers: {e}")
        return {}

st.session_state.philosophers = get_philosopher_list()

# --- SIDEBAR ---
st.sidebar.title("Select a Philosopher")

if st.session_state.philosophers:
    philosopher_names = list(st.session_state.philosophers.values())
    philosopher_ids = list(st.session_state.philosophers.keys())

    try:
        current_index = philosopher_ids.index(st.session_state.selected_philosopher_id)
    except ValueError:
        current_index = 0

    selected_philosopher_name = st.sidebar.selectbox(
        "Choose your conversational partner:",
        options=philosopher_names,
        index=current_index
    )

    selected_philosopher_id = next(
        (key for key, value in st.session_state.philosophers.items()
         if value == selected_philosopher_name),
        "socrates"
    )
else:
    st.sidebar.error("No philosophers available. Is FastAPI running?")
    selected_philosopher_id = "socrates"

# Store the selected philosopher
st.session_state.selected_philosopher_id = selected_philosopher_id

# Reset conversation
if st.sidebar.button("Reset Conversation"):
    try:
        requests.post(f"{API_BASE_URL}/reset-memory")
        st.session_state.messages = []
        st.experimental_rerun() # Use experimental_rerun to clear the page immediately
        st.sidebar.success("Conversation reset!")
    except Exception:
        st.sidebar.error("Could not reset conversation (backend down?)")

# --- CHAT DISPLAY ---
# This loop correctly displays the messages using Streamlit's chat_message block
st.write("### Conversation")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- USER INPUT ---
if prompt := st.chat_input("Ask something..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display the user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # Placeholder for streaming the response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

    # Get AI response
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={
                "message": prompt,
                "philosopher_id": st.session_state.selected_philosopher_id
            }
        )
        response.raise_for_status()
        
        # We assume the backend returns the full response text
        full_response = response.json().get("response", "No response from API.")
        
        # Display the full response
        message_placeholder.markdown(full_response)
        
    except Exception as e:
        full_response = f"Error contacting backend: {e}"
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- DEBUG INFO ---
# I'm commenting out these lines so the raw data does not clutter your display.
# If you need them later, uncomment them!
# st.write("DEBUG: Philosophers →", st.session_state.philosophers)
# st.write("DEBUG: Selected Philosopher ID →", st.session_state.selected_philosopher_id)
# st.write("DEBUG: Messages so far →", st.session_state.messages)
