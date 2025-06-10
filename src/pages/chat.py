import streamlit as st
import time
import requests

def save_message_to_backend(module, role, content):
    """Save chat message to backend"""
    try:
        # Convert module names to backend format
        module_mapping = {
            'Fichas Técnicas': 'fichasTecnicas',
            'Logomarca': 'logomarca',
            'Mock-ups': 'mockups'
        }
        backend_module = module_mapping.get(module, module.lower())
        
        response = requests.post(f'http://localhost:3000/api/chat/{backend_module}/messages', 
                               json={'role': role, 'content': content})
        return response.status_code == 201
    except Exception as e:
        print(f"Error saving message: {e}")
        return False

def load_messages_from_backend(module):
    """Load chat messages from backend"""
    try:
        # Convert module names to backend format
        module_mapping = {
            'Fichas Técnicas': 'fichasTecnicas',
            'Logomarca': 'logomarca',
            'Mock-ups': 'mockups'
        }
        backend_module = module_mapping.get(module, module.lower())
        
        response = requests.get(f'http://localhost:3000/api/chat/{backend_module}/messages')
        if response.status_code == 200:
            backend_messages = response.json()
            # Convert to frontend format
            return [{"role": msg["role"], "content": msg["content"]} for msg in backend_messages]
        return []
    except Exception as e:
        print(f"Error loading messages: {e}")
        return []

def generate_ai_response(prompt, module_name):
    """Gera resposta completa da IA baseada no módulo"""
    responses = {
        'Fichas Técnicas': f"📋 **Fichas Técnicas**: Posso ajudar você a criar fichas técnicas detalhadas para '{prompt}'. Incluo informações nutricionais, ingredientes, modo de preparo e especificações técnicas completas.",
        
        'Logomarca': f"🎨 **Logomarca**: Para '{prompt}', posso sugerir conceitos de design que reflitam a identidade da sua marca alimentar.",
        
        'Mock-ups': f"📱 **Mock-ups**: Vou criar propostas visuais para '{prompt}', incluindo diversos materiais promocionais."
    }
    
    return responses.get(module_name, f"Resposta para '{prompt}' no módulo {module_name}")

def switch_module(module_name):
    if module_name != st.session_state.active_module:
        st.session_state.active_module = module_name
        # Load messages from backend when switching modules
        backend_messages = load_messages_from_backend(module_name)
        st.session_state.module_chats[module_name] = backend_messages
        # Parar qualquer efeito de digitação ativo
        st.session_state.typing_effect['active'] = False
        st.rerun()

def clear_current_chat():
    current_module = st.session_state.active_module
    st.session_state.module_chats[current_module] = []
    # Also clear from backend
    try:
        module_mapping = {
            'Fichas Técnicas': 'fichasTecnicas',
            'Logomarca': 'logomarca',
            'Mock-ups': 'mockups'
        }
        backend_module = module_mapping.get(current_module, current_module.lower())
        requests.delete(f'http://localhost:3000/api/chat/{backend_module}/messages')
    except:
        pass
    
    # Parar efeito de digitação se estiver ativo no módulo atual
    if st.session_state.typing_effect['module'] == current_module:
        st.session_state.typing_effect['active'] = False
    st.rerun()

def clear_all_chats():
    st.session_state.module_chats = {
        'Fichas Técnicas': [],
        'Logomarca': [],
        'Mock-ups': []
    }
    # Also clear from backend
    try:
        requests.delete('http://localhost:3000/api/chat/messages')
    except:
        pass
    
    # Parar qualquer efeito de digitação
    st.session_state.typing_effect['active'] = False
    st.rerun()

def get_current_messages():
    current_module = st.session_state.active_module
    return st.session_state.module_chats.get(current_module, [])

def add_message_to_current(role, content):
    current_module = st.session_state.active_module
    st.session_state.module_chats[current_module].append({
        "role": role, 
        "content": content
    })
    # Save to backend
    save_message_to_backend(current_module, role, content)

def start_typing_effect(full_response, module_name, message_index):
    st.session_state.typing_effect.update({
        'active': True,
        'module': module_name,
        'message_index': message_index,
        'char_index': 0,
        'full_text': full_response,
        'start_time': time.time()
    })

def logout():
    st.session_state.user_logged_in = False
    st.session_state.current_user = None
    st.session_state.current_page = 'home'
    # Clear chat data on logout
    st.session_state.module_chats = {
        'Fichas Técnicas': [],
        'Logomarca': [],
        'Mock-ups': []
    }
    st.rerun()

def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

def render_chat_page():
    """Render the AI chat page"""
    
    # Sidebar with modules
    with st.sidebar:
        st.markdown(f"## 👋 Olá, {st.session_state.current_user}")
        st.markdown("*Food Wise v0.1*")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            logout()
        
        st.markdown("---")
        st.markdown("### Selecione um módulo:")
        
        modules_config = [
            ('📋', 'Fichas Técnicas'),
            ('🎨', 'Logomarca'),
            ('📱', 'Mock-ups')
        ]
        
        # Módulos como botões clicáveis na sidebar
        for icon, module_name in modules_config:
            is_active = st.session_state.active_module == module_name
            
            # Criar label do botão
            button_label = f"{icon} {module_name}"
            
            # Criar botão
            if st.button(
                button_label,
                key=f"module_btn_{module_name}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                switch_module(module_name)
        
        st.markdown("---")
        st.markdown("### Configurações")
        
        # Botão limpar chat atual
        if st.button("🗑️ Limpar Atual", use_container_width=True):
            clear_current_chat()
        
        # Botão limpar todos os chats
        if st.button("🗑️ Limpar Todos", use_container_width=True):
            clear_all_chats()
        
        # Voltar para home
        if st.button("🏠 Início", use_container_width=True):
            navigate_to('home')
    
    # Main chat area
    st.title("🍽️ Food Wise - Chat IA")
    st.markdown(f"**Módulo Ativo:** {st.session_state.active_module}")
    
    # Container principal para o chat
    chat_container = st.container()
    
    with chat_container:
        # Load messages from backend when entering chat
        if not get_current_messages():
            backend_messages = load_messages_from_backend(st.session_state.active_module)
            st.session_state.module_chats[st.session_state.active_module] = backend_messages
        
        # Exibir mensagens do histórico do módulo atual
        current_messages = get_current_messages()
        
        for i, message in enumerate(current_messages):
            with st.chat_message(message["role"]):
                # Verificar se esta é a mensagem que está sendo "digitada"
                if (st.session_state.typing_effect['active'] and 
                    st.session_state.typing_effect['module'] == st.session_state.active_module and
                    st.session_state.typing_effect['message_index'] == i and
                    message["role"] == "assistant"):
                    
                    # Mostrar efeito de digitação
                    typing = st.session_state.typing_effect
                    full_text = typing['full_text']
                    
                    # Calcular quantos caracteres mostrar baseado no tempo
                    chars_per_second = 200
                    elapsed_time = time.time() - typing['start_time']
                    target_chars = int(elapsed_time * chars_per_second)
                    
                    if target_chars >= len(full_text):
                        # Digitação completa
                        st.markdown(full_text)
                        st.session_state.typing_effect['active'] = False
                    else:
                        # Ainda digitando
                        partial_text = full_text[:target_chars]
                        st.markdown(partial_text + "▌")
                        
                        time.sleep(0.05)
                        st.rerun()
                else:
                    # Mensagem normal
                    st.markdown(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input(f"Pergunte algo sobre {st.session_state.active_module}..."):
        # Adicionar mensagem do usuário imediatamente
        add_message_to_current("user", prompt)
        
        # Gerar resposta completa da IA imediatamente
        ai_response = generate_ai_response(prompt, st.session_state.active_module)
        
        # Salvar resposta da IA no histórico
        add_message_to_current("assistant", ai_response)
        
        # Iniciar efeito de digitação para a última mensagem da IA
        last_message_index = len(get_current_messages()) - 1
        start_typing_effect(ai_response, st.session_state.active_module, last_message_index)
        
        # Recarregar para mostrar nova mensagem
        st.rerun()