class EventsView:
    def __init__(self, system):
        self.system = system
        self.ft = system.ft

    def render(self):
        return self.ft.Column([
            self.ft.Text("Log de Eventos (Logs)", size=28, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
            self.ft.Container(height=20),
            self.ft.DataTable(
                columns=[
                    self.ft.DataColumn(self.ft.Text("Horário", color=self.ft.Colors.WHITE)),
                    self.ft.DataColumn(self.ft.Text("Evento", color=self.ft.Colors.WHITE)),
                    self.ft.DataColumn(self.ft.Text("Status", color=self.ft.Colors.WHITE)),
                ],
                rows=[
                    self.ft.DataRow(cells=[
                        self.ft.DataCell(self.ft.Text("14:23", color=self.ft.Colors.GREY_400)),
                        self.ft.DataCell(self.ft.Text("Início da Varredura", color=self.ft.Colors.GREY_400)),
                        self.ft.DataCell(self.ft.Text("OK", color=self.ft.Colors.GREEN_400)),
                    ]),
                    self.ft.DataRow(cells=[
                        self.ft.DataCell(self.ft.Text("14:45", color=self.ft.Colors.GREY_400)),
                        self.ft.DataCell(self.ft.Text("Pausa por Obstrução", color=self.ft.Colors.GREY_400)),
                        self.ft.DataCell(self.ft.Text("AVISO", color=self.ft.Colors.AMBER)),
                    ])
                ],
                bgcolor="#111827",
                border_radius=10
            )
        ], expand=True)