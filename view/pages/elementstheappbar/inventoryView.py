class InventoryView:
    def __init__(self, system):
        self.system = system
        self.ft = system.ft
        self.db_client = system.model.database if hasattr(system.model, 'database') else None
        self.sensores = []
        self._load_sensores()

    def _load_sensores(self):
        """Carrega os sensores do banco de dados."""
        if not self.db_client:
            print("Erro: cliente do banco não disponível")
            self.sensores = []
            return
        
        try:
            # Obtém o ID do dispositivo selecionado
            id_dispositivo = self.system.obter_id_dispositivo()
            print(f"[INVENTORY] ID do dispositivo: {id_dispositivo}")
            
            if not id_dispositivo:
                print("[INVENTORY] Nenhum dispositivo selecionado")
                self.sensores = []
                return
            
            # Carrega apenas os sensores deste dispositivo
            sensores_db = self.db_client.listar_sensores_dispositivo(id_dispositivo)
            print(f"[INVENTORY] Sensores do BD: {sensores_db}")
            
            if not sensores_db:
                print("[INVENTORY] Nenhum sensor encontrado na junção")
                self.sensores = []
                return
            
            # Mapeia os sensores com ícones e cores - por nome e por ID
            mapeamento_sensores = {
                "mq-2": {"icon": self.ft.Icons.CLOUD, "color": self.ft.Colors.GREEN_400, "nome_display": "Sensor MQ2 (Gás)"},
                "mq-3": {"icon": self.ft.Icons.LOCAL_DRINK, "color": self.ft.Colors.YELLOW_700, "nome_display": "Sensor MQ3 (Álcool)"},
                "mczero7": {"icon": self.ft.Icons.SMOKE_FREE, "color": self.ft.Colors.RED_500, "nome_display": "Sensor MQ7 (CO)"},
                "mocr": {"icon": self.ft.Icons.OPACITY, "color": self.ft.Colors.ORANGE_400, "nome_display": "Módulo MOCR (Odometria)"},
                "hc-sr": {"icon": self.ft.Icons.STRAIGHTEN, "color": self.ft.Colors.BLUE_400, "nome_display": "Sensor HC-SR04 (Ultrassônico)"},
                "temperatura": {"icon": self.ft.Icons.THERMOSTAT, "color": self.ft.Colors.RED_400, "nome_display": "Sensor de Temperatura"},
                "umidade": {"icon": self.ft.Icons.WATER_DROP, "color": self.ft.Colors.CYAN_400, "nome_display": "Sensor de Umidade"},
                "distancia": {"icon": self.ft.Icons.STRAIGHTEN, "color": self.ft.Colors.BLUE_300, "nome_display": "Sensor Ultrassônico"},
                "luz": {"icon": self.ft.Icons.WB_SUNNY, "color": self.ft.Colors.YELLOW_400, "nome_display": "Sensor de Luminosidade"},
                "pressao": {"icon": self.ft.Icons.SPEED, "color": self.ft.Colors.PURPLE_400, "nome_display": "Barômetro"},
            }
            
            # Mapeamento por ID para sensores genéricos
            mapeamento_id_sensores = {
                6: {"icon": self.ft.Icons.WATER_DROP, "color": self.ft.Colors.CYAN_400, "nome_display": "Sensor de Umidade"},
                7: {"icon": self.ft.Icons.STRAIGHTEN, "color": self.ft.Colors.BLUE_300, "nome_display": "Sensor Ultrassônico"},
                8: {"icon": self.ft.Icons.THERMOSTAT, "color": self.ft.Colors.RED_400, "nome_display": "Sensor de Temperatura"},
            }
            
            self.sensores = []
            for sensor in sensores_db:
                # Tenta identificar o tipo de sensor pelo nome
                nome_sensor = sensor.get('nomes_sensores', '').lower()
                id_sensor = sensor.get('id_sensores')
                tipo_info = None
                
                print(f"[INVENTORY] Processando sensor ID={id_sensor}, Nome={nome_sensor}")
                
                # Primeiro tenta identificar por nome
                for chave, info in mapeamento_sensores.items():
                    if chave in nome_sensor:
                        tipo_info = info
                        print(f"[INVENTORY]   -> Identificado por nome: {chave}")
                        break
                
                # Se não identificou por nome, tenta por ID
                if not tipo_info and id_sensor in mapeamento_id_sensores:
                    tipo_info = mapeamento_id_sensores[id_sensor]
                    print(f"[INVENTORY]   -> Identificado por ID")
                
                # Se ainda não tem ícone, usa padrão
                if not tipo_info:
                    # Usa um ícone mais descritivo como padrão
                    tipo_info = {"icon": self.ft.Icons.SENSORS_OUTLINED, "color": self.ft.Colors.BLUE_300, "nome_display": f"Sensor {id_sensor} ({nome_sensor})"}
                    print(f"[INVENTORY]   -> Usando padrão")
                
                self.sensores.append({
                    "id": id_sensor,
                    "nome": tipo_info.get("nome_display", nome_sensor),
                    "icon": tipo_info.get("icon"),
                    "color": tipo_info.get("color"),
                    "ativo": True
                })
            
            print(f"[INVENTORY] Total de sensores carregados: {len(self.sensores)}")
            print(f"[INVENTORY] Sensores: {self.sensores}")
            
        except Exception as e:
            print(f"[INVENTORY] Erro ao carregar sensores: {e}")
            import traceback
            traceback.print_exc()
            self.sensores = []

    def render(self):
        # Recarrega os sensores do dispositivo selecionado
        self._load_sensores()
        
        print(f"[INVENTORY] Render chamado com {len(self.sensores)} sensores")
        
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
                    )
                ),
                bgcolor="#111827",
                border_radius=10,
                margin=self.ft.margin.only(bottom=10)
            )

        # Monta a lista visual a partir do dicionário
        lista_cards = [criar_card_sensor(s) for s in self.sensores]
        
        # Se não tiver sensores, mostra mensagem
        if not lista_cards:
            lista_cards = [
                self.ft.Container(
                    content=self.ft.Column([
                        self.ft.Icon(self.ft.Icons.SEARCH_OUTLINED, size=48, color=self.ft.Colors.GREY_500),
                        self.ft.Text(
                            "Nenhum sensor encontrado", 
                            size=16, 
                            color=self.ft.Colors.GREY_400,
                            text_align=self.ft.TextAlign.CENTER
                        ),
                        self.ft.Text(
                            "Verifique se há sensores associados ao dispositivo",
                            size=12,
                            color=self.ft.Colors.GREY_500,
                            text_align=self.ft.TextAlign.CENTER
                        )
                    ], alignment=self.ft.MainAxisAlignment.CENTER, horizontal_alignment=self.ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=40,
                    alignment=self.ft.alignment.center
                )
            ]

        return self.ft.Column([
            self.ft.Text("Inventário de Hardware", size=28, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
            self.ft.Text(
                "Sensores que estão conectados e enviando dados para o Dashboard", 
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