import json
import sqlite3
import time
import os
import requests
from typing import List, Dict, Optional

class AIMemoryManager:
    def __init__(self, user_id: str = None, session_id: str = None):
        self.user_id = user_id or "anonymous"
        self.session_id = session_id or f"session_{int(time.time())}"
        self.backend_url = "http://localhost:3000/api/chat"
        self.local_db_path = "chat_memory.db"
        self.max_context_messages = 10
        self.request_timeout = 5
        
        # Module mapping from frontend to backend
        self.module_mapping = {
            'Fichas Técnicas': 'fichasTecnicas',
            'Logomarca': 'logomarca',
            'Mock-ups': 'mockups'
        }
        
        # Initialize local database
        self._init_local_db()
    
    def _get_backend_module(self, frontend_module: str) -> str:
        """Convert frontend module name to backend format"""
        return self.module_mapping.get(frontend_module, frontend_module.lower())
    
    def _init_local_db(self):
        """Initialize local SQLite database for offline fallback"""
        try:
            conn = sqlite3.connect(self.local_db_path)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    module TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    context TEXT,
                    timestamp REAL NOT NULL,
                    synced INTEGER DEFAULT 0
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error initializing local database: {e}")
    
    def _is_backend_available(self) -> bool:
        """Check if backend is available"""
        try:
            response = requests.get("http://localhost:3000/", timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
        except Exception:  
            return False
    
    def save_message(self, module: str, role: str, content: str, context: Dict = None) -> bool:
        """Save message with backend and local fallback"""
        backend_module = self._get_backend_module(module)
        
        message_data = {
            "userId": self.user_id,
            "sessionId": f"{self.user_id}_{self.session_id}",  
            "role": role,
            "content": content,
            "context": context or {}
        }
        
        try:
            response = requests.post(
                f"{self.backend_url}/{backend_module}/messages",
                json=message_data,
                timeout=self.request_timeout
            )
            if response.status_code == 201:
                return True
        except Exception as e:
            print(f"Backend save failed: {e}")
        
        return self._save_to_local(module, role, content, context)
    
    def load_messages(self, module: str, limit: int = 50) -> List[Dict]:
        """Load messages with backend priority and local fallback"""
        backend_module = self._get_backend_module(module)
        
        try:
            response = requests.get(
                f"{self.backend_url}/{backend_module}/messages",
                params={
                    "userId": self.user_id,
                    "sessionId": f"{self.user_id}_{self.session_id}", 
                    "limit": limit
                },
                timeout=self.request_timeout
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return [
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in data["messages"]
                    ]
        except Exception as e:
            print(f"Backend load failed: {e}")
        
        return self._load_from_local(module, limit)
    
    def _save_to_local(self, module: str, role: str, content: str, context: Dict = None) -> bool:
        """Save message to local database"""
        try:
            conn = sqlite3.connect(self.local_db_path)
            conn.execute('''
                INSERT INTO chat_messages 
                (user_id, session_id, module, role, content, context, timestamp, synced)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.user_id, f"{self.user_id}_{self.session_id}", module, role, content,
                json.dumps(context or {}), time.time(), 0
            ))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Local save failed: {e}")
            return False
    
    def _load_from_local(self, module: str, limit: int = 50) -> List[Dict]:
        """Load messages from local database"""
        try:
            conn = sqlite3.connect(self.local_db_path)
            cursor = conn.execute('''
                SELECT role, content FROM chat_messages
                WHERE user_id = ? AND session_id = ? AND module = ?
                ORDER BY timestamp ASC
                LIMIT ?
            ''', (self.user_id, f"{self.user_id}_{self.session_id}", module, limit))
            
            messages = [
                {"role": row[0], "content": row[1]}
                for row in cursor.fetchall()
            ]
            conn.close()
            return messages
        except Exception as e:
            print(f"Local load failed: {e}")
            return []
    
    def get_context(self, module: str) -> List[Dict]:
        """Get recent conversation context for AI"""
        backend_module = self._get_backend_module(module)
        
        try:
            response = requests.get(
                f"{self.backend_url}/{backend_module}/context",
                params={
                    "userId": self.user_id,
                    "sessionId": f"{self.user_id}_{self.session_id}",  
                    "maxMessages": self.max_context_messages
                },
                timeout=self.request_timeout
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return data["context"]
        except Exception as e:
            print(f"Backend context failed: {e}")
        
        return self._get_local_context(module)
    def _get_local_context(self, module: str) -> List[Dict]:
        """Get context from local database"""
        try:
            conn = sqlite3.connect(self.local_db_path)
            cursor = conn.execute('''
                SELECT role, content, timestamp FROM chat_messages
                WHERE user_id = ? AND session_id = ? AND module = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (self.user_id, f"{self.user_id}_{self.session_id}", module, self.max_context_messages))
            
            messages = [
                {"role": row[0], "content": row[1], "timestamp": row[2]}
                for row in cursor.fetchall()
            ]
            conn.close()
            return list(reversed(messages))
        except Exception as e:
            print(f"Local context failed: {e}")
            return []
    
    def clear_messages(self, module: str) -> bool:
        """Clear messages for a specific module"""
        backend_module = self._get_backend_module(module)
        
        # Try backend first
        try:
            response = requests.delete(
                f"{self.backend_url}/{backend_module}/messages",
                params={
                    "userId": self.user_id,
                    "sessionId": f"{self.user_id}_{self.session_id}" 
                },
                timeout=self.request_timeout
            )
            if response.status_code == 200:
                self._clear_local_messages(module)
                return True
        except Exception as e:
            print(f"Backend clear failed: {e}")
        
        return self._clear_local_messages(module)
    
    def _clear_local_messages(self, module: str) -> bool:
        """Clear messages from local database"""
        try:
            conn = sqlite3.connect(self.local_db_path)
            conn.execute('''
                DELETE FROM chat_messages
                WHERE user_id = ? AND session_id = ? AND module = ?
            ''', (self.user_id, f"{self.user_id}_{self.session_id}", module))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Local clear failed: {e}")
            return False
    
    def sync_local_to_backend(self) -> Dict:
        """Sync unsynced local messages to backend"""
        if not self._is_backend_available():
            return {"success": False, "error": "Backend not available"}
        
        try:
            conn = sqlite3.connect(self.local_db_path)
            cursor = conn.execute('''
                SELECT id, module, role, content, context FROM chat_messages
                WHERE user_id = ? AND synced = 0
                ORDER BY timestamp ASC
            ''', (self.user_id,))
            
            synced_count = 0
            failed_count = 0
            
            for row in cursor.fetchall():
                msg_id, module, role, content, context = row
                backend_module = self._get_backend_module(module)
                
                try:
                    response = requests.post(
                        f"{self.backend_url}/{backend_module}/messages",
                        json={
                            "userId": self.user_id,
                            "sessionId": f"{self.user_id}_{self.session_id}",  # User-specific session
                            "role": role,
                            "content": content,
                            "context": json.loads(context or "{}")
                        },
                        timeout=self.request_timeout
                    )
                    
                    if response.status_code == 201:
                        conn.execute('UPDATE chat_messages SET synced = 1 WHERE id = ?', (msg_id,))
                        synced_count += 1
                    else:
                        failed_count += 1
                        
                except Exception as e:
                    print(f"Failed to sync message {msg_id}: {e}")
                    failed_count += 1
            
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "synced": synced_count,
                "failed": failed_count
            }
            
        except Exception as e:
            print(f"Sync failed: {e}")
            return {"success": False, "error": str(e)}