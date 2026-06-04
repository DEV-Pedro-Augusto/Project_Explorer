from datetime import datetime

class AgendamentoTesteView:
    def __init__(self, system):
        self.system = system
        self.ft = system.ft
        self.on_back = self.system.view.page.home

    def _carregar_agendamentos(self):
        try:
            id_dispositivo = self.system.obter_id_dispositivo()
            agendamentos = self.system.model.database.listar_agendamentos(id_dispositivo=id_dispositivo)
            return agendamentos or []
        except Exception as e:
            print(f"Erro ao carregar agendamentos: {e}")
            return []

    def _formatar_timestamp(self, timestamp_str):
        if not timestamp_str:
            return "N/A"
        try:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return dt.strftime("%d/%m/%Y %H:%M")
        except Exception:
            return str(timestamp_str)[:16]

    def _salvar_agendamento(self, e=None):
        data = self.input_date_text.value
        hora = self.input_time.value or "00:00"
        titulo = (self.input_titulo.value or "").strip()
        descricao = (self.input_descricao.value or "").strip()
        dispositivo = self.system.obter_id_dispositivo()
        
        if dispositivo is None and self.input_dispositivo:
            try:
                dispositivo = int(self.input_dispositivo.value)
            except Exception:
                dispositivo = None

        if not data or data == "Nenhuma selecionada":
            self._mostrar_alerta("Preencha uma data para o agendamento.")
            return

        if not hora or len(hora.split(':')) != 2:
            self._mostrar_alerta("Informe a hora no formato HH:MM.")
            return

        try:
            data_hora = f"{data}T{hora}:00"
            if titulo:
                descricao_livre = f"{titulo};{descricao}"
            else:
                descricao_livre = descricao

            id_usuario = self.system.obter_id_usuario()
            agendamento = self.system.model.database.cadastrar_agendamento(
                data_hora_agendamento=data_hora,
                id_dispositivo=dispositivo,
                descricao_livre=descricao_livre,
                id_usuario=id_usuario
            )

            if agendamento:
                self._mostrar_alerta("Agendamento criado com sucesso!", sucesso=True)
                self.render()
            else:
                self._mostrar_alerta("Falha ao cadastrar agendamento. Revise os campos e tente novamente.")
        except Exception as ex:
            self._mostrar_alerta(f"Erro ao cadastrar agendamento: {ex}")

    def _mostrar_alerta(self, mensagem, sucesso=False):
        dlg = self.ft.AlertDialog(
            title=self.ft.Text(
                "SISTEMA // SUCESSO" if sucesso else "SISTEMA // ATENÇÃO",
                weight=self.ft.FontWeight.BOLD,
                size=16,
                color=self.ft.Colors.GREEN_400 if sucesso else self.ft.Colors.RED_400
            ),
            content=self.ft.Text(mensagem, size=14, color=self.ft.Colors.WHITE),
            actions=[
                self.ft.TextButton("OK", on_click=lambda e: self._fechar_dialog(dlg))
            ],
            bgcolor="#111827",
        )
        self.system.page.dialog = dlg
        dlg.open = True
        self.system.page.update()

    def _fechar_dialog(self, dlg):
        dlg.open = False
        self.system.page.update()

    def _voltar(self, e=None):
        self.on_back(self.system).render()

    def _abrir_calendario(self, e):
        self.date_picker.pick_date()

    def _ao_mudar_data(self, e):
        if self.date_picker.value:
            self.input_date_text.value = self.date_picker.value.strftime("%Y-%m-%d")
            self.input_date_text.update()

    def render(self):
        ft = self.ft
        self.system.page.clean()
        self.system.page.padding = 30
        self.system.page.bgcolor = "#080E1A"  # Dark industrial background

        # Cores do Tema Técnico
        COLOR_BORDER = "#1F2937"
        COLOR_SURFACE = "#111827"
        ACCENT_CYAN = ft.Colors.CYAN_400
        ACCENT_BLUE = ft.Colors.BLUE_500

        # Instanciação Correta do Componente Oculto de Data do Flet
        self.date_picker = ft.DatePicker(
            first_date=datetime(2025, 1, 1),
            last_date=datetime(2030, 12, 31),
            on_change=self._ao_mudar_data
        )
        self.system.page.overlay.append(self.date_picker)

        # Carrega os agendamentos salvos
        agendamentos = self._carregar_agendamentos()
        lista_agendamentos = []
        
        for ag in agendamentos:
            data = ag.get('data_hora_agendamento') or ag.get('datas_agendamentos') or ag.get('data')
            id_disp = ag.get('id_dispositivos', 'N/A')
            desc_completa = ag.get('descricao_livre', '-')
            
            # Divide título e descrição baseados no separador padrão do sistema
            titulo_item = desc_completa.split(';', 1)[0] if ';' in desc_completa else "Rotina Operacional"
            desc_item = desc_completa.split(';', 1)[1] if ';' in desc_completa else desc_completa

            lista_agendamentos.append(
                ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.SUBDIRECTORY_ARROW_RIGHT_ROUNDED, color=ACCENT_CYAN, size=14),
                                ft.Text(titulo_item, color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.BOLD),
                            ], spacing=5),
                            ft.Container(height=2),
                            ft.Text(desc_item, color=ft.Colors.GREY_400, size=12, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                        ], expand=True),
                        ft.Column([
                            ft.Container(
                                content=ft.Text(self._formatar_timestamp(data), color=ACCENT_CYAN, size=11, weight=ft.FontWeight.W_600),
                                bgcolor="#1E293B",
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=5
                            ),
                            ft.Text(f"TARGET ID: {id_disp}", color=ft.Colors.GREY_500, size=10, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.RIGHT)
                        ], horizontal_alignment=ft.CrossAxisAlignment.END, alignment=ft.MainAxisAlignment.CENTER)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=16,
                    bgcolor="#141E30",
                    border=ft.border.all(1, "#243B55"),
                    border_radius=8,
                    on_click=lambda e, ag=ag: self._preencher_agendamento(ag)
                )
            )

        # Campos do Formulário Técnico
        self.input_date_text = ft.TextField(
            label="Data de Execução (AAAA-MM-DD)", 
            value=datetime.now().strftime("%Y-%m-%d"), 
            read_only=True,
            expand=True,
            border_color=COLOR_BORDER
        )
        
        self.input_time = ft.TextField(
            label="Horário (HH:MM)", 
            width=130, 
            value=datetime.now().strftime("%H:%M"),
            border_color=COLOR_BORDER,
            text_align=ft.TextAlign.CENTER
        )
        
        self.input_titulo = ft.TextField(
            label="Identificador do Teste / Título",
        )