import streamlit as st
import uuid
from components.homepage import render_homepage
from components.chat import render_chat_page
from components.styles import apply_dark_theme

# --- Configuração da Página ---
st.set_page_config(
    page_title="Food Wise",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

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
    apply_dark_theme()
    
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
