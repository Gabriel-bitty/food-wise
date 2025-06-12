import streamlit as st
import uuid
from components.homepage import render_homepage
from components.chat import render_chat_page

# --- Configuração da Página ---
st.set_page_config(
    page_title="Food Wise",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS to change the theme colors
custom_css = """
<style>
    /* Change the primary color for buttons and other elements */
    div[data-baseweb="button"] > button[kind="primary"] {
        background-color: #4A4A4A !important; /* Dark Grey */
        border-color: #4A4A4A !important; /* Dark Grey */
    }
    div[data-baseweb="button"] > button[kind="primary"]:hover {
        background-color: #303030 !important; /* Darker Grey for hover */
        border-color: #303030 !important; /* Darker Grey for hover */
    }
    div[data-baseweb="button"] > button[kind="primary"]:active {
        background-color: #202020 !important; /* Even Darker Grey for active/click */
        border-color: #202020 !important; /* Even Darker Grey for active/click */
    }

    /* Change the border color for selected tabs or active elements */
    /* This is a general selector, might need to be more specific for your tabs */
    .stTabs [data-baseweb="tab"][aria-selected="true"],
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #4A4A4A !important; /* Dark Grey */
        color: #4A4A4A !important; /* Dark Grey for text */
    }
    
    /* For radio buttons or similar selectable items in the sidebar */
    /* This targets the selected radio button's circle and label */
    div[data-testid="stSidebar"] div[role="radiogroup"] div[data-baseweb="radio"] label span[class*="RadioMark"] {
        background-color: white !important; /* Keep inner circle white */
        border-color: #4A4A4A !important; /* Dark Grey for the outer circle */
    }
    div[data-testid="stSidebar"] div[role="radiogroup"] div[data-baseweb="radio"][aria-checked="true"] label span[class*="RadioMarkInner"] {
        background-color: #4A4A4A !important; /* Dark Grey for the inner selected mark */
    }
    div[data-testid="stSidebar"] div[role="radiogroup"] div[data-baseweb="radio"]:hover label span[class*="RadioMark"] {
        border-color: #303030 !important; /* Darker Grey for hover on radio button */
    }

    /* Style for the buttons in the sidebar module selection */
    div[data-testid="stSidebar"] .stButton > button {
        border: 2px solid transparent !important; /* Default transparent border */
        transition: border-color 0.3s ease !important;
    }
    div[data-testid="stSidebar"] .stButton > button:hover {
        border-color: #4A4A4A !important; /* Dark Grey border on hover */
    }
    /* This is a bit tricky as Streamlit doesn't easily expose 'active' state for normal buttons in a group */
    /* We might need a more complex solution if this doesn't work as expected for the "selected" module button */
    /* If you have a specific class for the selected module button, that would be better */

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}
[data-testid="stDecoration"] {display:none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Inicializar session state
def initialize_session_state():
    st.session_state.setdefault('current_page', 'home')
    st.session_state.setdefault('user_logged_in', False)
    st.session_state.setdefault('current_user', None)
    
    if 'session_id' not in st.session_state or 'last_user' not in st.session_state:
        st.session_state['session_id'] = str(uuid.uuid4())
        st.session_state['last_user'] = None
    
    current_user = st.session_state.get('current_user')
    if current_user != st.session_state.get('last_user'):
        st.session_state['session_id'] = str(uuid.uuid4())
        st.session_state['last_user'] = current_user
        if 'memory_manager' in st.session_state:
            del st.session_state['memory_manager']
    
    # Módulo ativo
    st.session_state.setdefault('active_module', 'Logomarca')
    
    # Chat separado para cada módulo
    st.session_state.setdefault('module_chats', {
        'Fichas Técnicas': [],
        'Logomarca': [],
        'Mock-ups': []
    })
    
    # Estado para controlar efeito de digitação :D
    st.session_state.setdefault('typing_effect', {
        'active': False,
        'module': None,
        'message_index': -1,
        'char_index': 0,
        'full_text': '',
        'start_time': 0
    })

def main():

    initialize_session_state()
    
    if st.session_state.current_page == 'home':
        render_homepage()
    elif st.session_state.current_page == 'chat' and st.session_state.user_logged_in:
        render_chat_page()
    else:
        st.session_state.current_page = 'home'
        st.rerun()

if __name__ == "__main__":
    main()
