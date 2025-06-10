import streamlit as st

def apply_dark_theme():
    """Apply dark theme CSS to the app"""
    st.markdown("""
    <style>
    /* Tema Escuro Permanente */
    .stApp {
        background-color: #0E1117 !important;
        color: #FAFAFA !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        background-color: #0E1117 !important;
        color: #FAFAFA !important;
    }

    [data-testid="stSidebar"] {
        background-color: #262730 !important;
    }

    /* Texto da sidebar */
    [data-testid="stSidebar"] .stMarkdown {
        color: #FAFAFA !important;
    }

    /* Botões da sidebar */
    [data-testid="stButton"] button {
        background-color: #1E1E1E !important;
        color: #FAFAFA !important;
        border: 1px solid #3A3B3C !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        margin-bottom: 0.5rem !important;
        transition: all 0.2s ease !important;
        font-weight: 500 !important;
    }

    [data-testid="stButton"] button:hover {
        background-color: #2A2B2D !important;
        border-color: #4A4B4D !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
    }

    [data-testid="stButton"] button[kind="primary"] {
        background-color: #FF4B4B !important;
        color: white !important;
        border-color: #FF4B4B !important;
        font-weight: 600 !important;
    }

    [data-testid="stButton"] button[kind="primary"]:hover {
        background-color: #FF6B6B !important;
        border-color: #FF6B6B !important;
    }

    /* Chat messages modo escuro */
    [data-testid="stChatMessage"] {
        background-color: #1E1E1E !important;
        border-left-color: #FF4B4B !important;
        color: #FAFAFA !important;
    }

    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: #1A237E !important;
        border-left-color: #3F51B5 !important;
    }

    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background-color: #1B5E20 !important;
        border-left-color: #4CAF50 !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #FAFAFA !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #888888 !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #FAFAFA !important;
    }

    .stMarkdown p {
        color: #FAFAFA !important;
    }

    /* Tab styling */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 8px;
    }

    [data-testid="stTabs"] [data-baseweb="tab"] {
        background-color: #1E1E1E !important;
        color: #FAFAFA !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        border: 1px solid #3A3B3C !important;
    }

    [data-testid="stTabs"] [aria-selected="true"] {
        background-color: #FF4B4B !important;
        color: white !important;
        border-color: #FF4B4B !important;
    }

    /* Form styling */
    [data-testid="stForm"] {
        background-color: transparent !important;
        border: none !important;
    }

    /* Input styling */
    .stTextInput input {
        background-color: #1E1E1E !important;
        color: #FAFAFA !important;
        border: 1px solid #3A3B3C !important;
        border-radius: 6px !important;
    }

    .stTextInput input:focus {
        border-color: #FF4B4B !important;
        box-shadow: 0 0 0 1px #FF4B4B !important;
    }
    </style>
    """, unsafe_allow_html=True)