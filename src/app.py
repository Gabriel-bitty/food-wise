import streamlit as st

# Import pages
from pages.homepage import render_homepage
from pages.chat import render_chat_page
from pages.styles import apply_dark_theme

# --- Configuração da Página ---
st.set_page_config(
    page_title="Food Wise",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Inicializar session state
def initialize_session_state():
    # Navigation state
    st.session_state.setdefault('current_page', 'home')
    st.session_state.setdefault('user_logged_in', False)
    st.session_state.setdefault('current_user', None)
    
    # Módulo ativo
    st.session_state.setdefault('active_module', 'Logomarca')
    
    # Chat separado para cada módulo
    st.session_state.setdefault('module_chats', {
        'Fichas Técnicas': [],
        'Logomarca': [],
        'Mock-ups': []
    })
    
    # Estado para controlar efeito de digitação
    st.session_state.setdefault('typing_effect', {
        'active': False,
        'module': None,
        'message_index': -1,
        'char_index': 0,
        'full_text': '',
        'start_time': 0
    })

# --- Main App Logic ---
def main():
    # Apply dark theme
    apply_dark_theme()
    
    # Initialize session state
    initialize_session_state()
    
    # Route to appropriate page
    if st.session_state.current_page == 'home':
        render_homepage()
    elif st.session_state.current_page == 'chat' and st.session_state.user_logged_in:
        render_chat_page()
    else:
        # If trying to access chat without login, redirect to home
        st.session_state.current_page = 'home'
        st.rerun()

if __name__ == "__main__":
    main()
