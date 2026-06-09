import flet as ft
import os


class UploadDataView:
    def __init__(self, system):
        self.system = system
        self.page = system.page
        self.ft = system.ft
        self.selected_files = []

    def render(self):
        ft = self.ft

        # --- COMPONENTES DE TEXTO (CABEÇALHO) ---
        title = ft.Text(
            "Enviar Leituras", 
            size=32, 
            weight=ft.FontWeight.BOLD, 
            color=ft.Colors.WHITE
        )
        status = ft.Text(
            "Selecione os arquivos de telemetria dos Arduinos e valide os parâmetros abaixo.", 
            color=ft.Colors.GREY_400,
            size=14
        )

        status_message = ft.Text(
            "", 
            color=ft.Colors.CYAN_200,
            size=14
        )

        def go_home(e):
            self.system.view.animate.animacaoPagina.animar_tela(
                self.system,
                self.system.view.page.home
            )

        back_btn = ft.TextButton(
            "← Voltar ao início",
            on_click=go_home
        )

        # Caixa onde os arquivos selecionados serão mostrados como Chips decorados
        arquivos_box = ft.Column([], spacing=8)

        def on_files_selected(e: ft.FilePickerResultEvent):
            if e.files:
                self.selected_files = [f.path for f in e.files]
                arquivos_box.controls.clear()
                for p in self.selected_files:
                    # Extrai apenas o nome do arquivo para não quebrar o layout com caminhos gigantes
                    nome_arquivo = os.path.basename(p)
                    arquivos_box.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.INSERT_DRIVE_FILE_ROUNDED, color=ft.Colors.BLUE_400, size=18),
                                ft.Text(nome_arquivo, color=ft.Colors.WHITE, size=13, weight=ft.FontWeight.W_500),
                            ], tight=True),
                            bgcolor="#0D1117",
                            padding=ft.padding.symmetric(vertical=6, horizontal=12),
                            border_radius=8,
                            border=ft.border.all(1, "#30363D")
                        )
                    )
            else:
                arquivos_box.controls.append(
                    ft.Text("Nenhum arquivo selecionado", color=ft.Colors.GREY_600, italic=True, size=13)
                )
            self.page.update()

        file_picker = ft.FilePicker(on_result=on_files_selected)
        self.page.overlay.append(file_picker)

        # Botão de seleção estilizado como zona de upload
        btn_select = ft.OutlinedButton(
            "Procurar Arquivos CSV",
            icon=ft.Icons.FOLDER_OPEN_ROUNDED,
            on_click=lambda _: file_picker.pick_files(
                allow_multiple=True,
                allowed_extensions=["csv"]
            )
        )

        # --- CAMPOS DE ENTRADA (INPUTS) ---
        default_carr = ""
        try:
            default_carr = str(self.system.obter_id_dispositivo() or "")
        except Exception:
            default_carr = ""

        input_carrinho = ft.TextField(
            label="ID do Carrinho", 
            value=default_carr, 
            prefix_icon=ft.Icons.ELECTRIC_CAR_ROUNDED,
            border_color="#30363D",
            focused_border_color=ft.Colors.BLUE_400,
            border_radius=8,
            text_size=14,
            height=48
        )
        
        input_usuario = ft.TextField(
            label="ID do Usuário", 
            value=str(self.system.obter_id_usuario() or ""), 
            prefix_icon=ft.Icons.PERSON_ROUNDED,
            border_color="#30363D",
            focused_border_color=ft.Colors.BLUE_400,
            border_radius=8,
            text_size=14,
            height=48
        )

        # --- LOGICA DE ENVIO ---
        def process_and_send(e):
            if not self.selected_files or len(self.selected_files) < 2:
                status_message.value = "Selecione dois arquivos: gases e movimento."
                self.page.snack_bar = ft.SnackBar(ft.Text("Selecione dois arquivos CSV."))
                self.page.snack_bar.open = True
                self.page.update()
                print("UploadDataView: menos de dois arquivos selecionados")
                return

            if len(self.selected_files) > 2:
                status_message.value = "Selecione apenas dois arquivos: gases e movimento."
                self.page.snack_bar = ft.SnackBar(ft.Text("Remova arquivos extras e selecione somente 2 CSVs."))
                self.page.snack_bar.open = True
                self.page.update()
                print("UploadDataView: mais de dois arquivos selecionados")
                return

            status_message.value = "Enviando dados via pipeline..."
            self.page.update()
            print("UploadDataView: iniciando importação via pipeline")

            try:
                files = self.selected_files[:2]
            except Exception as ex:
                status_message.value = f"Erro ao validar arquivos: {ex}"
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao validar arquivos: {ex}"))
                self.page.snack_bar.open = True
                self.page.update()
                print(f"UploadDataView: falha ao validar arquivos: {ex}")
                return

            try:
                id_usuario = int(input_usuario.value) if input_usuario.value else None
                id_dispositivo = int(input_carrinho.value) if input_carrinho.value else None

                if id_usuario is None or id_dispositivo is None:
                    status_message.value = "Preencha ID do usuário e do carrinho."
                    self.page.snack_bar = ft.SnackBar(ft.Text("ID do usuário ou do carrinho não informado."))
                    self.page.snack_bar.open = True
                    self.page.update()
                    return

                db = getattr(self.system.model, 'database', None)
                if not db or not hasattr(db, 'importar_telemetria_supabase'):
                    status_message.value = "Erro: função de importação não disponível."
                    self.page.snack_bar = ft.SnackBar(ft.Text("Função de importação não encontrada."))
                    self.page.snack_bar.open = True
                    self.page.update()
                    print("UploadDataView: importar_telemetria_supabase indisponível")
                    return

                sucesso = db.importar_telemetria_supabase(
                    files[0],
                    files[1],
                    id_usuario,
                    id_dispositivo,
                    descricao="Importação via app"
                )

                if sucesso:
                    status_message.value = "Upload concluído com sucesso."
                    self.page.snack_bar = ft.SnackBar(ft.Text("Dados enviados com sucesso."))
                    self.page.snack_bar.open = True
                    self.page.update()
                    print("UploadDataView: upload via database concluído")
                    return
                else:
                    status_message.value = "Falha ao importar dados no banco."
                    self.page.snack_bar = ft.SnackBar(ft.Text("Falha na importação de telemetria."))
                    self.page.snack_bar.open = True
                    self.page.update()
                    print("UploadDataView: importação via database retornou falso")
                    return

            except Exception as ex:
                status_message.value = f"Erro processamento: {ex}"
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Erro processamento: {ex}"))
                self.page.snack_bar.open = True
                self.page.update()
                print(f"UploadDataView: erro de processamento: {ex}")
                return

        # Botão de Enviar Maciço e Chamativo
        submit_btn = ft.ElevatedButton(
            "Processar & Sincronizar Dados",
            icon=ft.Icons.CLOUD_UPLOAD_ROUNDED,
            on_click=process_and_send,
            bgcolor=ft.Colors.BLUE_500,
            color=ft.Colors.WHITE,
            expand=True
        )

        # Botão para voltar à página inicial após o upload
        go_home_btn = ft.TextButton(
            "Voltar ao Início",
            on_click=go_home,
            style=ft.ButtonStyle(
                overlay_color=ft.MaterialStateProperty.all("#062D5F")
            )
        )

        # --- ESTRUTURA VISUAL DA TELA (LAYOUT) ---
        content = ft.Column([
            # Cabeçalho da página e botão de retorno
            ft.Row([back_btn], alignment=ft.MainAxisAlignment.START),
            ft.Container(height=6),
            ft.Column([title, status, status_message], spacing=4),
            ft.Container(height=16),

            # Grid Responsivo dividindo Parâmetros de Arquivos
            ft.ResponsiveRow([
                # Coluna Esquerda: Dados de Configuração
                ft.Column([
                    ft.Text("PARÂMETROS DE SESSÃO", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Container(input_carrinho, expand=True),
                                ft.Container(input_usuario, expand=True),
                            ], spacing=12),
                        ], spacing=16),
                        bgcolor="#161B22",
                        border=ft.border.all(1, "#30363D"),
                        border_radius=12,
                        padding=20,
                    )
                ], col={"sm": 12, "md": 6}),

                # Coluna Direita: Caixa de Arquivos
                ft.Column([
                    ft.Text("ARQUIVOS FONTE", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                btn_select,
                                ft.Text("Máx: 2 arquivos (.csv)", color=ft.Colors.GREY_500, size=12)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Divider(height=1, color="#30363D"),
                            arquivos_box,
                        ], spacing=16, alignment=ft.MainAxisAlignment.CENTER),
                        bgcolor="#161B22",
                        border=ft.border.all(1, "#30363D"),
                        border_radius=12,
                        padding=20,
                        height=175
                    )
                ], col={"sm": 12, "md": 6}),
            ], run_spacing=16),

            ft.Container(height=16),
            
            # Botões de ação
            ft.Row([submit_btn], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([go_home_btn], alignment=ft.MainAxisAlignment.CENTER),
            
        ], expand=True, scroll=ft.ScrollMode.AUTO, spacing=0)

        self.page.clean()
        # Retorna a view envelopada em um Container elegante com espaçamento geral
        self.page.add(ft.Container(content, expand=True, padding=24))