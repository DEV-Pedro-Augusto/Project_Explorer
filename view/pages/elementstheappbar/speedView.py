class SpeedView:
    def __init__(self, system):
        self.system = system
        self.ft = system.ft

    def render(self):
        return self.ft.Column([
            self.ft.Text("Telemetria e Controle", size=28, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
            self.ft.Container(height=20),
            self.ft.Container(
                content=self.ft.Column([
                    self.ft.Text("Velocidade Atual", color=self.ft.Colors.GREY_400),
                    self.ft.Text("1.2 m/s", size=40, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.CYAN_400),
                    self.ft.Slider(min=0, max=5, divisions=10, value=1.2, label="{value} m/s")
                ], alignment=self.ft.MainAxisAlignment.CENTER, horizontal_alignment=self.ft.CrossAxisAlignment.CENTER),
                bgcolor="#111827",
                padding=40,
                border_radius=10
            )
        ], expand=True)