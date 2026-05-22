class InventoryView:
    def __init__(self, system):
        self.system = system
        self.ft = system.ft
        
        # Lista simulada do inventário do robô.
        # "ativo" define se ele manda dados para o Dashboard ou se está isolado.
        self.sensores = [
            {"id": "s1", "nome": "Sensor de Gás (NH3)", "icon": self.ft.Icons.AIR, "color": self.ft.Colors.GREEN_400, "ativo": True},
            {"id": "s2", "nome": "Sensor de Temperatura", "icon": self.ft.Icons.THERMOSTAT, "color": self.ft.Colors.RED_500, "ativo": True},
            {"id": "s3", "nome": "Sensor de Umidade", "icon": self.ft.Icons.WATER_DROP, "color": self.ft.Colors.CYAN_400, "ativo": True},
            {"id": "s4", "nome": "Sensor Ultrassônico (Distância)", "icon": self.ft.Icons.STRAIGHTEN, "color": self.ft.Colors.BLUE_300, "ativo": False},
            {"id": "s5", "nome": "Sensor de Luminosidade", "icon": self.ft.Icons.WB_SUNNY, "color": self.ft.Colors.YELLOW_400, "ativo": True},
            {"id": "s6", "nome": "Barômetro (Pressão)", "icon": self.ft.Icons.SPEED, "color": self.ft.Colors.PURPLE_400, "ativo": True},
        ]

    def render(self):
        # Função para criar a UI de cada sensor na lista
        def criar_card_sensor(sensor):
            return self.ft.Container(
                content=self.ft.ListTile(
                    leading=self.ft.Container(
                        content=self.ft.Icon(sensor["icon"], color=sensor["color"], size=24),
                        padding=10,
                        bgcolor="#0A1122",
                        border_radius=8,
                        border=self.ft.border.all(1, sensor["color"])
                    ),
                    title=self.ft.Text(sensor["nome"], color=self.ft.Colors.WHITE, weight=self.ft.FontWeight.BOLD),
                    subtitle=self.ft.Text(
                        "Enviando dados para o Dashboard" if sensor["ativo"] else "Leitura isolada (Não contabilizada)",
                        color=self.ft.Colors.GREEN_400 if sensor["ativo"] else self.ft.Colors.GREY_500,
                        size=12
                    ),
                    trailing=self.ft.Switch(
                        value=sensor["ativo"], 
                        active_color=self.ft.Colors.BLUE_400,
                        tooltip="Ativar/Desativar no Dashboard"
                    )
                ),
                bgcolor="#111827",
                border_radius=10,
                margin=self.ft.margin.only(bottom=10)
            )

        # Monta a lista visual a partir do dicionário
        lista_cards = [criar_card_sensor(s) for s in self.sensores]

        return self.ft.Column([
            self.ft.Text("Inventário de Hardware", size=28, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
            self.ft.Text(
                "Ative ou desative os módulos no Dashboard. Sensores desativados continuam sendo lidos no backend e armazenados em log.", 
                color=self.ft.Colors.GREY_400
            ),
            self.ft.Container(height=20),
            
            # Container rolável com todos os sensores
            self.ft.Column(
                controls=lista_cards,
                scroll=self.ft.ScrollMode.AUTO,
                expand=True
            )
        ], expand=True)