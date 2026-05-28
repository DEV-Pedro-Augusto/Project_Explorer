class CalendarView:
    def __init__(self, system):
        self.system = system
        self.ft = system.ft

    def render(self):
        # Paleta de Cores Alinhada
        BG_CARD = "#111827"
        BORDER_COLOR = "#1f2937"
        ACCENT_BLUE = self.ft.Colors.BLUE_400
        ACCENT_PURPLE = self.ft.Colors.PURPLE_400
        
        return self.ft.Column([
            # CABEÇALHO
            self.ft.Row([
                self.ft.Column([
                    self.ft.Row([
                        self.ft.Icon(self.ft.Icons.CALENDAR_TODAY_ROUNDED, color=ACCENT_BLUE, size=32),
                        self.ft.Text("Cronograma & Ciclos de Teste", size=28, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE)
                    ]),
                    self.ft.Text("Planejamento de rotinas de pista e calibração de sensores", color=self.ft.Colors.GREY_400, size=14)
                ]),
                # Botão para agendar nova rotina no banco
                self.ft.ElevatedButton(
                    text="Agendar Novo Teste",
                    icon=self.ft.Icons.ADD,
                    bgcolor=ACCENT_BLUE,
                    color=self.ft.Colors.BLACK,
                    style=self.ft.ButtonStyle(shape=self.ft.RoundedRectangleBorder(radius=8))
                )
            ], alignment=self.ft.MainAxisAlignment.SPACE_BETWEEN),
            
            self.ft.Container(height=20),
            
            # FILTROS DE VISUALIZAÇÃO RÁPIDA
            self.ft.Row([
                self.ft.Chip(label=self.ft.Text("Todos os Testes"), selected=True, bgcolor="#1e293b"),
                self.ft.Chip(label=self.ft.Text("Pendentes")),
                self.ft.Chip(label=self.ft.Text("Ciclos de Stress")),
                self.ft.Chip(label=self.ft.Text("Calibração")),
            ], spacing=10),
            
            self.ft.Container(height=15),
            
            # CARD DE DESTAQUE: PRÓXIMA MISSÃO (Contagem Regressiva Visual)
            self.ft.Container(
                bgcolor="#1e1b4b", # Roxo escuro para destacar
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
                            self.ft.Text("Inicia em: 11h 45min", color=self.ft.Colors.GREY_300, size=13, weight=self.ft.FontWeight.W_500)
                        ], spacing=15),
                        self.ft.Container(height=5),
                        self.ft.Text("Varredura de Perímetro e Coleta de Latência", size=22, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
                        self.ft.Row([
                            self.ft.Icon(self.ft.Icons.LOCATION_ON, color=self.ft.Colors.GREY_400, size=16),
                            self.ft.Text("Circuito de Testes - Bloco B", color=self.ft.Colors.GREY_400, size=14),
                            self.ft.Container(width=10),
                            self.ft.Icon(self.ft.Icons.ACCESS_TIME, color=self.ft.Colors.GREY_400, size=16),
                            self.ft.Text("Amanhã, às 08:30 AM", color=self.ft.Colors.GREY_400, size=14),
                        ])
                    ], expand=True),
                    
                    # Sensores Alvo desse teste especificamente
                    self.ft.Column([
                        self.ft.Text("Sensores Avaliados", size=12, color=self.ft.Colors.GREY_400, weight=self.ft.FontWeight.BOLD),
                        self.ft.Row([
                            self.ft.Container(
                                content=self.ft.Text("Ultra_01", size=11, color=self.ft.Colors.WHITE),
                                bgcolor="#1f2937",
                                padding=self.ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=4
                            ),
                            self.ft.Container(
                                content=self.ft.Text("Infra_L", size=11, color=self.ft.Colors.WHITE),
                                bgcolor="#1f2937",
                                padding=self.ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=4
                            ),
                        ], spacing=5)
                    ], alignment=self.ft.MainAxisAlignment.CENTER, horizontal_alignment=self.ft.CrossAxisAlignment.END)
                ])
            ),
            
            self.ft.Container(height=20),
            self.ft.Text("Linha do Tempo / Próximos Dias", size=18, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
            self.ft.Container(height=10),
            
            # LINHA DO TEMPO (LISTA DE EVENTOS FUTUROS)
            self.ft.Column([
                self.build_timeline_item(
                    date="28 MAI",
                    title="Teste de Stress: Autonomia de Bateria",
                    local="Laboratório de Robótica",
                    sensors=["Todos os Sensores", "Motores"],
                    type_color=self.ft.Colors.RED_ACCENT_400,
                    type_label="STRESS TEST",
                    ft=self.ft, bg_card=BG_CARD, border_color=BORDER_COLOR
                ),
                self.build_timeline_item(
                    date="30 MAI",
                    title="Calibração do Sensor de Linha (Infra_R / Infra_L)",
                    local="Pista de Testes Metálica",
                    sensors=["Infra_R", "Infra_L"],
                    type_color=self.ft.Colors.GREEN_400,
                    type_label="CALIBRAÇÃO",
                    ft=self.ft, bg_card=BG_CARD, border_color=BORDER_COLOR
                ),
                self.build_timeline_item(
                    date="02 JUN",
                    title="Simulação de Perda de Sinal Supabase (Modo Offline)",
                    local="Área Externa - Bloco A",
                    sensors=["Módulo Wi-Fi", "Cache SQLite"],
                    type_color=self.ft.Colors.CYAN_400,
                    type_label="SOFTWARE",
                    ft=self.ft, bg_card=BG_CARD, border_color=BORDER_COLOR
                ),
            ], spacing=12, scroll=self.ft.ScrollMode.AUTO, expand=True)
            
        ], expand=True, scroll=self.ft.ScrollMode.AUTO)

    def build_timeline_item(self, date, title, local, sensors, type_color, type_label, ft, bg_card, border_color):
        return ft.Container(
            bgcolor=bg_card,
            padding=15,
            border_radius=10,
            border=ft.border.all(1, border_color),
            content=ft.Row([
                # Bloco de Data Lateral Esquerdo
                ft.Container(
                    width=70,
                    alignment=ft.alignment.center,
                    content=ft.Column([
                        ft.Text(date.split()[0], size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text(date.split()[1], size=12, color=ft.Colors.GREY_400, weight=ft.FontWeight.W_500),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
                ),
                ft.VerticalDivider(color="#1f2937"),
                
                # Detalhes do Evento
                ft.Container(
                    expand=True,
                    content=ft.Column([
                        ft.Row([
                            ft.Text(title, size=15, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
                            # Badge de Categoria Dinâmico
                            ft.Container(
                                content=ft.Text(type_label, size=9, weight=ft.FontWeight.BOLD, color=type_color),
                                border=ft.border.all(1, type_color),
                                padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                border_radius=4
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Container(height=2),
                        ft.Row([
                            ft.Icon(ft.Icons.PLACE, size=14, color=ft.Colors.GREY_500),
                            ft.Text(local, size=13, color=ft.Colors.GREY_500),
                            ft.Container(width=15),
                            ft.Icon(ft.Icons.MEMORY, size=14, color=ft.Colors.GREY_500),
                            ft.Text(f"Foco: {', '.join(sensors)}", size=13, color=ft.Colors.GREY_500),
                        ])
                    ], spacing=4)
                ),
                
                # Ações rápidas para o agendamento
                ft.IconButton(icon=ft.Icons.EDIT_CALENDAR_ROUNDED, icon_color=ft.Colors.GREY_400, tooltip="Modificar parâmetros"),
                ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.RED_400, tooltip="Cancelar Teste")
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )