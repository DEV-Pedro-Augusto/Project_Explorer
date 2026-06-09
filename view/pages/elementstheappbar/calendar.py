from datetime import datetime, timezone

class CalendarView:
    def __init__(self, system):
        self.system = system
        self.ft = system.ft
        self.agendamentos_table = None

    def _formatar_timestamp(self, timestamp_str):
        if not timestamp_str:
            return "N/A"
        try:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return dt.strftime("%d/%m/%Y %H:%M")
        except Exception:
            return str(timestamp_str)[:16]

    def _carregar_agendamentos(self):
        try:
            id_dispositivo = self.system.obter_id_dispositivo()
            agendamentos = self.system.model.database.listar_agendamentos(id_dispositivo=id_dispositivo)
            return agendamentos or []
        except Exception as e:
            print(f"Erro ao carregar agendamentos: {e}")
            return []

    def _obter_proximo_evento(self, agendamentos):
        """Encontra o agendamento futuro mais próximo do horário atual."""
        agora = datetime.now(timezone.utc)
        proximo_evento = None
        menor_diferenca = None

        for ag in agendamentos:
            data_str = ag.get('data_hora_agendamento') or ag.get('data_hora_hendamento') or ag.get('datas_agendamentos')
            if not data_str:
                continue
            try:
                # Normaliza string e converte para objeto datetime com timezone
                dt_evento = datetime.fromisoformat(data_str.replace('Z', '+00:00'))
                if dt_evento.tzinfo is None:
                    dt_evento = dt_evento.replace(tzinfo=timezone.utc)
                
                # Se o evento ainda vai acontecer
                if dt_evento > agora:
                    diferenca = dt_evento - agora
                    if menor_diferenca is None or diferenca < menor_diferenca:
                        menor_diferenca = diferenca
                        proximo_evento = {
                            "dados": ag,
                            "datetime": dt_evento,
                            "tempo_restante": diferenca
                        }
            except Exception:
                continue

        return proximo_evento

    def _build_agendamentos_rows(self, agendamentos):
        ft = self.ft
        if not agendamentos:
            return [
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("Nenhum agendamento encontrado", color=ft.Colors.GREY_500, size=12, italic=True)),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                ])
            ]

        rows = []
        for ag in agendamentos:
            data_banco = ag.get('data_hora_agendamento') or ag.get('data_hora_hendamento') or ag.get('datas_agendamentos')
            dispositivo = ag.get('id_dispositivos', 'N/A')
            descricao = ag.get('descricao_livre', '-')

            rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(self._formatar_timestamp(data_banco), color=ft.Colors.CYAN_300, weight=ft.FontWeight.W_600, size=12),
                            padding=ft.padding.all(4)
                        )
                    ),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(f"ID: {dispositivo}", color=ft.Colors.WHITE10, size=12),
                            padding=ft.padding.all(4)
                        )
                    ),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(descricao, color=ft.Colors.GREY_300, size=12),
                            padding=ft.padding.all(4)
                        )
                    ),
                ])
            )
        return rows

    def _abrir_dialog_novo_agendamento(self, e=None):
        ft = self.ft
        id_dispositivo = self.system.obter_id_dispositivo()
        
        data_atual_exemplo = datetime.now().strftime("%Y-%m-%dT%H:%M:00")
        self.input_data = ft.TextField(
            label="Data/Hora do Agendamento", 
            value=data_atual_exemplo, 
            hint_text="AAAA-MM-DDTHH:MM:SS", 
            border_color=ft.Colors.BLUE_400,
            width=300
        )
        self.input_titulo = ft.TextField(label="Título do Agendamento", width=300)
        self.input_descricao = ft.TextField(label="Descrição Livre", width=300)
        self.input_dispositivo = None

        if id_dispositivo is None:
            self.input_dispositivo = ft.TextField(label="ID do Dispositivo Target", hint_text="Digite o ID numérico", width=300)

        def on_submit(_e=None):
            datas = self.input_data.value
            titulo = (self.input_titulo.value or '').strip()
            descricao = (self.input_descricao.value or '').strip()
            # concatena título e descrição usando ';' conforme especificado
            descricao_completa = f"{titulo};{descricao}" if titulo else descricao

            dispositivo = id_dispositivo
            
            if dispositivo is None:
                dispositivo_text = self.input_dispositivo.value if self.input_dispositivo else None
                if not dispositivo_text:
                    return
                try:
                    dispositivo = int(dispositivo_text)
                except ValueError:
                    return

            id_usuario = self.system.obter_id_usuario()
            try:
                novo = self.system.model.database.cadastrar_agendamento(datas, dispositivo, descricao_completa, id_usuario=id_usuario)
                if novo:
                    dlg.open = False
                    self._refresh_agendamentos()
            except Exception as ex:
                print(f'Erro ao cadastrar agendamento: {ex}')

        actions = [
            ft.TextButton("Cancelar", on_click=lambda e: (setattr(dlg, 'open', False), self.system.page.update())),
            ft.ElevatedButton("Salvar Registro", bgcolor=ft.Colors.BLUE_500, color=ft.Colors.WHITE, on_click=on_submit)
        ]

        content_controls = [self.input_data, self.input_titulo, self.input_descricao]
        if self.input_dispositivo is not None:
            content_controls.append(self.input_dispositivo)

        dlg = ft.AlertDialog(
            title=ft.Text("Cadastrar Rotina na Tabela", weight=ft.FontWeight.BOLD),
            content=ft.Column(content_controls, spacing=12, tight=True),
            actions=actions,
            modal=True
        )
        page = self.system.page
        page.dialog = dlg
        dlg.open = True
        page.update()

    def _refresh_agendamentos(self):
        if not self.agendamentos_table:
            return
        agendamentos = self._carregar_agendamentos()
        self.agendamentos_table.rows = self._build_agendamentos_rows(agendamentos)
        self.system.page.update()

    def render(self):
        BG_CARD = "#111827"
        BORDER_COLOR = "#1f2937"
        ACCENT_BLUE = self.ft.Colors.BLUE_400
        ACCENT_PURPLE = self.ft.Colors.PURPLE_400
        
        agendamentos = self._carregar_agendamentos()
        total_agendamentos = len(agendamentos)
        
        # Busca o evento mais próximo dinamicamente
        evento_proximo_info = self._obter_proximo_evento(agendamentos)
        
        if evento_proximo_info:
            dados_ev = evento_proximo_info["dados"]
            dt_ev = evento_proximo_info["datetime"]
            restante = evento_proximo_info["tempo_restante"]
            
            # Formata tempo restante de forma amigável (Ex: 2h 14m ou 1 dia, 3h)
            horas_totais = int(restante.total_seconds() // 3600)
            minutos_totais = int((restante.total_seconds() % 3600) // 60)
            
            if horas_totais >= 24:
                dias = horas_totais // 24
                horas_restantes = horas_totais % 24
                tempo_string = f"Inicia em: {dias}d {horas_restantes}h"
            else:
                tempo_string = f"Inicia em: {horas_totais}h {minutos_totais}min"
                
            titulo_evento = dados_ev.get('descricao_livre') or "Rotina Operacional Sem Nome"
            data_evento_formatada = dt_ev.strftime("%d/%m/%Y às %H:%M")
            id_disp_evento = dados_ev.get('id_dispositivos', 'N/A')
        else:
            # Estado Fallback caso não existam agendamentos futuros
            tempo_string = "Sem eventos futuros"
            titulo_evento = "Nenhuma rotina agendada na fila"
            data_evento_formatada = "--/--/---- --:--"
            id_disp_evento = "N/A"

        self.agendamentos_table = self.ft.DataTable(
            border=self.ft.border.all(1, BORDER_COLOR),
            border_radius=10,
            heading_row_color="#1f2937",
            divider_thickness=1,
            horizontal_lines=self.ft.border.BorderSide(1, "#1f2937"),
            columns=[
                self.ft.DataColumn(self.ft.Text("DATA / HORA", color=self.ft.Colors.CYAN_400, size=12, weight="bold")),
                self.ft.DataColumn(self.ft.Text("DISPOSITIVO", color=self.ft.Colors.WHITE, size=12, weight="bold")),
                self.ft.DataColumn(self.ft.Text("DESCRIÇÃO LIVRE", color=self.ft.Colors.WHITE, size=12, weight="bold")),
            ],
            rows=self._build_agendamentos_rows(agendamentos),
            bgcolor=BG_CARD,
        )

        return self.ft.Column([
            self.ft.Row([
                self.ft.Column([
                    self.ft.Row([
                        self.ft.Icon(self.ft.Icons.CALENDAR_TODAY_ROUNDED, color=ACCENT_BLUE, size=32),
                        self.ft.Text("Cronograma & Ciclos de Teste", size=28, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE)
                    ]),
                    self.ft.Text("Planejamento de rotinas de pista e calibração de sensores", color=self.ft.Colors.GREY_400, size=14)
                ]),
                self.ft.ElevatedButton(
                    text="Agendar Novo Teste",
                    icon=self.ft.Icons.ADD,
                    bgcolor=ACCENT_BLUE,
                    color=self.ft.Colors.BLACK,
                    style=self.ft.ButtonStyle(shape=self.ft.RoundedRectangleBorder(radius=8)),
                    on_click=lambda e: self.system.view.page.agendamento(self.system).render()
                )
            ], alignment=self.ft.MainAxisAlignment.SPACE_BETWEEN),
            
            self.ft.Container(height=20),
            
            self.ft.Row([
                self.ft.Chip(label=self.ft.Text("Todos os Testes"), selected=True, bgcolor="#1e293b"),
                self.ft.Chip(label=self.ft.Text("Pendentes")),
                self.ft.Chip(label=self.ft.Text("Ciclos de Stress")),
                self.ft.Chip(label=self.ft.Text("Calibração")),
            ], spacing=10),
            
            self.ft.Container(height=15),
            
            # --- CARD DESTAQUE DINÂMICO ---
            self.ft.Container(
                bgcolor="#1e1b4b", 
                padding=25,
                border_radius=12,
                border=self.ft.border.all(1, "#312e81"),
                content=self.ft.Row([
                    self.ft.Column([
                        self.ft.Row([
                            self.ft.Container(
                                content=self.ft.Text("PRÓXIMO EVENTO", size=11, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.BLACK),
                                bgcolor=ACCENT_PURPLE,
                                padding=self.ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=5
                            ),
                            self.ft.Text(tempo_string, color=self.ft.Colors.GREY_300, size=13, weight=self.ft.FontWeight.W_500)
                        ], spacing=15),
                        self.ft.Container(height=5),
                        self.ft.Text(titulo_evento, size=22, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
                        self.ft.Row([
                            self.ft.Icon(self.ft.Icons.LOCATION_ON, color=self.ft.Colors.GREY_400, size=16),
                            self.ft.Text("Circuito de Testes", color=self.ft.Colors.GREY_400, size=14),
                            self.ft.Container(width=10),
                            self.ft.Icon(self.ft.Icons.ACCESS_TIME, color=self.ft.Colors.GREY_400, size=16),
                            self.ft.Text(data_evento_formatada, color=self.ft.Colors.GREY_400, size=14),
                        ])
                    ], expand=True),
                    
                    self.ft.Column([
                        self.ft.Text("Dispositivo Target", size=12, color=self.ft.Colors.GREY_400, weight=self.ft.FontWeight.BOLD),
                        self.ft.Row([
                            self.ft.Container(
                                content=self.ft.Text(f"ID: {id_disp_evento}", size=11, color=self.ft.Colors.WHITE),
                                bgcolor="#1f2937", padding=self.ft.padding.symmetric(horizontal=8, vertical=4), border_radius=4
                            ),
                        ], spacing=5)
                    ], alignment=self.ft.MainAxisAlignment.CENTER, horizontal_alignment=self.ft.CrossAxisAlignment.END)
                ])
            ),
            
            self.ft.Container(height=20),
            self.ft.Text("Linha do Tempo / Próximos Dias", size=18, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
            self.ft.Container(height=10),
            
            self.ft.Container(height=15),
            self.ft.Row([
                self.ft.Column([
                    self.ft.Text("Agendamentos no Banco (Tabela)", size=18, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
                    self.ft.Text(f"{total_agendamentos} registro(s) sincronizados", color=self.ft.Colors.GREY_400, size=12)
                ]),
            ], alignment=self.ft.MainAxisAlignment.SPACE_BETWEEN),
            self.ft.Container(height=10),
            
            self.agendamentos_table
        ], expand=True, scroll=self.ft.ScrollMode.AUTO)