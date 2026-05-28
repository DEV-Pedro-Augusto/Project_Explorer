class AnimationPage:
    """Motor central de transições e animações do projeto."""

    def __init__(self):
        pass

    # ==========================================
    # 0. CONSTRUTOR INTERNO DA UI DE LOADING
    # ==========================================
    @staticmethod
    def _build_loading_ui(system, mensagem):
        """Constrói um indicador de carregamento minimalista e moderno."""
        # Criando algo próximo ao seu design: um aro fino e translúcido
        # e um indicador principal brilhante.
        spinner = system.ft.ProgressRing(
            width=50, 
            height=50, 
            stroke_width=4, 
            color=system.ft.Colors.CYAN_200, # A parte brilhante que gira
            bgcolor=system.ft.Colors.with_opacity(0.1, system.ft.Colors.CYAN_200) # O "rastro" translúcido
        )
        
        texto = system.ft.Text(mensagem, size=14, weight=system.ft.FontWeight.W_400, color=system.ft.Colors.WHITE70)
        
        # Apenas um container simples, sem cartão de vidro!
        return system.ft.Container(
            content=system.ft.Column(
                [spinner, system.ft.Container(height=10), texto],
                horizontal_alignment=system.ft.CrossAxisAlignment.CENTER,
                alignment=system.ft.MainAxisAlignment.CENTER
            ),
            alignment=system.ft.alignment.center, 
            expand=True
        )

    # ==========================================
    # 1. ANIMAÇÕES SIMPLES (Transição Direta)
    # ==========================================
    @staticmethod
    def animar_widget(system, container_alvo, nova_view):
        """Esmaece uma caixa específica, troca o conteúdo e acende novamente."""
        if not container_alvo: return
        container_alvo.opacity = 0
        container_alvo.update()
        system.time.sleep(0.3)
        container_alvo.content = nova_view
        container_alvo.opacity = 1
        container_alvo.update()

    @staticmethod
    def animar_tela(system, nova_tela_class):
        """Esmaece toda a janela, limpa a tela e constrói a nova página."""
        if system.page.controls:
            for controle in system.page.controls:
                if hasattr(controle, 'opacity'):
                    controle.opacity = 0
            system.page.update()
            system.time.sleep(0.3) 
            
        system.page.clean()
        nova_tela_instancia = nova_tela_class(system)
        if hasattr(nova_tela_instancia, 'render'):
            nova_tela_instancia.render()

    # ==========================================
    # 2. ANIMAÇÕES COM LOADING INTELIGENTE
    # ==========================================
    @staticmethod
    def animacao_loading_widget(system, container_alvo, funcao_obter_view, mensagem="Carregando..."):
        """
        SÓ MOSTRA O LOADING SE A FUNÇÃO DEMORAR!
        Em vez de passar a 'nova_view' já pronta, passamos a função que GERA a view.
        Assim, podemos medir o tempo. Se demorar, mostramos o loading.
        """
        if not container_alvo: return
        
        # 1. Fade-out rápido do conteúdo atual
        container_alvo.opacity = 0
        container_alvo.update()
        
        # Iniciamos o relógio para ver quanto tempo a view demora pra ser criada
        inicio = system.time.time()
        
        # 2. Tentamos obter a nova tela (ex: puxar dados dos sensores)
        nova_view = funcao_obter_view() 
        
        fim = system.time.time()
        tempo_decorrido = fim - inicio

        # Se demorou MAIS de 0.2 segundos (200ms), a gente mostra o loading rapidinho
        # Se foi instantâneo, a gente pula direto pro passo final!
        if tempo_decorrido > 0.2:
            container_alvo.content = AnimationPage._build_loading_ui(system, mensagem)
            container_alvo.opacity = 1
            container_alvo.update()
            
            # Deixa o loading na tela pelo menos um pouquinho (pra não só piscar)
            system.time.sleep(0.8) 
            
            container_alvo.opacity = 0
            container_alvo.update()
            system.time.sleep(0.2)

        # 3. Mostra o novo conteúdo final
        container_alvo.content = nova_view
        container_alvo.opacity = 1
        container_alvo.update()

    @staticmethod
    def animacao_loading_tela(system, nova_tela_class, mensagem="Iniciando..."):
        """Loading inteligente para troca de telas inteiras."""
        # Fade-out da tela atual
        if system.page.controls:
            for controle in system.page.controls:
                if hasattr(controle, 'opacity'):
                    controle.opacity = 0
            system.page.update()
            system.time.sleep(0.3)
            
        system.page.clean()
        
        # Mostra o loading imediatamente enquanto prepara a nova classe
        loading_container = system.ft.Container(
            content=AnimationPage._build_loading_ui(system, mensagem),
            expand=True, opacity=1, # Já entra visível
            gradient=system.ft.RadialGradient(colors=["#2A0A4A", "#050011"], center=system.ft.alignment.top_center, radius=1.5)
        )
        system.page.add(loading_container)
        
        # Simula um tempo mínimo para você ver a animação caso o app seja muito rápido
        system.time.sleep(1.0) 
        
        loading_container.opacity = 0
        loading_container.update()
        system.time.sleep(0.3)
        system.page.clean()
        
        nova_tela_instancia = nova_tela_class(system)
        if hasattr(nova_tela_instancia, 'render'):
            nova_tela_instancia.render()