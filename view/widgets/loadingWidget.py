class LoadingWidget:
    def __init__(self, system, color=None, size=40, stroke_width=4, mensagem="Carregando..."):
        """
        Cria um indicador de carregamento simples (uma bolinha girando).
        """
        self.system = system
        self.ft = system.ft
        
        # Cor padrão (Ciano claro). Você pode passar outra se quiser.
        self.color = color if color else self.ft.Colors.CYAN_200 
        self.size = size
        self.stroke_width = stroke_width
        self.mensagem = mensagem

    def build(self):
        # O Círculo de Carregamento (O Flet anima isso sozinho quando 'value' não é definido)
        spinner = self.ft.ProgressRing(
            width=self.size, 
            height=self.size, 
            stroke_width=self.stroke_width,
            color=self.color,
        )

        # Se houver mensagem, exibe o spinner e o texto
        if self.mensagem:
            texto = self.ft.Text(
                self.mensagem, 
                size=14, 
                weight=self.ft.FontWeight.W_400, 
                color=self.ft.Colors.WHITE70
            )
            
            return self.ft.Container(
                content=self.ft.Column(
                    [spinner, self.ft.Container(height=10), texto],
                    horizontal_alignment=self.ft.CrossAxisAlignment.CENTER,
                    alignment=self.ft.MainAxisAlignment.CENTER
                ),
                alignment=self.ft.alignment.center,
                expand=True
            )
        else:
            # Se não houver mensagem, retorna só a bolinha centralizada
            return self.ft.Container(
                content=spinner,
                alignment=self.ft.alignment.center,
                expand=True
            )