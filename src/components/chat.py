import streamlit as st
import time
import requests
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from utils.memory_manager import AIMemoryManager

def get_memory_manager():
    if 'memory_manager' not in st.session_state:
        user_id = st.session_state.get('current_user', 'anonymous')
        session_id = st.session_state.get('session_id')
        st.session_state.memory_manager = AIMemoryManager(user_id, session_id)
    return st.session_state.memory_manager

def save_message_to_backend(module, role, content):
    memory_manager = get_memory_manager()
    return memory_manager.save_message(module, role, content)

def load_messages_from_backend(module):
    memory_manager = get_memory_manager()
    return memory_manager.load_messages(module)

def generate_ai_response(prompt, module_name):
    memory_manager = get_memory_manager()
    
    context = memory_manager.get_context(module_name)
    
    responses = {
        'Fichas Técnicas': f"📋 **Fichas Técnicas**: Posso ajudar você a criar fichas técnicas detalhadas para '{prompt}'. Incluo informações nutricionais, ingredientes, modo de preparo e especificações técnicas completas.",
        
        'Logomarca': f"🎨 **Logomarca**: Para '{prompt}', posso sugerir conceitos de design que reflitam a identidade da sua marca alimentar.",
        
        'Mock-ups': f"📱 **Mock-ups**: Vou criar propostas visuais para '{prompt}', incluindo diversos materiais promocionais."
    }
    
    base_response = responses.get(module_name, f"Resposta para '{prompt}' no módulo {module_name}")
    
    if len(context) > 0:
        base_response += f"\n\n*Baseado em nossa conversa anterior, posso personalizar ainda mais essa resposta.*"
    
    return base_response

def switch_module(module_name):
    if module_name != st.session_state.active_module:
        st.session_state.active_module = module_name
        messages = load_messages_from_backend(module_name)
        st.session_state.module_chats[module_name] = messages
        st.session_state.typing_effect['active'] = False
        st.rerun()

def clear_current_chat():
    current_module = st.session_state.active_module
    memory_manager = get_memory_manager()
    
    if memory_manager.clear_messages(current_module):
        st.session_state.module_chats[current_module] = []
        
        if st.session_state.typing_effect['module'] == current_module:
            st.session_state.typing_effect['active'] = False
        st.rerun()

def clear_all_chats():
    memory_manager = get_memory_manager()
    
    for module in ['Fichas Técnicas', 'Logomarca', 'Mock-ups']:
        memory_manager.clear_messages(module)
    
    st.session_state.module_chats = {
        'Fichas Técnicas': [],
        'Logomarca': [],
        'Mock-ups': []
    }
    
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
    st.session_state.module_chats = {
        'Fichas Técnicas': [],
        'Logomarca': [],
        'Mock-ups': []
    }
    if 'memory_manager' in st.session_state:
        del st.session_state['memory_manager']
    st.session_state.typing_effect['active'] = False
    st.rerun()

def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

def render_chat_page():    
    memory_manager = get_memory_manager()
    with st.sidebar:
        st.markdown(f"## 👋 Olá, {st.session_state.current_user}")
        st.markdown("*Food Wise v0.1*")
        st.markdown("---")
        if memory_manager._is_backend_available():
            st.success("🟢 Online")
        else:
            st.warning("🟡 Modo Offline")
            if st.button("🔄 Sincronizar", use_container_width=True):
                sync_result = memory_manager.sync_local_to_backend()
                if sync_result["success"]:
                    st.success(f"✅ {sync_result['synced']} mensagens sincronizadas")
                else:
                    st.error("❌ Falha na sincronização")
        
        if st.button("🏠 Página Inicial", use_container_width=True):
            st.session_state.current_page = 'home'
            st.rerun()

        if st.button("🚪 Logout", use_container_width=True):
            logout()
        
        st.markdown("---")
        st.markdown("### Selecione um módulo:")
        
        modules_config = [
            ('📋', 'Fichas Técnicas'),
            ('🎨', 'Logomarca'),
            ('📱', 'Mock-ups')
        ]
        
        for icon, module_name in modules_config:
            is_active = st.session_state.active_module == module_name
            
            button_label = f"{icon} {module_name}"
            
            if st.button(
                button_label,
                key=f"module_btn_{module_name}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                switch_module(module_name)
        
        st.markdown("---")
        st.markdown("### Configurações")
        
        if st.button("🗑️ Limpar Atual", use_container_width=True):
            clear_current_chat()
        
        if st.button("🗑️ Limpar Todos", use_container_width=True):
            clear_all_chats()
        
    
    # Lógica do chat
    st.title("🍽️ Food Wise - Chat IA")
    st.markdown(f"**Módulo Ativo:** {st.session_state.active_module}")
    
    chat_container = st.container()
    
    with chat_container:
        if not get_current_messages():
            messages = load_messages_from_backend(st.session_state.active_module)
            st.session_state.module_chats[st.session_state.active_module] = messages
        
        current_messages = get_current_messages()
        
        for i, message in enumerate(current_messages):
            with st.chat_message(message["role"]):
                if (st.session_state.typing_effect['active'] and 
                    st.session_state.typing_effect['module'] == st.session_state.active_module and
                    st.session_state.typing_effect['message_index'] == i and
                    message["role"] == "assistant"):
                    
                    typing = st.session_state.typing_effect
                    full_text = typing['full_text']
                    
                    chars_per_second = 100
                    elapsed_time = time.time() - typing['start_time']
                    target_chars = int(elapsed_time * chars_per_second)
                    
                    if target_chars >= len(full_text):
                        st.markdown(full_text)
                        st.session_state.typing_effect['active'] = False
                    else:
                        partial_text = full_text[:target_chars]
                        st.markdown(partial_text + "▌")
                        
                        time.sleep(0.05)
                        st.rerun()
                else:
                    st.markdown(message["content"])
    
    st.markdown('<div class="chat-separator"></div>', unsafe_allow_html=True)
    
    input_container = st.container()
    with input_container:
        if prompt := st.chat_input(f"💬 Pergunte algo sobre {st.session_state.active_module}..."):
            add_message_to_current("user", prompt)
            
            ai_response = generate_ai_response(prompt, st.session_state.active_module)
            
            add_message_to_current("assistant", ai_response)
            
            last_message_index = len(get_current_messages()) - 1
            start_typing_effect(ai_response, st.session_state.active_module, last_message_index)
            
            st.rerun()