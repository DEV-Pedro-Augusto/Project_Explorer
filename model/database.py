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
    def exibir_catalogo_de_status(db):
        # Aqui vamos direto na tabela de status, sem segredo
        resposta = db.table("status_dispositivos").select("nomes_status_dispositivos").execute()
        
        # Armazenamos a lista de resultados
        lista_status = resposta.data

        print("\n--- CATÁLOGO DE STATUS DISPONÍVEIS ---")
        for s in lista_status:
            # Definimos a variável com o nome do status
            nome_status = s['nomes_status_dispositivos']
            
            # Exibimos o resultado
            print(f"Status Cadastrado: {nome_status}")
    def buscar_relatorio_por_status(db, id_filtro):
        resposta = db.table("dispositivos").select(
            "codigos_dispositivos, "
            "nomes_dispositivos, "
            "fabricacoes_dispositivos, "
            "ativacoes_dispositivos, "
            "ultimas_conexoes_dispositivos, "
            "status_dispositivos(nomes_status_dispositivos)"
        ).eq("id_status_dispositivos", id_filtro).execute()

        # O 'resposta.data' é onde estão os resultados
        dispositivos = resposta.data

        for d in dispositivos:
            # Eles definem uma variável e atribuem o valor da coluna
            codigo = d['codigos_dispositivos']
            nome = d['nomes_dispositivos']
            data_fabricação = d['fabricacoes_dispositivos']
            data_ativação = d['ativacoes_dispositivos']
            ultima_conexao = d['ultimas_conexoes_dispositivos']
            status = d['status_dispositivos']['nomes_status_dispositivos']

        print(f"Exibindo Dados: Código {resposta.data}")
