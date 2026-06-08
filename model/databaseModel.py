"""Database connection wrapper."""

class Database:
    """Represents a database connection and provides basic helpers."""

    def __init__(self, config: dict):
        self.config = config
        self.connection = None

<<<<<<< Updated upstream
    def connect(self):
        """Open a database connection. Placeholder implementation."""
        # TODO: implement real database connection logic.
        self.connection = True
        return self.connection

    def close(self):
        """Close the database connection."""
        self.connection = None
=======
    @staticmethod
        def conectar_supabase(self):
        """Inicializa o cliente Supabase utilizando as novas credenciais."""
        try:
            httpx_client = self.system.httpx.Client(verify=False)

            options = self.system.supabase["SyncClientOptions"](
                httpx_client=httpx_client
            )

            supabase = self.system.supabase["create_client"](
                "https://ulgnemjbobycljlfuitc.supabase.co",
                "sb_publishable_BsXf3gfYCYCAz5LKlgHl_w_sGQjjMwd",
                options=options
            )

            print("Conexão estabelecida com sucesso!")
            return supabase

        except Exception as e:
            print(f"Erro ao conectar: {e}")
            return None

    def listar_itens(self) -> list:
        """Retorna todos os itens da tabela de dispositivos."""
        if not self.client:  # Corrigido para minúsculo
            return []

        try:
            resposta = self.client.table("dispositivos").select(
                "id_dispositivos, codigos_dispositivos, nomes_dispositivos, fabricacoes_dispositivos, ativacoes_dispositivos, ultimas_conexoes_dispositivos, status_dispositivos(nomes_status_dispositivos)"
            ).execute()
            print(f"Itens listados: {resposta.data}")
            return resposta.data or []
        except Exception as e:
            print(f"Erro ao carregar itens do banco: {e}")
            return []
    def listar_sensores(self) -> list:
        """Retorna todos os sensores da tabela de sensores."""
        if not self.client:  # Corrigido para minúsculo
            return []

        try:
            resposta = self.client.table("sensores").select(
                "id_sensores, codigos_sensores, nomes_sensores, fabricacoes_sensores, ativacoes_sensores, ultimas_conexoes_sensores"
            ).execute()
            return resposta.data or []
        except Exception as e:
            print(f"Erro ao carregar sensores do banco: {e}")
            return []

    def exibir_catalogo_de_status(self):
        """Exibe no console os status cadastrados."""
        if not self.client:  # Corrigido para minúsculo
            return

        resposta = self.client.table("status_dispositivos").select("nomes_status_dispositivos").execute()
        lista_status = resposta.data

        print("\n--- CATÁLOGO DE STATUS DISPONÍVEIS ---")
        for s in lista_status:
            nome_status = s['nomes_status_dispositivos']
            print(f"Status Cadastrado: {nome_status}")

    def buscar_relatorio_por_status(self, id_filtro):
        """Busca dispositivos filtrados por um ID de status específico."""
        if not self.client:  # Corrigido para minúsculo
            return []

        resposta = self.client.table("dispositivos").select(
            "id_dispositivos, "
            "codigos_dispositivos, "
            "nomes_dispositivos, "
            "fabricacoes_dispositivos, "
            "ativacoes_dispositivos, "
            "ultimas_conexoes_dispositivos, "
            "status_dispositivos(nomes_status_dispositivos)"
        ).eq("id_status_dispositivos", id_filtro).execute()

        dispositivos = resposta.data

        for d in dispositivos:
            id_dispositivo = d['id_dispositivos']
            codigo = d['codigos_dispositivos']
            nome = d['nomes_dispositivos']
            data_fabricação = d['fabricacoes_dispositivos']
            data_ativação = d['ativacoes_dispositivos']
            ultima_conexao = d['ultimas_conexoes_dispositivos']
            
            # .get() evita erros caso o relacionamento retorne nulo (None)
            dados_status = d.get('status_dispositivos')
            status = dados_status.get('nomes_status_dispositivos') if dados_status else "Sem Status"

        print(f"Exibindo Dados: Código {resposta.data}")
        return resposta.data

    def buscar_relatorio_por_sensor(self, id_sensor):
        """Busca os registros da junção filtrando pelo ID do sensor."""
        if not self.client:  # Corrigido para minúsculo
            return []

        requisicao = self.client.table("juncao_ds")\
            .select("id_juncao_ds, id_dispositivos, id_sensores")\
            .eq("id_sensores", id_sensor)\
            .execute()
        
        dados = requisicao.data if hasattr(requisicao, 'data') else requisicao
        
        print(f"Exibindo Dados do Sensor {id_sensor}: {dados}")
        return dados
>>>>>>> Stashed changes
