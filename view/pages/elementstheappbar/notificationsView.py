class NotificationsView:
    def __init__(self, system):
        self.system = system
        self.ft = system.ft

    def render(self):
        return self.ft.Column([
            self.ft.Text("Central de Notificações", size=28, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
            self.ft.Container(height=20),
            self.ft.ListTile(
                leading=self.ft.Icon(self.ft.Icons.WARNING, color=self.ft.Colors.AMBER),
                title=self.ft.Text("Alerta de Gás Detectado", color=self.ft.Colors.WHITE),
                subtitle=self.ft.Text("Nível de NH3 excedeu 130 ppm na área de teste.", color=self.ft.Colors.GREY_400),
                bgcolor="#111827"
            ),
            self.ft.ListTile(
                leading=self.ft.Icon(self.ft.Icons.CHECK_CIRCLE, color=self.ft.Colors.GREEN_400),
                title=self.ft.Text("Sincronização Concluída", color=self.ft.Colors.WHITE),
                subtitle=self.ft.Text("Dados do robô baixados com sucesso.", color=self.ft.Colors.GREY_400),
                bgcolor="#111827"
            )
        ], expand=True)