import pandas as pd
import math
import re
from datetime import datetime

class SettingView:
    """Tela de Sincronização de Telemetria."""

    def __init__(self, system, on_back_callback):
        self.system = system
        self.ft = self.system.ft
        self.voltar_para_selecao = on_back_callback
        
        # Variáveis de estado
        self.arquivos_selecionados = []
        
        # Mapeamento de Etiquetas
        self.MAPEAMENTO_ETIQUETAS = {
            "mq2_ppm": 1, "mq2_lel_pct": 2, "mq3_ppm": 3, "mq3_mgl": 4,
            "mq7_ppm": 5, "mq7_cohb_pct": 6, "tempo_volta_s": 7,
            "dist_total_m": 8, "frente_cm": 9, "direita_cm": 10,
            "esquerda_cm": 11, "traseira_cm": 12
        }

    def render(self):
        # Limpa a tela
        self.system.page.clean()
        self.system.page.padding = 0

        # Fundo global da tela 
        fundo_gradiente = self.ft.RadialGradient(
            colors=["#2A0A4A", "#050011"], 
            center=self.ft.alignment.top_center, 
            radius=1.5
        )

        # --- COMPONENTES DE UI (Sincronização) ---
        titulo_row = self.ft.Row(
            [
                self.ft.Icon(self.ft.Icons.SYNC_ALT, color=self.ft.Colors.CYAN_400, size=32),
                self.ft.Text("Sincronização de Telemetria", size=28, weight=self.ft.FontWeight.W_400, color=self.ft.Colors.WHITE)
            ],
            alignment=self.ft.MainAxisAlignment.CENTER
        )
        
        status_text = self.ft.Text("Aguardando arquivos...", color=self.ft.Colors.GREY_400, size=14, weight=self.ft.FontWeight.W_500)
        lista_arquivos_ui = self.ft.Column(spacing=10, horizontal_alignment=self.ft.CrossAxisAlignment.CENTER)
        
        # --- LÓGICA DE PROCESSAMENTO (ETL) ---
        def processar_arquivos(path_gases, path_movimento, id_usuario_cabecalho, id_dispositivo_cabecalho):
            try:
                # 1. Carrega CSVs ignorando o cabeçalho
                df_gases = pd.read_csv(path_gases, comment='#')
                df_movimento = pd.read_csv(path_movimento, comment='#')

                # 2. Limpeza e formatação temporal
                df_gases['horario'] = pd.to_datetime(df_gases['horario'], errors='coerce')
                df_gases.sort_values('horario', inplace=True)

                df_movimento['horario'] = pd.to_datetime(df_movimento['horario'], errors='coerce')
                colunas_numericas = ['tempo_volta_s', 'dist_total_m', 'frente_cm', 'direita_cm', 'esquerda_cm', 'traseira_cm']
                for col in colunas_numericas:
                    if col in df_movimento.columns:
                        df_movimento[col] = pd.to_numeric(df_movimento[col], errors='coerce').fillna(0)
                df_movimento.sort_values('horario', inplace=True)

                # 3. Sincronização por proximidade (5 segundos)
                df_sync = pd.merge_asof(
                    left=df_gases, right=df_movimento,
                    on='horario', direction='nearest',
                    tolerance=pd.Timedelta(seconds=5), suffixes=('_gases', '_mov')
                )
                df_sync = df_sync.where(pd.notnull(df_sync), None)

                # 4. Verticalização (EAV)
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

                    for chave, id_tag in self.MAPEAMENTO_ETIQUETAS.items():
                        valor = registro.get(chave)
                        if valor is not None and not (isinstance(valor, float) and math.isnan(valor)):
                            lista_verticalizada.append({
                                "horario": horario_iso,
                                "id_etiqueta": id_tag,
                                "valor": float(valor)
                            })

                if not lista_verticalizada:
                    return False, "Nenhum dado válido para sincronizar."

                # 5. Descobrir Início e Fim
                horarios_validos.sort()
                inicio_missao = horarios_validos[0]
                fim_missao = horarios_validos[-1]

                # 6. Fallback de IDs
                id_usuario_final = id_usuario_cabecalho or self.system.model.usuario_model.obter_id_usuario()
                id_disp_final = id_dispositivo_cabecalho or 1

                # ✅ TRAVA DE SEGURANÇA CONTRA ERRO DE INSTÂNCIA DO BANCO
                db = self.system.model.database
                if isinstance(db, type):
                    db = db(self.system)
                
                supabase_client = db.client

                # 7. Salvar no Supabase (Sessão)
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

                # 8. Salvar no Supabase (Leituras em Lote)
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
            if len(self.arquivos_selecionados) != 2:
                status_text.value = "Erro: Selecione exatamente 2 arquivos CSV."
                status_text.color = self.ft.Colors.RED_400
                self.system.page.update()
                return

            status_text.value = "Lendo e identificando arquivos..."
            status_text.color = self.ft.Colors.YELLOW_400
            self.system.page.update()

            path_gases = None
            path_mov = None
            id_usuario = None
            id_dispositivo = None

            for path in self.arquivos_selecionados:
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
                status_text.color = self.ft.Colors.RED_400
                self.system.page.update()
                return

            status_text.value = "Processando Pandas e enviando ao Supabase..."
            self.system.page.update()

            sucesso, mensagem = processar_arquivos(path_gases, path_mov, id_usuario, id_dispositivo)

            if sucesso:
                status_text.color = self.ft.Colors.GREEN_400
                self.arquivos_selecionados.clear()
                lista_arquivos_ui.controls.clear()
            else:
                status_text.color = self.ft.Colors.RED_400
                
            status_text.value = mensagem
            self.system.page.update()

        # --- SELETOR DE ARQUIVOS (FILE PICKER) COM UI APRIMORADA ---
        def on_files_selected(e):
            if e.files:
                self.arquivos_selecionados = [f.path for f in e.files]
                lista_arquivos_ui.controls.clear()
                for path in self.arquivos_selecionados:
                    nome_arquivo = path.split('/')[-1] if '/' in path else path.split(chr(92))[-1]
                    
                    # Chip elegante para os arquivos selecionados
                    chip_arquivo = self.ft.Container(
                        content=self.ft.Row([
                            self.ft.Icon(self.ft.Icons.DATA_OBJECT, color=self.ft.Colors.CYAN_300, size=20),
                            self.ft.Text(nome_arquivo, color=self.ft.Colors.WHITE, size=14, weight=self.ft.FontWeight.W_500)
                        ], alignment=self.ft.MainAxisAlignment.CENTER),
                        bgcolor=self.ft.Colors.with_opacity(0.1, self.ft.Colors.WHITE),
                        padding=self.ft.padding.symmetric(horizontal=20, vertical=10),
                        border_radius=12,
                        border=self.ft.border.all(1, self.ft.Colors.with_opacity(0.2, self.ft.Colors.WHITE))
                    )
                    lista_arquivos_ui.controls.append(chip_arquivo)
                    
                status_text.value = f"{len(self.arquivos_selecionados)} arquivo(s) preparado(s) para upload."
                status_text.color = self.ft.Colors.CYAN_200
            else:
                status_text.value = "Nenhum arquivo selecionado."
            self.system.page.update()

        file_picker = self.ft.FilePicker(on_result=on_files_selected)
        self.system.page.overlay.append(file_picker)

        # --- BOTÕES DE AÇÃO ---
        btn_selecionar = self.ft.ElevatedButton(
            "Selecionar 2 Arquivos CSV",
            icon=self.ft.Icons.ATTACH_FILE,
            on_click=lambda _: file_picker.pick_files(allow_multiple=True, allowed_extensions=["csv"]),
            style=self.ft.ButtonStyle(
                bgcolor=self.ft.Colors.with_opacity(0.15, self.ft.Colors.WHITE), 
                color=self.ft.Colors.WHITE,
                padding=self.ft.padding.all(20),
                shape=self.ft.RoundedRectangleBorder(radius=12)
            )
        )

        btn_processar = self.ft.ElevatedButton(
            "Sincronizar e Subir Dados",
            icon=self.ft.Icons.CLOUD_UPLOAD,
            on_click=iniciar_pipeline,
            style=self.ft.ButtonStyle(
                bgcolor=self.ft.Colors.CYAN_700, 
                color=self.ft.Colors.WHITE,
                padding=self.ft.padding.all(20),
                shape=self.ft.RoundedRectangleBorder(radius=12)
            )
        )

        # --- CARTÃO CENTRAL (ETL) ---
        painel_etl = self.ft.Container(
            content=self.ft.Column(
                [
                    titulo_row,
                    self.ft.Container(height=5),
                    self.ft.Text(
                        "Selecione os logs de telemetria do Carrinho e do Pit Stop.\nO sistema identificará e alinhará os dados automaticamente.", 
                        color=self.ft.Colors.WHITE70, text_align=self.ft.TextAlign.CENTER, size=15
                    ),
                    self.ft.Container(height=30),
                    btn_selecionar,
                    self.ft.Container(height=15),
                    lista_arquivos_ui,
                    self.ft.Container(height=30),
                    btn_processar,
                    self.ft.Container(height=20),
                    status_text
                ],
                horizontal_alignment=self.ft.CrossAxisAlignment.CENTER,
                alignment=self.ft.MainAxisAlignment.CENTER
            ),
            width=650,
            padding=50,
            border_radius=24,
            bgcolor=self.ft.Colors.with_opacity(0.05, self.ft.Colors.WHITE), 
            border=self.ft.border.all(1.5, self.ft.Colors.with_opacity(0.15, self.ft.Colors.WHITE)), 
            blur=25,
            shadow=self.ft.BoxShadow(blur_radius=60, color=self.ft.Colors.with_opacity(0.15, self.ft.Colors.CYAN_900))
        )

        # --- TOPBAR ---
        btn_voltar = self.ft.IconButton(
            icon=self.ft.Icons.ARROW_BACK,
            icon_color=self.ft.Colors.WHITE,
            icon_size=30,
            tooltip="Voltar",
            on_click=lambda e: self.voltar_para_selecao()
        )
        
        topbar = self.ft.Container(
            content=self.ft.Row([btn_voltar], alignment=self.ft.MainAxisAlignment.START),
            padding=20
        )

        # --- LAYOUT PRINCIPAL ---
        main_layout = self.ft.Container(
            content=self.ft.Column(
                [
                    topbar,
                    self.ft.Container(height=40),
                    self.ft.Row([painel_etl], alignment=self.ft.MainAxisAlignment.CENTER)
                ],
                horizontal_alignment=self.ft.CrossAxisAlignment.CENTER
            ),
            expand=True,
            gradient=fundo_gradiente,
            opacity=0,
            animate_opacity=800
        )

        self.system.page.add(main_layout)
        self.system.time.sleep(0.1)
        main_layout.opacity = 1
        main_layout.update()