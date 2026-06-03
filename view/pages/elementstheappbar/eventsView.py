from datetime import datetime

class EventsView:
    def __init__(self, system):
        self.system = system
        self.ft = system.ft

    def _formatar_timestamp(self, timestamp_str):
        """Converte timestamp ISO para formato legível (HH:MM ou DD/MM HH:MM)"""
        if not timestamp_str:
            return "N/A"
        try:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return dt.strftime("%d/%m %H:%M")
        except:
            return str(timestamp_str)[:19]

    def _calcular_duracao(self, inicio_str, fim_str):
        """Calcula a duração entre dois timestamps em formato legível (HH:MM:SS)"""
        if not inicio_str:
            return "N/A"
        if not fim_str:
            return "Em andamento..."
        
        try:
            inicio = datetime.fromisoformat(inicio_str.replace('Z', '+00:00'))
            fim = datetime.fromisoformat(fim_str.replace('Z', '+00:00'))
            duracao = fim - inicio
            
            total_segundos = int(duracao.total_seconds())
            horas = total_segundos // 3600
            minutos = (total_segundos % 3600) // 60
            segundos = total_segundos % 60
            
            if horas > 0:
                return f"{horas}h {minutos}m {segundos}s"
            elif minutos > 0:
                return f"{minutos}m {segundos}s"
            else:
                return f"{segundos}s"
        except:
            return "N/A"

    def _carregar_sessoes(self):
        """Carrega as sessões de leitura do banco de dados."""
        try:
            id_usuario = self.system.obter_id_usuario()
            id_dispositivo = self.system.obter_id_dispositivo()
            
            if id_dispositivo:
                sessoes = self.system.model.database.listar_sessoes_leituras(id_dispositivo=id_dispositivo)
            else:
                sessoes = self.system.model.database.listar_sessoes_leituras(id_usuario=id_usuario)
            return sessoes or []
        except Exception as e:
            print(f"Erro ao carregar sessões: {e}")
            return []

    def _carregar_agendamentos(self):
        """Carrega agendamentos da tabela `agendamentos`. Filtra por dispositivo selecionado quando possível."""
        try:
            id_dispositivo = self.system.obter_id_dispositivo()
            agendamentos = self.system.model.database.listar_agendamentos(id_dispositivo=id_dispositivo) if hasattr(self.system.model.database, 'listar_agendamentos') else []
            return agendamentos or []
        except Exception as e:
            print(f"Erro ao carregar agendamentos: {e}")
            return []

    def _abrir_dialog_novo_agendamento(self, e=None):
        """Abre diálogo para registrar novo agendamento."""
        ft = self.ft
        self.input_data = ft.TextField(label="Data/Hora (ISO)", hint_text="2026-06-10T14:30:00", width=300)
        self.input_descricao = ft.TextField(label="Descrição", width=300)

        def on_submit(_e=None):
            datas = self.input_data.value
            descricao = self.input_descricao.value or ''
            id_dispositivo = self.system.obter_id_dispositivo() or None
            try:
                novo = self.system.model.database.cadastrar_agendamento(datas, id_dispositivo, descricao)
                if novo:
                    dlg.open = False
                    self.system.page.update()
                    self.system.atualizar_tela() if hasattr(self.system, 'atualizar_tela') else None
                else:
                    print('Falha ao cadastrar agendamento')
            except Exception as ex:
                print(f'Erro ao cadastrar agendamento: {ex}')

        actions = [
            ft.TextButton("Cancelar", on_click=lambda e: (setattr(dlg, 'open', False), self.system.page.update())),
            ft.ElevatedButton("Salvar", on_click=on_submit)
        ]

        dlg = ft.AlertDialog(
            title=ft.Text("Novo Agendamento", weight=ft.FontWeight.BOLD),
            content=ft.Column([self.input_data, self.input_descricao], spacing=10),
            actions=actions,
            modal=True
        )
        self.system.page.dialog = dlg
        dlg.open = True
        self.system.page.update()

    def _criar_linhas_tabela(self, sessoes):
        """Cria as linhas da tabela a partir das sessões de leitura."""
        linhas = []
        
        if not sessoes:
            linhas.append(
                self.ft.DataRow(cells=[
                    self.ft.DataCell(self.ft.Text("--:--", color=self.ft.Colors.GREY_500, size=11)),
                    self.ft.DataCell(self.ft.Text("--:--", color=self.ft.Colors.GREY_500, size=11)),
                    self.ft.DataCell(self.ft.Text("--:--", color=self.ft.Colors.GREY_500, size=11)),
                    self.ft.DataCell(self.ft.Text("N/A", color=self.ft.Colors.GREY_500, size=11)),
                    self.ft.DataCell(self.ft.Text("Nenhuma sessão registrada", color=self.ft.Colors.GREY_500, size=11)),
                    self.ft.DataCell(self.ft.Text("N/A", color=self.ft.Colors.GREY_500, size=11)),
                    self.ft.DataCell(self.ft.Text("Aguardando...", color=self.ft.Colors.AMBER_500, size=11, weight="bold")),
                ])
            )
        else:
            for sessao in sessoes:
                id_dispositivo = str(sessao.get('id_dispositivos', 'N/A'))
                data_upload = self._formatar_timestamp(sessao.get('datas_uploads'))
                inicio = self._formatar_timestamp(sessao.get('inicio_missao'))
                fim = self._formatar_timestamp(sessao.get('fim_missao')) if sessao.get('fim_missao') else "--:--"
                duracao = self._calcular_duracao(sessao.get('inicio_missao'), sessao.get('fim_missao'))
                descricao = sessao.get('descricao_livre', 'Sem descrição')
                if len(descricao) > 25:
                    descricao = descricao[:22] + "..."
                
                if sessao.get('fim_missao'):
                    status = "✓ Finalizada"
                    status_color = self.ft.Colors.GREEN_400
                else:
                    status = "⏱ Em Andamento"
                    status_color = self.ft.Colors.BLUE_400
                
                linhas.append(
                    self.ft.DataRow(cells=[
                        self.ft.DataCell(self.ft.Text(data_upload, color=self.ft.Colors.WHITE70, size=11)),
                        self.ft.DataCell(self.ft.Text(inicio, color=self.ft.Colors.WHITE70, size=11)),
                        self.ft.DataCell(self.ft.Text(fim, color=self.ft.Colors.WHITE70, size=11)),
                        self.ft.DataCell(self.ft.Text(duracao, color=self.ft.Colors.CYAN_400, size=11, weight="bold")),
                        self.ft.DataCell(self.ft.Text(descricao, color=self.ft.Colors.WHITE70, size=11)),
                        self.ft.DataCell(self.ft.Text(id_dispositivo, color=self.ft.Colors.BLUE_200, size=11)),
                        self.ft.DataCell(self.ft.Text(status, color=status_color, size=11, weight="bold")),
                    ])
                )
        return linhas

    def render(self):
        # 1. Carrega os dados antes para alimentar os contadores do topo
        sessoes = self._carregar_sessoes()
        total_sessoes = len(sessoes)
        em_andamento = sum(1 for s in sessoes if not s.get('fim_missao'))
        
        BG_CARD = "#111827"
        BORDER_COLOR = "#1f2937"

        return self.ft.Column([
            # CABEÇALHO DA TELA
            self.ft.Row([
                self.ft.Column([
                    self.ft.Row([
                        self.ft.Icon(self.ft.Icons.HISTORY_TOGGLE_OFF_ROUNDED, color=self.ft.Colors.CYAN_400, size=32),
                        self.ft.Text("Histórico de Missões", size=28, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
                    ]),
                    self.ft.Text("Gerenciamento e auditoria de sessões salvas no Supabase", color=self.ft.Colors.GREY_400, size=14),
                ]),
                self.ft.IconButton(
                    icon=self.ft.Icons.REFRESH_ROUNDED, 
                    icon_color=self.ft.Colors.CYAN_400, 
                    tooltip="Atualizar Logs",
                    on_click=lambda _: self.system.atualizar_tela() 
                )
            ], alignment=self.ft.MainAxisAlignment.SPACE_BETWEEN),
            
            self.ft.Container(height=15),
            
            # 2. CARDS RESUMIDOS (KPIs)
            self.ft.ResponsiveRow([
                self.ft.Container(
                    col={"sm": 6, "md": 4},
                    bgcolor=BG_CARD, padding=15, border_radius=10, border=self.ft.border.all(1, BORDER_COLOR),
                    content=self.ft.Row([
                        self.ft.Icon(self.ft.Icons.PLAY_CIRCLE_OUTLINE, color=self.ft.Colors.BLUE_400, size=30),
                        self.ft.Column([
                            self.ft.Text("Em Execução", color=self.ft.Colors.GREY_400, size=11),
                            self.ft.Text(f"{em_andamento} ativa(s)", size=18, weight="bold", color=self.ft.Colors.WHITE)
                        ], spacing=2)
                    ])
                ),
                self.ft.Container(
                    col={"sm": 6, "md": 4},
                    bgcolor=BG_CARD, padding=15, border_radius=10, border=self.ft.border.all(1, BORDER_COLOR),
                    content=self.ft.Row([
                        self.ft.Icon(self.ft.Icons.ASSESSMENT_ROUNDED, color=self.ft.Colors.GREEN_400, size=30),
                        self.ft.Column([
                            self.ft.Text("Total de Corridas", color=self.ft.Colors.GREY_400, size=11),
                            self.ft.Text(f"{total_sessoes} registradas", size=18, weight="bold", color=self.ft.Colors.WHITE)
                        ], spacing=2)
                    ])
                ),
            ], spacing=15),
            
            self.ft.Container(height=15),
            
            # 3. TABELA COM SUPORTE A ROLAGEM RESPONSIVA
            self.ft.Text("Registros de Telemetria", size=16, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
            self.ft.Container(height=5),
            
            # O ListView com expand=True já substitui o Expanded com segurança aqui
            self.ft.ListView(
                expand=True,
                controls=[
                    self.ft.Row(
                        scroll=self.ft.ScrollMode.ALWAYS,
                        controls=[
                            self.ft.DataTable(
                                border=self.ft.border.all(1, BORDER_COLOR),
                                border_radius=10,
                                heading_row_color="#1f2937",
                                column_spacing=24,
                                columns=[
                                    self.ft.DataColumn(self.ft.Text("Data Upload", color=self.ft.Colors.CYAN_400, size=12, weight="bold")),
                                    self.ft.DataColumn(self.ft.Text("Início", color=self.ft.Colors.WHITE, size=12)),
                                    self.ft.DataColumn(self.ft.Text("Fim", color=self.ft.Colors.WHITE, size=12)),
                                    self.ft.DataColumn(self.ft.Text("Duração", color=self.ft.Colors.WHITE, size=12)),
                                    self.ft.DataColumn(self.ft.Text("Descrição", color=self.ft.Colors.WHITE, size=12)),
                                    self.ft.DataColumn(self.ft.Text("Dispositivo", color=self.ft.Colors.WHITE, size=12)),
                                    self.ft.DataColumn(self.ft.Text("Status", color=self.ft.Colors.WHITE, size=12)),
                                ],
                                rows=self._criar_linhas_tabela(sessoes),
                                bgcolor=BG_CARD,
                            )
                        ]
                    )
                ]
            )
        ], expand=True)