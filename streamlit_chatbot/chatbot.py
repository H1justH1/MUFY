import streamlit as st
import google.generativeai as genai
import pandas as pd

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyCPCiG6rbVyMFFUZsRYzwjKZH9Cy5JjdKI"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def get_gemini_response(prompt):
    response = model.generate_content(prompt)
    return response.text

def main():
    st.title("Gemini AI Chatbot")

    initialize_session_state()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Chat with Gemini"):
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get Gemini response
        response = get_gemini_response(prompt)

        # Display assistant response
        with st.chat_message("assistant"):
            st.write(response)

        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()

# Sample data
data = {
    "Month": ["January", "February", "March", "April"],
    "Price": [500, 1500, 2200, 800]
}
df = pd.DataFrame(data)

# Sidebar Filters
st.sidebar.header("Filters")

selected_month = st.sidebar.selectbox(
    "Select Month",
    options=df['Month'].unique()
)

price_range = st.sidebar.slider(
    "Select Price Range",
    min_value=0,
    max_value=3000,
    value=(0, 3000)
)

# --- Sidebar Controls ---
st.sidebar.title("⚙️ Settings")

# Dark mode toggle (this doesn't change the theme directly, but we can simulate it)
dark_mode = st.sidebar.toggle("🌙 Dark Mode")

# File upload
uploaded_file = st.sidebar.file_uploader("📁 Upload a file", type=["csv", "txt", "xlsx"])

# Display uploaded file content (optional)
if uploaded_file:
    st.sidebar.success("File uploaded successfully!")
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        st.sidebar.dataframe(df.head())
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
        st.sidebar.dataframe(df.head())
    elif uploaded_file.name.endswith('.txt'):
        content = uploaded_file.read().decode("utf-8")
        st.sidebar.text_area("Text file content", content, height=150)

# Apply background color (simulated dark mode)
if dark_mode:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #1e1e1e;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )