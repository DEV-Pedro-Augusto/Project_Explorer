

class Database:
    """Representa uma conexão com o banco de dados."""

    def __init__(self,system):
        # Inicializa a conexão ao criar o objeto (usando minúsculo)
        self.system = system
        self.client = self.conectar_supabase()

    @staticmethod
    def conectar_supabase(self):
        """Inicializa o cliente Supabase utilizando o contexto do system."""
        try:
            # Para evitar erro de certificado em ambientes de desenvolvimento,
            # criamos um cliente httpx sem verificação de SSL.
            # Acessando o httpx que foi injetado via system:
            httpx_client = self.system.httpx.Client(verify=False)
            
            # Buscando as classes e opções estruturadas dentro do dicionário ou atributos do seu system:
            SyncClientOptions = self.system.supabase["SyncClientOptions"]
            create_client = self.system.supabase["create_client"]
            
            supabase_url = self.system.supabase["SUPABASE_URL"]
            supabase_key = self.system.supabase["SUPABASE_KEY"]

            options = SyncClientOptions(httpx_client=httpx_client)

            # Instanciando o cliente do Supabase de forma dinâmica
            supabase = create_client(supabase_url, supabase_key, options=options)
            
            print("Conexão estabelecida com sucesso!")
            return supabase
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            return None
        
    def listar_logins(self) -> list:
        """Retorna todos os logins da tabela de usuários."""
        if not self.client:  # Corrigido para minúsculo
            return []

        try:
            resposta = self.client.table("logins").select(
                "id_logins,id_usuarios,id_permissoes,nomes_logins,senhas_logins"
            ).execute()
            print(f"Logins listados: {resposta.data}")
            return resposta.data or []
        except Exception as e:
            print(f"Erro ao carregar logins do banco: {e}")
            return []
    
    def listar_leituras(self) -> list:
        """Retorna todas as leituras da tabela de leituras."""
        if not self.client:  # Corrigido para minúsculo
            return []

        try:
            resposta = self.client.table("leituras").select(
                "id_leituras, id_sessoes_leituras, id_etiquetas_sensores, valores_lidos, data_hora"
            ).execute()
            print(f"Leituras listadas: {resposta.data}")
            return resposta.data or []
        except Exception as e:
            print(f"Erro ao carregar leituras do banco: {e}")
            return []

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

    def autenticar_usuario(self, email: str, senha: str) -> dict:
        """Autentica um usuário verificando email e senha."""
        if not self.client:
            print("Erro: Sem conexão com o banco de dados")
            return None

        try:
            # Busca o usuário pela coluna email na tabela usuarios
            resposta_usuario = self.client.table("usuarios").select(
                "id_usuarios, nomes_usuarios, emails_usuarios, telefone_usuarios"
            ).eq("emails_usuarios", email).execute()
            
            if resposta_usuario.data and len(resposta_usuario.data) > 0:
                usuario = resposta_usuario.data[0]
                id_usuario = usuario['id_usuarios']
                
                # Busca os dados de login na tabela logins
                resposta_login = self.client.table("logins").select(
                    "id_logins, id_usuarios, nomes_logins, senhas_logins"
                ).eq("id_usuarios", id_usuario).execute()
                
                if resposta_login.data and len(resposta_login.data) > 0:
                    login_info = resposta_login.data[0]
                    
                    # Valida a senha
                    if login_info['senhas_logins'] == senha:
                        print(f"Usuário autenticado: {usuario['nomes_usuarios']}")
                        return usuario
                    else:
                        print("Senha incorreta")
                        return None
                else:
                    print("Dados de login não encontrados")
                    return None
            else:
                print("Usuário não encontrado")
                return None
        except Exception as e:
            print(f"Erro ao autenticar usuário: {e}")
            return None

    def listar_carrinhos_usuario(self, id_usuario: int) -> list:
        """Retorna todos os carrinhos/dispositivos disponíveis."""
        if not self.client:
            return []

        try:
            # Carrega todos os dispositivos (ajuste conforme a relação usuario-dispositivo)
            resposta = self.client.table("dispositivos").select(
                "id_dispositivos, nomes_dispositivos, codigos_dispositivos"
            ).execute()
            
            print(f"Carrinhos carregados: {resposta.data}")
            return resposta.data or []
        except Exception as e:
            print(f"Erro ao carregar carrinhos: {e}")
            return []

    def cadastrar_carrinho(self, nome: str, codigo: str, id_usuario: int) -> dict:
        """Cadastra um novo carrinho/dispositivo para um usuário."""
        if not self.client:
            print("Erro: Sem conexão com o banco de dados")
            return None

        try:
            # Insere um novo dispositivo
            novo_dispositivo = {
                "nomes_dispositivos": nome,
                "codigos_dispositivos": codigo,
                "id_usuarios": id_usuario,
                "ativacoes_dispositivos": self._obter_timestamp_agora(),
                "status_dispositivos": 1  # Status ativo (ajuste conforme seu sistema)
            }
            
            resposta = self.client.table("dispositivos").insert(novo_dispositivo).execute()
            
            if resposta.data:
                print(f"Carrinho '{nome}' cadastrado com sucesso!")
                return resposta.data[0] if isinstance(resposta.data, list) else resposta.data
            else:
                print("Erro ao cadastrar carrinho")
                return None
        except Exception as e:
            print(f"Erro ao cadastrar carrinho: {e}")
            return None

    def listar_sessoes_leituras(self, id_usuario: int = None, id_dispositivo: int = None) -> list:
        """Retorna as sessões de leitura filtradas por usuário e/ou dispositivo.

        Se nenhum filtro for informado, retorna todas as sessões ordenadas por `datas_uploads` desc.
        """
        if not self.client:
            return []

        try:
            query = self.client.table("sessoes_leituras").select(
                "id_sessoes_leituras, id_usuarios, id_dispositivos, datas_uploads, inicio_missao, fim_missao, descricao_livre"
            )

            # Aplica filtros quando fornecidos
            if id_usuario:
                query = query.eq("id_usuarios", id_usuario)
            if id_dispositivo:
                query = query.eq("id_dispositivos", id_dispositivo)

            # Ordena por data de upload (mais recentes primeiro)
            resposta = query.order("datas_uploads", desc=True).execute()

            print(f"Sessões de leitura listadas: {resposta.data}")
            return resposta.data or []
        except Exception as e:
            print(f"Erro ao carregar sessões de leitura: {e}")
            return []

    @staticmethod
    def _obter_timestamp_agora() -> str:
        """Retorna o timestamp atual no formato ISO."""
        from datetime import datetime
        return datetime.now().isoformat()