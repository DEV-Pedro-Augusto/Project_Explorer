import os
import httpx
import logging
import math
import pandas as pd
from typing import List, Dict, Any
from supabase import create_client, Client
from supabase.lib.client_options import SyncClientOptions

# Configurações (Idealmente via variáveis de ambiente)
SUPABASE_URL = "https://ulgnemjbobycljlfuitc.supabase.co"
SUPABASE_KEY = "sb_publishable_BsXf3gfYCYCAz5LKlgHl_w_sGQjjMwd"

class Database:
    """Representa uma conexão com o banco de dados."""

    # Mapeamento Oficial Exigido (Adicionado do test.py)
    MAPEAMENTO_ETIQUETAS = {
        "mq2_ppm": 1,
        "mq2_lel_pct": 2,
        "mq3_ppm": 3,
        "mq3_mgl": 4,
        "mq7_ppm": 5,
        "mq7_cohb_pct": 6,
        "tempo_volta_s": 7,
        "dist_total_m": 8,
        "frente_cm": 9,
        "direita_cm": 10,
        "esquerda_cm": 11,
        "traseira_cm": 12
    }

    def __init__(self):
        # Inicializa a conexão ao criar o objeto (usando minúsculo)
        self.client = self.conectar_supabase()

    @staticmethod
    def conectar_supabase() -> Client:
        """Inicializa o cliente Supabase como um método estático."""
        try:
            # Para evitar erro de certificado em ambientes de desenvolvimento,
            # criamos um cliente httpx sem verificação de SSL.
            httpx_client = httpx.Client(verify=False)
            options = SyncClientOptions(httpx_client=httpx_client)

            supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY, options=options)
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
            resposta = self.client.table("logins").select("*").execute()
            print(f"Logins listados: {resposta.data}")
            return resposta.data or []
        except Exception as e:
            # Se a tabela 'logins' não existir, tenta recuperar credenciais da tabela 'usuarios'
            print(f"Erro ao carregar logins do banco: {e}")
            try:
                resp_usuarios = self.client.table('usuarios').select('id_usuarios, nomes_usuarios, emails_usuarios, senhas_usuarios, id_permissoes').execute()
                usuarios = resp_usuarios.data or []
                # Converte para estrutura similar à antiga tabela de logins
                logins = []
                for u in usuarios:
                    logins.append({
                        'id_logins': u.get('id_usuarios'),
                        'id_usuarios': u.get('id_usuarios'),
                        'id_permissoes': u.get('id_permissoes'),
                        'nomes_logins': u.get('emails_usuarios') or u.get('nomes_usuarios'),
                        'senhas_logins': u.get('senhas_usuarios') or u.get('senha')
                    })
                print(f"Logins (fallback de usuarios) listados: {logins}")
                return logins
            except Exception as e2:
                print(f"Erro ao carregar usuarios como fallback de logins: {e2}")
                return []
    
    def listar_leituras(self, id_sessao: str = None, id_dispositivo: int = None, id_sensor: int = None) -> list:
        """Retorna leituras da tabela de leituras, com filtros opcionais."""
        if not self.client:
            return []

        try:
            query = self.client.table("leituras").select(
                "id_leituras, id_sessoes_leituras, id_etiquetas_sensores, valores_lidos, data_hora"
            )

            if id_sessao is not None:
                query = query.eq("id_sessoes_leituras", id_sessao)
            elif id_dispositivo is not None:
                sessoes = self.listar_sessoes_leituras(id_dispositivo=id_dispositivo)
                session_ids = [s.get("id_sessoes_leituras") for s in sessoes if s.get("id_sessoes_leituras") is not None]
                if session_ids:
                    query = query.in_("id_sessoes_leituras", session_ids)
                else:
                    print(f"Nenhuma sessão encontrada para id_dispositivo {id_dispositivo}")
                    return []

            if id_sensor is not None:
                query = query.eq("id_etiquetas_sensores", id_sensor)

            resposta = query.order("data_hora", desc=True).execute()
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
            resposta = self.client.table("dispositivos").select("*").execute()
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
            resposta = self.client.table("sensores").select("*").execute()
            return resposta.data or []
        except Exception as e:
            print(f"Erro ao carregar sensores do banco: {e}")
            return []

    def listar_sensores_dispositivo(self, id_dispositivo: int) -> list:
        """Retorna apenas os sensores do dispositivo especificado."""
        if not self.client:
            return []

        try:
            # Busca na tabela de junção (juncao_ds) os sensores associados ao dispositivo
            resposta_juncao = self.client.table("juncao_ds").select("id_sensores").eq("id_dispositivos", id_dispositivo).execute()
            
            if not resposta_juncao.data:
                print(f"Nenhum sensor encontrado para o dispositivo {id_dispositivo}")
                return []
            
            # Extrai os IDs dos sensores
            ids_sensores = [item.get("id_sensores") for item in resposta_juncao.data if item.get("id_sensores")]
            
            if not ids_sensores:
                return []
            
            # Busca os dados completos dos sensores
            resposta_sensores = self.client.table("sensores").select("*").in_("id_sensores", ids_sensores).execute()
            
            return resposta_sensores.data or []
        except Exception as e:
            print(f"Erro ao carregar sensores do dispositivo {id_dispositivo}: {e}")
            return []

    def exibir_catalogo_de_status(self):
        """Exibe no console os status cadastrados."""
        if not self.client:  # Corrigido para minúsculo
            return

        resposta = self.client.table("status_dispositivos").select("*").execute()
        lista_status = resposta.data

        print("\n--- CATÁLOGO DE STATUS DISPONÍVEIS ---")
        for s in lista_status:
            # tenta chaves possíveis para o nome do status, sem assumir sufixos
            nome_status = s.get('nomes_status_dispositivos') or s.get('nomes_status') or s.get('nome_status') or str(s)
            print(f"Status Cadastrado: {nome_status}")

    def buscar_relatorio_por_status(self, id_filtro):
        """Busca dispositivos filtrados por um ID de status específico."""
        if not self.client:  # Corrigido para minúsculo
            return []

        try:
            resposta = self.client.table("dispositivos").select("*").eq("id_status_dispositivos", id_filtro).execute()
            dispositivos = resposta.data
        except Exception:
            # Coluna não existe no schema — busca todos e filtra em memória
            try:
                resp_all = self.client.table("dispositivos").select("*").execute()
                all_dispositivos = resp_all.data or []
            except Exception:
                return []

            dispositivos = []
            for d in all_dispositivos:
                if d.get('id_status_dispositivos') == id_filtro:
                    dispositivos.append(d)
                else:
                    # se a relação status_dispositivos estiver embutida
                    sd = d.get('status_dispositivos')
                    if sd:
                        sid = sd.get('id_status_dispositivos') or sd.get('id')
                        if sid == id_filtro:
                            dispositivos.append(d)

        for d in dispositivos:
            id_dispositivo = d.get('id_dispositivos')
            codigo = d.get('codigos_dispositivos')
            nome = d.get('nomes_dispositivos')
            data_fabricacao = d.get('fabricacoes_dispositivos')
            data_ativacao = d.get('ativacoes_dispositivos')
            ultima_conexao = d.get('ultimas_conexoes_dispositivos')

            # tenta obter status pela relação ou campo direto
            dados_status = d.get('status_dispositivos')
            if dados_status:
                status = dados_status.get('nomes_status_dispositivos') or dados_status.get('nomes_status') or dados_status.get('nome_status')
            else:
                # tenta buscar o nome do status na tabela de status pelo id
                id_status = d.get('id_status_dispositivos')
                status = "Sem Status"
                if id_status:
                    try:
                        resp_status = self.client.table('status_dispositivos').select('*').eq('id_status_dispositivos', id_status).execute()
                        sdata = resp_status.data[0] if resp_status.data else None
                        if sdata:
                            status = sdata.get('nomes_status_dispositivos') or sdata.get('nomes_status') or sdata.get('nome_status') or status
                    except Exception:
                        pass

        print(f"Exibindo Dados: Código {dispositivos}")
        return dispositivos

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
            resposta_usuario = self.client.table("usuarios").select("*").eq("emails_usuarios", email).execute()
            
            if resposta_usuario.data and len(resposta_usuario.data) > 0:
                usuario = resposta_usuario.data[0]
                id_usuario = usuario['id_usuarios']
                
                # Busca os dados de login na tabela logins (com fallback caso a tabela não exista)
                login_info = None
                try:
                    resposta_login = self.client.table("logins").select("*").eq("id_usuarios", id_usuario).execute()
                    if resposta_login and getattr(resposta_login, 'data', None) and len(resposta_login.data) > 0:
                        login_info = resposta_login.data[0]
                except Exception as e_login:
                    # tabela 'logins' pode não existir no schema; usaremos campos da tabela 'usuarios' como fallback
                    print(f"Aviso: não foi possível acessar 'logins' ({e_login}); usando 'usuarios' como fallback")
                    login_info = {
                        'senhas_logins': usuario.get('senhas_usuarios') or usuario.get('senha') or usuario.get('senhas'),
                        'nomes_logins': usuario.get('emails_usuarios') or usuario.get('nomes_usuarios'),
                        'id_usuarios': usuario.get('id_usuarios'),
                        'id_permissoes': usuario.get('id_permissoes')
                    }

                if login_info:
                    # Valida a senha usando campos possíveis
                    senha_salva = login_info.get('senhas_logins') or login_info.get('senha_logins') or login_info.get('senha') or login_info.get('senhas')
                    if senha_salva == senha:
                        print(f"Usuário autenticado: {usuario.get('nomes_usuarios')}")
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
            resposta = self.client.table("dispositivos").select("*").execute()
            
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
            # Usa chaves esperadas; o Supabase aceita chaves extras/ausentes conforme o schema
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
        """Retorna as sessões de leitura filtradas por usuário e/ou dispositivo."""
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

    def listar_agendamentos(self, id_dispositivo: int = None) -> list:
        """Retorna os agendamentos (opcionalmente filtrados por dispositivo)."""
        if not self.client:
            return []

        try:
            query = self.client.table("agendamentos").select("*")
            if id_dispositivo is not None:
                query = query.eq("id_dispositivos", id_dispositivo)

            # Executa a query sem order e ordena em memória se o campo existir
            resposta = query.execute()
            registros = resposta.data or []
            try:
                registros = sorted(
                    registros,
                    key=lambda r: r.get('data_hora_agendamento') or r.get('datas_agendamentos') or r.get('data') or ''
                )
            except Exception:
                pass

            print(f"Agendamentos listados: {registros}")
            return registros
        except Exception as e:
            print(f"Erro ao carregar agendamentos: {e}")
            return []

    def cadastrar_agendamento(self, data_hora_agendamento: str, id_dispositivo: int, descricao_livre: str, id_usuario: int = None) -> dict:
        """Insere um novo agendamento na tabela `agendamentos` usando o schema esperado."""
        if not self.client:
            return None

        try:
            novo = {
                "data_hora_agendamento": data_hora_agendamento,
                "id_dispositivos": id_dispositivo,
                "descricao_livre": descricao_livre,
            }
            if id_usuario is not None:
                novo["id_usuarios"] = id_usuario

            resposta = self.client.table("agendamentos").insert(novo).execute()
            print(f"Agendamento cadastrado: {resposta.data}")
            if resposta.data:
                return resposta.data[0] if isinstance(resposta.data, list) else resposta.data
            return None
        except Exception as e:
            print(f"Erro ao cadastrar agendamento: {e}")
            return None

    def deletar_agendamento(self, id_agendamento: int) -> bool:
        """Deleta um agendamento da tabela `agendamentos` pelo ID."""
        if not self.client:
            return False

        try:
            resposta = self.client.table("agendamentos").delete().eq("id", id_agendamento).execute()
            print(f"Agendamento deletado: {resposta.data}")
            return True
        except Exception as e:
            print(f"Erro ao deletar agendamento: {e}")
            return False

    @staticmethod
    def _obter_timestamp_agora() -> str:
        """Retorna o timestamp atual no formato ISO."""
        from datetime import datetime
        return datetime.now().isoformat()


    def processar_pipeline_telemetria(self, path_gases: str, path_movimento: str) -> List[Dict[str, Any]]:
        """Executa a fusão e verticalização (EAV) de dois arquivos CSV quaisquer.
        
        Retorna a lista verticalizada pronta para inserção no banco.
        """
        try:
            print(f"Iniciando pipeline de fusão:\n-> Gases: {path_gases}\n-> Movimento: {path_movimento}")
            
            # 1. Carrega os arquivos ignorando comentários
            df_gases = pd.read_csv(path_gases, comment='#')
            df_movimento = pd.read_csv(path_movimento, comment='#')

            # 2. Limpa e ordena Gases
            df_gases['horario'] = pd.to_datetime(df_gases['horario'], errors='coerce')
            df_gases.sort_values('horario', inplace=True)

            # 3. Limpa e ordena Movimento (Mantendo 'Sem Leitura' como 0)
            df_movimento['horario'] = pd.to_datetime(df_movimento['horario'], errors='coerce')
            colunas_numericas = ['tempo_volta_s', 'dist_total_m', 'frente_cm', 'direita_cm', 'esquerda_cm', 'traseira_cm']
            for col in colunas_numericas:
                if col in df_movimento.columns:
                    df_movimento[col] = pd.to_numeric(df_movimento[col], errors='coerce').fillna(0)
            df_movimento.sort_values('horario', inplace=True)

            # 4. Sincroniza tabelas por proximidade temporal (Merge Asof)
            df_sync = pd.merge_asof(
                left=df_gases,
                right=df_movimento,
                on='horario',
                direction='nearest',
                tolerance=pd.Timedelta(seconds=5),
                suffixes=('_gases', '_mov')
            )
            df_sync = df_sync.where(pd.notnull(df_sync), None)

            # 5. Estrutura a lista unificada e verticaliza no padrão EAV
            lista_verticalizada = []
            for _, row in df_sync.iterrows():
                horario_iso = row["horario"].isoformat()

                linha_unificada = {
                    "mq2_ppm": row.get("mq2_ppm"),
                    "mq2_lel_pct": row.get("mq2_lel_pct"),
                    "mq3_ppm": row.get("mq3_ppm"),
                    "mq3_mgl": row.get("mq3_mgl"),
                    "mq7_ppm": row.get("mq7_ppm"),
                    "mq7_cohb_pct": row.get("mq7_cohb_pct"),
                    "tempo_volta_s": row.get("tempo_volta_s_mov") if row.get("tempo_volta_s_mov") is not None else row.get("tempo_volta_s_gases"),
                    "dist_total_m": row.get("dist_total_m"),
                    "frente_cm": row.get("frente_cm"),
                    "direita_cm": row.get("direita_cm"),
                    "esquerda_cm": row.get("esquerda_cm"),
                    "traseira_cm": row.get("traseira_cm")
                }

                # Cria a lista verticalizada usando o dicionário MAPEAMENTO_ETIQUETAS
                for chave, id_tag in self.MAPEAMENTO_ETIQUETAS.items():
                    valor = linha_unificada.get(chave)
                    if valor is not None and not (isinstance(valor, float) and math.isnan(valor)):
                        lista_verticalizada.append({
                            "horario": horario_iso,
                            "id_etiqueta": id_tag,
                            "valor": float(valor)
                        })

            print(f"Pipeline concluído com sucesso. {len(lista_verticalizada)} registros gerados.")
            return lista_verticalizada

        except Exception as e:
            print(f"Erro ao executar o pipeline de telemetria: {e}")
            return []

    def importar_telemetria_supabase(self, path_gases: str, path_movimento: str, id_usuario: int, id_dispositivo: int, descricao: str = "Importação automática via pipeline") -> bool:
        """Processa os CSVs informados, cria uma sessão vinculada ao carrinho (id_dispositivo) 
        e insere as leituras em blocos.
        """
        if not self.client:
            print("Erro: Sem conexão com o banco de dados")
            return False

        # Executa o processamento dos arquivos selecionados
        dados_verticalizados = self.processar_pipeline_telemetria(path_gases, path_movimento)
        if not dados_verticalizados:
            print("Erro: Nenhum dado foi processado pelo pipeline.")
            return False

        try:
            # Descobre os limites temporais (Início e Fim da missão)
            horarios = sorted([reg["horario"] for reg in dados_verticalizados])
            inicio_missao = horarios[0]
            fim_missao = horarios[-1]

            # Cria o payload da sessão usando o ID do Carrinho (id_dispositivo)
            sessao_payload = {
                "id_usuarios": id_usuario,
                "id_dispositivos": id_dispositivo,  # Vinculação correta com o carrinho
                "inicio_missao": inicio_missao,
                "fim_missao": fim_missao,
                "descricao_livre": descricao
            }

            # Insere a sessão de leitura no Supabase
            res_sessao = self.client.table("sessoes_leituras").insert(sessao_payload).execute()
            if not res_sessao.data:
                print("Erro ao tentar salvar a sessão de leitura.")
                return False

            id_sessao = res_sessao.data[0]["id_sessoes_leituras"]
            print(f"Nova sessão de leitura cadastrada com ID: {id_sessao}")

            # Prepara a lista final de leituras mapeando as colunas do banco
            dados_para_inserir = []
            for registro in dados_verticalizados:
                dados_para_inserir.append({
                    "id_sessoes_leituras": id_sessao,
                    "id_etiquetas_sensores": registro["id_etiqueta"],
                    "valores_lidos": registro["valor"],
                    "data_hora": registro["horario"]
                })

            # Inserção em lotes de 500 registros para otimização de banda
            BATCH_SIZE = 500
            for i in range(0, len(dados_para_inserir), BATCH_SIZE):
                lote = dados_para_inserir[i:i + BATCH_SIZE]
                self.client.table("leituras").insert(lote).execute()
                print(f"Enviando lote de leituras: {i + len(lote)} / {len(dados_para_inserir)}")

            print(f"🎉 Processamento e Upload finalizados! {len(dados_para_inserir)} leituras salvas na sessão {id_sessao}.")
            return True

        except Exception as e:
            print(f"Erro durante a inserção dos dados no Supabase: {e}")
            return False