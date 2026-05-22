class CalendarView:
    def __init__(self, system):
        self.system = system
        self.ft = system.ft

    def render(self):
        return self.ft.Column([
            self.ft.Text("Cronograma de Testes", size=28, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
            self.ft.Container(height=20),
            self.ft.Row([
                self.ft.Icon(self.ft.Icons.CALENDAR_MONTH, size=50, color=self.ft.Colors.BLUE_400),
                self.ft.Column([
                    self.ft.Text("Próxima varredura agendada:", color=self.ft.Colors.GREY_400),
                    self.ft.Text("Amanhã, 08:30 AM - Bloco B", size=18, color=self.ft.Colors.WHITE)
                ])
            ], spacing=20)
        ], expand=True)