class AnimationPage:
    """Motor central de transições e animações do projeto."""

    def __init__(self):
        pass

    # ==========================================
    # 1. ANIMAÇÃO PARA WIDGETS (Partes da tela)
    # ==========================================
    @staticmethod
    def animar_widget(system, container_alvo, nova_view):
        """Esmaece uma caixa específica, troca o conteúdo e acende novamente."""
        if not container_alvo:
            return

        # Fade-out
        container_alvo.opacity = 0
        container_alvo.update()
        
        # Usando o time injetado no system
        system.time.sleep(0.3)
        
        # Troca o conteúdo e Fade-in
        container_alvo.content = nova_view
        container_alvo.opacity = 1
        container_alvo.update()

    # ==========================================
    # 2. ANIMAÇÃO PARA TELAS NORMAIS (Páginas Inteiras)
    # ==========================================
    @staticmethod
    def animar_tela(system, nova_tela_class):
        """Esmaece toda a janela, limpa a tela e constrói a nova página."""
        # Esmaece os controles principais atuais
        if system.page.controls:
            for controle in system.page.controls:
                if hasattr(controle, 'opacity'):
                    controle.opacity = 0
            system.page.update()
            
            # Usando o time injetado no system
            system.time.sleep(0.3) 

        # Limpa a tela
        system.page.clean()

        # Instancia e renderiza a nova tela
        nova_tela_instancia = nova_tela_class(system)
        if hasattr(nova_tela_instancia, 'render'):
            nova_tela_instancia.render()