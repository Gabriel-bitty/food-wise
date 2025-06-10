import streamlit as st

def apply_dark_theme():
    """Apply clean dark theme CSS to the app"""
    st.markdown("""
    <style>
    /* Reset and Base Dark Theme */
    .stApp {
        background-color: #0E1117 !important;
        color: #FAFAFA !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        background-color: #0E1117 !important;
        color: #FAFAFA !important;
    }

    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stHeader"] {display: none !important;}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #262730 !important;
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: #FAFAFA !important;
    }

    /* Text Elements */
    h1, h2, h3, h4, h5, h6 {
        color: #FAFAFA !important;
    }

    .stMarkdown p {
        color: #FAFAFA !important;
    }

    /* Chat Input */
    [data-testid="stChatInput"] {
        background-color: #262730 !important;
        border: 1px solid #404040 !important;
        border-radius: 12px !important;
        padding: 4px !important;
    }

    [data-testid="stChatInput"] textarea {
        background-color: #262730 !important;
        color: #FAFAFA !important;
        border: none !important;
        font-size: 16px !important;
        padding: 12px !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #888888 !important;
        opacity: 1 !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: none !important;
        outline: none !important;
        box-shadow: 0 0 0 2px #FF4B4B !important;
    }

    [data-testid="stChatInput"] button {
        background-color: #FF4B4B !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
    }

    [data-testid="stChatInput"] button:hover {
        background-color: #FF6B6B !important;
    }

    /* Chat Messages */
    [data-testid="stChatMessage"] {
        background-color: #1E1E1E !important;
        border-left: 4px solid #FF4B4B !important;
        color: #FAFAFA !important;
        margin-bottom: 1rem !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }

    /* Regular Buttons */
    .stButton > button {
        background-color: #1E1E1E !important;
        color: #FAFAFA !important;
        border: 1px solid #404040 !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background-color: #2A2B2D !important;
        border-color: #FF4B4B !important;
        color: #FFFFFF !important;
    }

    /* Primary Buttons */
    .stButton > button[kind="primary"] {
        background-color: #FF4B4B !important;
        color: white !important;
        border-color: #FF4B4B !important;
        font-weight: 600 !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #FF6B6B !important;
        border-color: #FF6B6B !important;
    }

    /* Form Submit Buttons */
    .stForm button[kind="primary"],
    .stForm button[type="submit"],
    .stFormSubmitButton > button {
        background-color: #FF4B4B !important;
        color: white !important;
        border: 1px solid #FF4B4B !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
    }

    .stForm button[kind="primary"]:hover,
    .stForm button[type="submit"]:hover,
    .stFormSubmitButton > button:hover {
        background-color: #FF6B6B !important;
        border-color: #FF6B6B !important;
        color: white !important;
    }

    /* Text Inputs */
    .stTextInput > div > div > input {
        background-color: #1E1E1E !important;
        color: #FAFAFA !important;
        border: 1px solid #404040 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #FF4B4B !important;
        box-shadow: 0 0 0 1px #FF4B4B !important;
        outline: none !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #888888 !important;
    }

    /* Password Inputs */
    .stTextInput > div > div > input[type="password"] {
        background-color: #1E1E1E !important;
        color: #FAFAFA !important;
        border: 1px solid #404040 !important;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: transparent !important;
        border-bottom: 1px solid #404040 !important;
        margin-bottom: 1rem !important;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #1E1E1E !important;
        color: #FAFAFA !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 0.75rem 1.5rem !important;
        border: 1px solid #404040 !important;
        border-bottom: none !important;
        font-weight: 500 !important;
        margin-bottom: 0 !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2A2B2D !important;
        color: #FFFFFF !important;
        border-color: #FF4B4B !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #FF4B4B !important;
        color: white !important;
        border-color: #FF4B4B !important;
        font-weight: 600 !important;
    }

    /* Tab Content */
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #262730 !important;
        border-radius: 0 8px 8px 8px !important;
        border: 1px solid #404040 !important;
        padding: 1.5rem !important;
        margin-top: -1px !important;
    }

    /* Form Container */
    .stForm {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    .stForm > div {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        gap: 1rem !important;
    }

    /* Success/Error Messages */
    .stAlert {
        background-color: #1E1E1E !important;
        border-radius: 8px !important;
        border: 1px solid #404040 !important;
        color: #FAFAFA !important;
    }

    /* Success Alert */
    .stAlert[data-baseweb="notification"][kind="success"] {
        background-color: #1B5E20 !important;
        border-color: #4CAF50 !important;
    }

    /* Error Alert */
    .stAlert[data-baseweb="notification"][kind="error"] {
        background-color: #B71C1C !important;
        border-color: #F44336 !important;
    }

    /* Remove extra containers and margins */
    .element-container {
        margin-bottom: 1rem !important;
    }

    .stContainer > div {
        background-color: transparent !important;
        padding: 0 !important;
    }

    /* Labels */
    .stTextInput > label,
    .stSelectbox > label {
        color: #FAFAFA !important;
        font-weight: 500 !important;
        margin-bottom: 0.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)