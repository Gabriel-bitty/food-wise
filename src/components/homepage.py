import streamlit as st
import time
import requests

def create_client(name, passkey):
    try:
        response = requests.post('http://localhost:3000/api/clients', 
                               json={'name': name, 'passkey': passkey})
        if response.status_code == 201:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": response.json().get('error', 'Unknown error')}
    except Exception as e:
        return {"success": False, "error": f"Backend connection error: {str(e)}"}

def verify_client(name, passkey):
    try:
        response = requests.get('http://localhost:3000/api/clients')
        if response.status_code == 200:
            clients = response.json()
            for client in clients:
                if client['name'] == name:
                    return {"success": True, "client": client}
            return {"success": False, "error": "Client not found"}
        else:
            return {"success": False, "error": "Backend error"}
    except Exception as e:
        return {"success": False, "error": f"Backend connection error: {str(e)}"}

def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

def render_homepage():
    # Mostrar status de login se logado
    if st.session_state.get('user_logged_in', False):
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.success(f"✅ Logado como: {st.session_state.current_user}")
                if st.button("🍽️ Ir para Chat", use_container_width=True, type="primary"):
                    st.session_state.current_page = 'chat'
                    st.rerun()
                st.markdown("---")
    
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">🍽️ Food Wise</h1>
        <p class="hero-subtitle">Sua ferramenta de IA para criação e gestão de conteúdo alimentar</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### ✨ Recursos")
        
        st.markdown("""
        <div class="feature-card">
            <h4>📋 Fichas Técnicas</h4>
            <p>Crie fichas técnicas detalhadas com informações nutricionais, ingredientes e modo de preparo.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>🎨 Logomarca</h4>
            <p>Desenvolva conceitos de design para sua marca alimentar com sugestões personalizadas.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>📱 Mock-ups</h4>
            <p>Crie propostas visuais e materiais promocionais para seus produtos.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🔐 Acesso")
        
        tab1, tab2 = st.tabs(["Login", "Cadastro"])
        
        with tab1:
            with st.form("login_form", clear_on_submit=False):
                st.markdown("**Entre com sua conta**")
                login_name = st.text_input("Nome de usuário", key="login_name", placeholder="Digite seu nome de usuário")
                login_passkey = st.text_input("Chave de acesso", type="password", key="login_passkey", placeholder="Digite sua chave de acesso")
                login_submit = st.form_submit_button("Entrar", use_container_width=True, type="primary")
                
                if login_submit:
                    if login_name and login_passkey:
                        result = verify_client(login_name, login_passkey)
                        if result["success"]:
                            st.session_state.user_logged_in = True
                            st.session_state.current_user = login_name
                            st.success(f"Bem-vindo, {login_name}!")
                            time.sleep(1)
                            navigate_to('chat')
                        else:
                            st.error("Usuário não encontrado. Tente fazer cadastro primeiro.")
                    else:
                        st.error("Por favor, preencha todos os campos.")
        
        with tab2:
            with st.form("signup_form", clear_on_submit=False):
                st.markdown("**Crie sua conta**")
                signup_name = st.text_input("Nome de usuário", key="signup_name", placeholder="Escolha um nome de usuário")
                signup_passkey = st.text_input("Chave de acesso", type="password", key="signup_passkey", placeholder="Crie uma chave de acesso")
                signup_passkey_confirm = st.text_input("Confirme a chave", type="password", key="signup_passkey_confirm", placeholder="Confirme sua chave de acesso")
                signup_submit = st.form_submit_button("Cadastrar", use_container_width=True, type="primary")
                
                if signup_submit:
                    if signup_name and signup_passkey and signup_passkey_confirm:
                        if signup_passkey == signup_passkey_confirm:
                            result = create_client(signup_name, signup_passkey)
                            if result["success"]:
                                st.success("Conta criada com sucesso! Faça login para continuar.")
                            else:
                                if "duplicate" in result["error"].lower() or "unique" in result["error"].lower():
                                    st.error("Este nome de usuário já existe. Escolha outro.")
                                else:
                                    st.error(f"Erro ao criar conta: {result['error']}")
                        else:
                            st.error("As chaves de acesso não coincidem.")
                    else:
                        st.error("Por favor, preencha todos os campos.")
    
    st.markdown("---")
    st.markdown("### 📖 Sobre o Projeto")
    
    about_col1, about_col2 = st.columns([2, 1])
    
    with about_col1:
        st.markdown("""
        **Food Wise** é uma plataforma inovadora que utiliza inteligência artificial para auxiliar 
        profissionais e empresas do setor alimentício na criação de conteúdo técnico e promocional.
        
        #### Funcionalidades Principais:
        - **Geração Inteligente**: IA especializada em conteúdo alimentar
        - **Multi-módulos**: Três áreas especializadas de atuação
        - **Interface Intuitiva**: Design moderno e fácil de usar
        - **Persistência de Dados**: Seus chats são salvos automaticamente
        """)
    
    with about_col2:
        st.markdown("""
        #### 📊 Estatísticas
        - **Versão**: 0.1 (Protótipo)
        - **Módulos**: 3 especializados
        - **Status**: Em desenvolvimento
        
        #### 🎯 Objetivos
        - Automatizar criação de fichas técnicas
        - Auxiliar no desenvolvimento de marca
        - Facilitar criação de materiais promocionais
        """)