import flet as ft
import time
import pandas as pd
import math
import re
from datetime import datetime

class ProfileSelectionView:
    def __init__(self, system):
        self.system = system
        self.page = system.page
        self.on_profile_selected = None  # Será definido conforme necessário
        self.db_client = system.model.database if hasattr(system.model, 'database') else None

    def _load_carrinhos(self) -> list:
        """Carrega os carrinhos/dispositivos do usuário logado do banco de dados."""
        if not self.db_client or not self.system:
            print("Erro: db_client ou system não disponível")
            return []
        try:
            # Obtém o ID do usuário logado
            id_usuario = self.system.model.usuario_model.obter_id_usuario()
            if not id_usuario:
                print("Nenhum usuário logado")
                return []
            
            # --- TRAVA DE SEGURANÇA CONTRA ERRO DE INSTÂNCIA ---
            db = self.db_client
            if isinstance(db, type):
                db = db(self.system)
            
            carrinhos = db.listar_carrinhos_usuario(id_usuario)
            return carrinhos or []
        except Exception as e:
            print(f"Erro ao carregar carrinhos: {e}")
            import traceback
            traceback.print_exc()
            return []

    def render(self):
        self.page.clean()
        self.page.padding = 0

        # Fundo global da tela (Gradiente Escuro Roxo/Azul estilo HBO)
        fundo_gradiente = ft.RadialGradient(
            colors=["#2A0A4A", "#050011"], 
            center=ft.alignment.top_center, 
            radius=1.5
        )

        # --- CONSTRUTORES DE TELAS INTERNAS ---

        def build_selection_view():
            """Constrói a tela inicial com as bolhas dos perfis."""
            titulo = ft.Text("Quem está monitorando?", size=40, weight=ft.FontWeight.W_300, color=ft.Colors.WHITE)

            def handle_logout(e):
                self.system.model.usuario_model.limpar_usuario()
                self.system.view.animate.animacaoPagina.animar_tela(self.system, self.system.view.page.login)

            btn_logout = ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                    icon_color=ft.Colors.RED_400,
                    icon_size=24,
                    tooltip="Logout",
                    on_click=handle_logout
                ),
                alignment=ft.alignment.top_left,
                padding=ft.padding.only(top=20, left=40)
            )

            # Botão de Engrenagem abre a nova Sincronização de Telemetria
            btn_engrenagem = ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.SETTINGS,
                    icon_color=ft.Colors.GREY_400,
                    icon_size=28,
                    tooltip="Sincronização de Telemetria",
                    on_click=lambda e: trocar_tela(build_sincronizacao_view())
                ),
                alignment=ft.alignment.top_right,
                padding=ft.padding.only(top=20, right=40)
            )

            def criar_bolha_perfil(nome, gradiente_colors, is_add_button=False, carrinho=None):
                letra_inicial = nome[0].upper() if not is_add_button else "+"
                
                circulo_interno = ft.Container(
                    width=132, height=132, shape=ft.BoxShape.CIRCLE, bgcolor="#050011",
                    content=ft.Text(letra_inicial, size=50, weight=ft.FontWeight.W_200, color=ft.Colors.WHITE),
                    alignment=ft.alignment.center,
                )

                circulo_externo = ft.Container(
                    width=140, height=140, shape=ft.BoxShape.CIRCLE,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=gradiente_colors
                    ) if not is_add_button else None,
                    border=ft.border.all(2, ft.Colors.GREY_700) if is_add_button else None,
                    content=circulo_interno, alignment=ft.alignment.center,
                    animate_scale=ft.Animation(200, ft.AnimationCurve.DECELERATE),
                )

                nome_texto = ft.Text(nome, size=16, color=ft.Colors.GREY_400, weight=ft.FontWeight.W_400)

                lapis_icon = ft.IconButton(
                    icon=ft.Icons.EDIT, icon_color=ft.Colors.GREY_600, icon_size=16,
                    on_click=lambda e: trocar_tela(build_edit_view(nome, gradiente_colors)),
                    visible=not is_add_button
                )

                def on_hover(e):
                    if e.data == "true":
                        circulo_externo.scale = 1.1
                        nome_texto.color = ft.Colors.WHITE
                    else:
                        circulo_externo.scale = 1.0
                        nome_texto.color = ft.Colors.GREY_400
                    circulo_externo.update()
                    nome_texto.update()

                def on_click_action(e):
                    if is_add_button:
                        self.system.view.page.cadastro_carrinho(self.system).render()
                    else:
                        try:
                            if carrinho and carrinho.get('id_dispositivos'):
                                self.system.model.usuario_model.definir_dispositivo(carrinho.get('id_dispositivos'))
                        except Exception as ex:
                            print(f"Erro ao definir dispositivo: {ex}")
                        self.system.view.page.home(self.system).render()

                return ft.Container(
                    content=ft.Column(
                        [
                            circulo_externo, ft.Container(height=10),
                            ft.Row([nome_texto, lapis_icon], alignment=ft.MainAxisAlignment.CENTER, spacing=0)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0
                    ),
                    on_hover=on_hover, on_click=on_click_action
                )

            grid_perfis = ft.Row([], alignment=ft.MainAxisAlignment.CENTER, spacing=50)

            carrinhos = self._load_carrinhos()
            cores_padrao = [
                ["#FF007F", "#7F00FF"], ["#0052D4", "#6FB1FC"], ["#FF6B6B", "#FF8C42"],
                ["#4ECDC4", "#44A08D"], ["#9B59B6", "#8E44AD"],
            ]
            
            bolhas_carrinhos = []
            for idx, carrinho in enumerate(carrinhos):
                nome = carrinho.get('nomes_dispositivos', f'Carrinho {idx + 1}')
                cores = cores_padrao[idx % len(cores_padrao)]
                bolhas_carrinhos.append(criar_bolha_perfil(nome, cores, False, carrinho))
            
            bolhas_carrinhos.append(criar_bolha_perfil("Adicionar", [], is_add_button=True, carrinho=None))
            grid_perfis.controls = bolhas_carrinhos

            topbar = ft.Row([btn_logout, ft.Container(expand=True), btn_engrenagem], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=False)

            return ft.Column(
                [
                    topbar, ft.Container(height=40), titulo, ft.Container(height=60), grid_perfis,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True
            )

        def build_sincronizacao_view():
            """Painel de Sincronização de Telemetria (ETL)"""
            MAPEAMENTO_ETIQUETAS = {
                "mq2_ppm": 1, "mq2_lel_pct": 2, "mq3_ppm": 3, "mq3_mgl": 4,
                "mq7_ppm": 5, "mq7_cohb_pct": 6, "tempo_volta_s": 7,
                "dist_total_m": 8, "frente_cm": 9, "direita_cm": 10,
                "esquerda_cm": 11, "traseira_cm": 12
            }

            state = {"arquivos": []}

            titulo_row = ft.Row([
                ft.Icon(ft.Icons.SYNC_ALT, color=ft.Colors.CYAN_400, size=32),
                ft.Text("Sincronização de Telemetria", size=28, weight=ft.FontWeight.W_400, color=ft.Colors.WHITE)
            ], alignment=ft.MainAxisAlignment.CENTER)
            
            status_text = ft.Text("Aguardando arquivos...", color=ft.Colors.GREY_400, size=14, weight=ft.FontWeight.W_500)
            lista_arquivos_ui = ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

            def processar_arquivos(path_gases, path_movimento, id_u, id_d):
                try:
                    df_gases = pd.read_csv(path_gases, comment='#')
                    df_movimento = pd.read_csv(path_movimento, comment='#')

                    df_gases['horario'] = pd.to_datetime(df_gases['horario'], errors='coerce')
                    df_gases.sort_values('horario', inplace=True)

                    df_movimento['horario'] = pd.to_datetime(df_movimento['horario'], errors='coerce')
                    colunas_numericas = ['tempo_volta_s', 'dist_total_m', 'frente_cm', 'direita_cm', 'esquerda_cm', 'traseira_cm']
                    for col in colunas_numericas:
                        if col in df_movimento.columns:
                            df_movimento[col] = pd.to_numeric(df_movimento[col], errors='coerce').fillna(0)
                    df_movimento.sort_values('horario', inplace=True)

                    df_sync = pd.merge_asof(
                        left=df_gases, right=df_movimento,
                        on='horario', direction='nearest',
                        tolerance=pd.Timedelta(seconds=5), suffixes=('_gases', '_mov')
                    )
                    df_sync = df_sync.where(pd.notnull(df_sync), None)

                    lista_verticalizada = []
                    horarios_validos = []
                    
                    for _, row in df_sync.iterrows():
                        horario = row["horario"]
                        if pd.isnull(horario): continue
                        
                        horario_iso = horario.isoformat()
                        horarios_validos.append(horario_iso)

                        registro = {
                            "mq2_ppm": row.get("mq2_ppm"), "mq2_lel_pct": row.get("mq2_lel_pct"),
                            "mq3_ppm": row.get("mq3_ppm"), "mq3_mgl": row.get("mq3_mgl"),
                            "mq7_ppm": row.get("mq7_ppm"), "mq7_cohb_pct": row.get("mq7_cohb_pct"),
                            "tempo_volta_s": row.get("tempo_volta_s_mov") if row.get("tempo_volta_s_mov") is not None else row.get("tempo_volta_s_gases"),
                            "dist_total_m": row.get("dist_total_m"), "frente_cm": row.get("frente_cm"),
                            "direita_cm": row.get("direita_cm"), "esquerda_cm": row.get("esquerda_cm"),
                            "traseira_cm": row.get("traseira_cm")
                        }

                        for chave, id_tag in MAPEAMENTO_ETIQUETAS.items():
                            valor = registro.get(chave)
                            if valor is not None and not (isinstance(valor, float) and math.isnan(valor)):
                                lista_verticalizada.append({
                                    "horario": horario_iso, "id_etiqueta": id_tag, "valor": float(valor)
                                })

                    if not lista_verticalizada:
                        return False, "Nenhum dado válido para sincronizar."

                    horarios_validos.sort()
                    inicio_missao = horarios_validos[0]
                    fim_missao = horarios_validos[-1]

                    id_usuario_final = id_u or self.system.model.usuario_model.obter_id_usuario()
                    id_disp_final = id_d or 1

                    # ✅ CORREÇÃO DO ERRO DA IMAGEM: Obtendo instância real do Banco ✅
                    db_instance = self.system.model.database
                    if isinstance(db_instance, type):
                        db_instance = db_instance(self.system)
                    
                    supabase_client = db_instance.client
                    if not supabase_client:
                        return False, "Erro: Falha de conexão ao banco de dados."

                    sessao = {
                        "id_usuarios": id_usuario_final,
                        "id_dispositivos": id_disp_final,
                        "inicio_missao": inicio_missao,
                        "fim_missao": fim_missao,
                        "descricao_livre": "Upload automatizado via Painel"
                    }
                    
                    resp_sessao = supabase_client.table("sessoes_leituras").insert(sessao).execute()
                    if not resp_sessao.data:
                        return False, "Erro ao criar a sessão no banco de dados."
                    
                    id_sessao = resp_sessao.data[0]["id_sessoes_leituras"]

                    leituras_insert = []
                    for item in lista_verticalizada:
                        leituras_insert.append({
                            "id_sessoes_leituras": id_sessao,
                            "id_etiquetas_sensores": item["id_etiqueta"],
                            "valores_lidos": item["valor"],
                            "data_hora": item["horario"]
                        })

                    lote_size = 500
                    for i in range(0, len(leituras_insert), lote_size):
                        lote = leituras_insert[i:i + lote_size]
                        supabase_client.table("leituras").insert(lote).execute()

                    return True, f"Sucesso! {len(leituras_insert)} leituras salvas na sessão {id_sessao}."

                except Exception as e:
                    return False, f"Erro no processamento: {str(e)}"

            def iniciar_pipeline(e):
                if len(state["arquivos"]) != 2:
                    status_text.value = "Erro: Selecione exatamente 2 arquivos CSV."
                    status_text.color = ft.Colors.RED_400
                    self.page.update()
                    return

                status_text.value = "Lendo e identificando arquivos..."
                status_text.color = ft.Colors.YELLOW_400
                self.page.update()

                path_gases = None
                path_mov = None
                id_usuario = None
                id_dispositivo = None

                for path in state["arquivos"]:
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            linhas = [next(f) for _ in range(15)]
                            texto_cabecalho = "".join(linhas).lower()

                            if "pit stop" in texto_cabecalho or "gases" in texto_cabecalho:
                                path_gases = path
                            if "carrinho" in texto_cabecalho or "movimento" in texto_cabecalho:
                                path_mov = path

                            match_u = re.search(r"usuario:.*\(id=(\d+)\)", texto_cabecalho)
                            if match_u: id_usuario = int(match_u.group(1))

                            match_d = re.search(r"dispositivo:.*\(id=(\d+)\)", texto_cabecalho)
                            if match_d: id_dispositivo = int(match_d.group(1))
                    except Exception as ex:
                        print(f"Erro ao ler cabeçalho do arquivo {path}: {ex}")

                if not path_gases or not path_mov:
                    status_text.value = "Erro: Não foi possível identificar arquivo de Gases e Movimento."
                    status_text.color = ft.Colors.RED_400
                    self.page.update()
                    return

                status_text.value = "Processando Pandas e enviando ao Supabase..."
                self.page.update()

                sucesso, mensagem = processar_arquivos(path_gases, path_mov, id_usuario, id_dispositivo)

                if sucesso:
                    status_text.color = ft.Colors.GREEN_400
                    state["arquivos"].clear()
                    lista_arquivos_ui.controls.clear()
                else:
                    status_text.color = ft.Colors.RED_400
                    
                status_text.value = mensagem
                self.page.update()

            def on_files_selected(e):
                if e.files:
                    state["arquivos"] = [f.path for f in e.files]
                    lista_arquivos_ui.controls.clear()
                    for path in state["arquivos"]:
                        nome_arquivo = path.split('/')[-1] if '/' in path else path.split(chr(92))[-1]
                        chip_arquivo = ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.DATA_OBJECT, color=ft.Colors.CYAN_300, size=20),
                                ft.Text(nome_arquivo, color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.W_500)
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                            padding=ft.padding.symmetric(horizontal=20, vertical=10),
                            border_radius=12,
                            border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE))
                        )
                        lista_arquivos_ui.controls.append(chip_arquivo)
                        
                    status_text.value = f"{len(state['arquivos'])} arquivo(s) preparado(s) para upload."
                    status_text.color = ft.Colors.CYAN_200
                else:
                    status_text.value = "Nenhum arquivo selecionado."
                self.page.update()

            file_picker = ft.FilePicker(on_result=on_files_selected)
            self.page.overlay.append(file_picker)
            self.page.update()

            btn_selecionar = ft.ElevatedButton(
                "Selecionar 2 Arquivos CSV", icon=ft.Icons.ATTACH_FILE,
                on_click=lambda _: file_picker.pick_files(allow_multiple=True, allowed_extensions=["csv"]),
                style=ft.ButtonStyle(bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE), color=ft.Colors.WHITE, padding=ft.padding.all(20), shape=ft.RoundedRectangleBorder(radius=12))
            )

            btn_processar = ft.ElevatedButton(
                "Sincronizar e Subir Dados", icon=ft.Icons.CLOUD_UPLOAD, on_click=iniciar_pipeline,
                style=ft.ButtonStyle(bgcolor=ft.Colors.CYAN_700, color=ft.Colors.WHITE, padding=ft.padding.all(20), shape=ft.RoundedRectangleBorder(radius=12))
            )

            painel_etl = ft.Container(
                content=ft.Column(
                    [
                        titulo_row, ft.Container(height=5),
                        ft.Text("Selecione os logs de telemetria do Carrinho e do Pit Stop.\nO sistema identificará e alinhará os dados automaticamente.", color=ft.Colors.WHITE70, text_align=ft.TextAlign.CENTER, size=15),
                        ft.Container(height=30), btn_selecionar, ft.Container(height=15), lista_arquivos_ui,
                        ft.Container(height=30), btn_processar, ft.Container(height=20), status_text
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER
                ),
                width=650, padding=50, border_radius=24, bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE), border=ft.border.all(1.5, ft.Colors.with_opacity(0.15, ft.Colors.WHITE)), blur=25,
            )

            btn_voltar = ft.Container(
                content=ft.Text("VOLTAR PARA SELEÇÃO", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300),
                alignment=ft.alignment.center, width=250, height=45, border_radius=25, bgcolor="#2A2A35", ink=True,
                on_click=lambda e: trocar_tela(build_selection_view()) 
            )

            return ft.Column([
                ft.Container(height=60), ft.Row([painel_etl], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=40), ft.Row([btn_voltar], alignment=ft.MainAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)

        def build_edit_view(nome_atual, cor_atual):
            """Constrói a tela de criar/editar perfil."""
            titulo = ft.Text("Criar perfil" if nome_atual == "Novo Perfil" else "Editar perfil", size=36, weight=ft.FontWeight.W_300, color=ft.Colors.WHITE)

            avatar_preview = ft.Container(
                width=160, height=160, shape=ft.BoxShape.CIRCLE, gradient=ft.LinearGradient(colors=cor_atual),
                content=ft.Container(width=150, height=150, shape=ft.BoxShape.CIRCLE, bgcolor="#050011", content=ft.Icon(ft.Icons.PERSON_OUTLINE, size=80, color=ft.Colors.GREY_400), alignment=ft.alignment.center),
                alignment=ft.alignment.center
            )
            caixa_foto = ft.Container(content=ft.Text("Use o aplicativo para\ncarregar uma foto ou\nescolher um avatar.", text_align=ft.TextAlign.CENTER, size=12, color=ft.Colors.GREY_400), padding=20, bgcolor="#151125", border_radius=15, width=180)
            col_esquerda = ft.Column([avatar_preview, ft.Container(height=20), caixa_foto], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

            input_nome = ft.TextField(label="Nome", value="" if nome_atual == "Novo Perfil" else nome_atual, width=350, border=ft.InputBorder.UNDERLINE, color=ft.Colors.WHITE, bgcolor=ft.Colors.TRANSPARENT)

            def criar_bolinha_cor(cores): return ft.Container(width=40, height=40, shape=ft.BoxShape.CIRCLE, gradient=ft.LinearGradient(colors=cores), ink=True)

            paleta_cores = ft.Row([
                criar_bolinha_cor(["#FF007F", "#FF007F"]), criar_bolinha_cor(["#FF007F", "#7F00FF"]), criar_bolinha_cor(["#7F00FF", "#7F00FF"]), 
                criar_bolinha_cor(["#0052D4", "#7F00FF"]), criar_bolinha_cor(["#0052D4", "#6FB1FC"]), 
            ], spacing=15)
            col_direita = ft.Column([ft.Container(height=40), input_nome, ft.Container(height=40), paleta_cores], horizontal_alignment=ft.CrossAxisAlignment.START)

            btn_salvar = ft.Container(content=ft.Text("SALVAR", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE), alignment=ft.alignment.center, width=150, height=45, border_radius=25, ink=True, gradient=ft.LinearGradient(colors=["#7F00FF", "#0052D4"]), on_click=lambda e: trocar_tela(build_selection_view()))
            btn_cancelar = ft.Container(content=ft.Text("CANCELAR", weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300), alignment=ft.alignment.center, width=150, height=45, border_radius=25, bgcolor="#2A2A35", ink=True, on_click=lambda e: trocar_tela(build_selection_view()))
            botoes_acao = ft.Row([btn_salvar, btn_cancelar], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

            return ft.Column([
                ft.Container(height=60), titulo, ft.Container(height=50),
                ft.Row([col_esquerda, ft.Container(width=50), col_direita], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START),
                ft.Container(height=60), botoes_acao
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)

        # --- GERENCIADOR DE ESTADO (TROCA DE TELAS) ---

        self.main_content = ft.Container(
            content=build_selection_view(), 
            expand=True, gradient=fundo_gradiente, opacity=0, animate_opacity=800,
        )

        def trocar_tela(nova_view):
            self.main_content.opacity = 0
            self.main_content.update()
            time.sleep(0.3)
            self.main_content.content = nova_view
            self.main_content.opacity = 1
            self.main_content.update()

        self.page.add(self.main_content)
        time.sleep(0.1)
        self.main_content.opacity = 1
        self.main_content.update()