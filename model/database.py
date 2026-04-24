import os
from supabase import create_client, Client

# Configurações (Idealmente via variáveis de ambiente)
SUPABASE_URL = "https://ulgnemjbobycljlfuitc.supabase.co"
SUPABASE_KEY = "sb_publishable_BsXf3gfYCYCAz5LKlgHl_w_sGQjjMwd"

class Database:
    """Representa uma conexão com o banco de dados."""

    def __init__(self):
        # Inicializa a conexão ao criar o objeto
        self.client = self.conectar_supabase()

    @staticmethod
    def conectar_supabase() -> Client:
        """Inicializa o cliente Supabase como um método estático."""
        try:
            supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            print("✅ Conexão estabelecida com sucesso!")
            return supabase
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return None
