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
        if not inicio_str or not fim_str:
            return "Em progresso..."
        
        try:
            inicio = datetime.fromisoformat(inicio_str.replace('Z', '+00:00'))
            fim = datetime.fromisoformat(fim_str.replace('Z', '+00:00'))
            duracao = fim - inicio
            
            # Converte para formato HH:MM:SS
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
            sessoes = self.system.model.database.listar_sessoes_leituras(id_usuario)
            return sessoes or []
        except Exception as e:
            print(f"Erro ao carregar sessões: {e}")
            return []

    def _criar_linhas_tabela(self):
        """Cria as linhas da tabela a partir das sessões de leitura."""
        sessoes = self._carregar_sessoes()
        linhas = []
        
        if not sessoes:
            # Se não houver sessões, exibe uma linha padrão
            linhas.append(
                self.ft.DataRow(cells=[
                    self.ft.DataCell(self.ft.Text("--:--", color=self.ft.Colors.GREY_400, size=10)),
                    self.ft.DataCell(self.ft.Text("--:--", color=self.ft.Colors.GREY_400, size=10)),
                    self.ft.DataCell(self.ft.Text("N/A", color=self.ft.Colors.GREY_400, size=10)),
                    self.ft.DataCell(self.ft.Text("Sem eventos", color=self.ft.Colors.GREY_400, size=10)),
                    self.ft.DataCell(self.ft.Text("N/A", color=self.ft.Colors.GREY_400, size=10)),
                    self.ft.DataCell(self.ft.Text("Aguardando...", color=self.ft.Colors.AMBER, size=10)),
                ])
            )
        else:
            for sessao in sessoes:
                # Extrai todos os dados
                id_sessao = str(sessao.get('id_sessoes_leituras', 'N/A'))
                id_usuario = str(sessao.get('id_usuarios', 'N/A'))
                id_dispositivo = str(sessao.get('id_dispositivos', 'N/A'))
                data_upload = self._formatar_timestamp(sessao.get('datas_uploads'))
                inicio = self._formatar_timestamp(sessao.get('inicio_missao'))
                fim = self._formatar_timestamp(sessao.get('fim_missao'))
                duracao = self._calcular_duracao(sessao.get('inicio_missao'), sessao.get('fim_missao'))
                descricao = sessao.get('descricao_livre', 'Sem descrição')[:25]
                
                # Define o status baseado no fim_missao
                if sessao.get('fim_missao'):
                    status = "✓ Finalizada"
                    status_color = self.ft.Colors.GREEN_400
                else:
                    status = "⏱ Em Andamento"
                    status_color = self.ft.Colors.BLUE_400
                
                # Cria a linha com todos os dados
                linhas.append(
                    self.ft.DataRow(cells=[
                        self.ft.DataCell(self.ft.Text(data_upload, color=self.ft.Colors.GREY_400, size=10)),
                        self.ft.DataCell(self.ft.Text(inicio, color=self.ft.Colors.GREY_400, size=10)),
                        self.ft.DataCell(self.ft.Text(duracao, color=self.ft.Colors.CYAN_400, size=10, weight="bold")),
                        self.ft.DataCell(self.ft.Text(descricao, color=self.ft.Colors.GREY_400, size=10)),
                        self.ft.DataCell(self.ft.Text(id_dispositivo, color=self.ft.Colors.BLUE_200, size=10)),
                        self.ft.DataCell(self.ft.Text(status, color=status_color, size=10, weight="bold")),
                    ])
                )
        
        return linhas

    def render(self):
        return self.ft.Column([
            self.ft.Text("Log de Eventos (Sessões de Leitura)", size=28, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
            self.ft.Container(height=20),
            self.ft.DataTable(
                columns=[
                    self.ft.DataColumn(self.ft.Text("Data Upload", color=self.ft.Colors.WHITE, size=11)),
                    self.ft.DataColumn(self.ft.Text("Início", color=self.ft.Colors.WHITE, size=11)),
                    self.ft.DataColumn(self.ft.Text("Duração", color=self.ft.Colors.CYAN, size=11)),
                    self.ft.DataColumn(self.ft.Text("Descrição", color=self.ft.Colors.WHITE, size=11)),
                    self.ft.DataColumn(self.ft.Text("Dispositivo", color=self.ft.Colors.WHITE, size=11)),
                    self.ft.DataColumn(self.ft.Text("Status", color=self.ft.Colors.WHITE, size=11)),
                ],
                rows=self._criar_linhas_tabela(),
                bgcolor="#111827",
                border_radius=10
            )
        ], expand=True)