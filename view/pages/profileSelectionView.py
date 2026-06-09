class ProfileSelectionView:
    def __init__(self, system):
        self.system = system
        self.on_profile_selected = self.system.view.page.home
        self.ft = self.system.ft
        
        self.db_client = self.system.model.database if hasattr(self.system.model, 'database') else None

    def _load_carrinhos(self) -> list:
        """Carrega os carrinhos/dispositivos do usuário logado do banco de dados."""
        if not self.db_client or not self.system:
            return []
        try:
            id_usuario = self.system.model.usuario_model.obter_id_usuario()
            if not id_usuario:
                print("Nenhum usuário logado")
                return []
            
            # --- TRAVA DE SEGURANÇA CONTRA ERRO DE INSTÂNCIA ---
            # Se db_client for a classe (type) e não o objeto, instanciamos ele aqui na hora
            db = self.db_client
            if isinstance(db, type):
                db = db(self.system)
            
            carrinhos = db.listar_carrinhos_usuario(id_usuario)
            return carrinhos or []
            
        except Exception as e:
            print(f"Erro ao carregar carrinhos: {e}")
            return []

    def render(self):
        self.system.page.clean()
        self.system.page.padding = 0

        # Fundo global da tela (Gradiente Escuro Roxo/Azul)
        fundo_gradiente = self.ft.RadialGradient(
            colors=["#2A0A4A", "#050011"], 
            center=self.ft.alignment.top_center, 
            radius=1.5
        )

        def voltar_para_selecao():
            """Como a SettingView limpa a tela inteira, precisamos renderizar esta view novamente para voltar."""
            self.render()

        def abrir_configuracoes(e):
            """Ensina o animador a instanciar a SettingView passando os argumentos corretos."""
            
            # Criamos uma função anônima (lambda) que recebe o 'sys' do animar_tela
            # e repassa para a SettingView junto com o voltar_para_selecao
            construtor_settings = lambda sys: self.system.view.page.settings(sys, voltar_para_selecao)
            
            # Agora mandamos a função construtora para a animação (ela não vai mais quebrar)
            self.system.view.animate.animacaoPagina.animar_tela(self.system, construtor_settings)

        # --- CONSTRUTOR DA TELA INICIAL (BOLHAS) ---
        def build_selection_view():
            titulo = self.ft.Text("Quem está monitorando?", size=40, weight=self.ft.FontWeight.W_300, color=self.ft.Colors.WHITE)

            # Botão de Logout 
            def handle_logout(e):
                self.system.usuario_model.limpar_usuario()
                self.system.view.animate.animacaoPagina.animar_tela(self.system, self.system.view.page.login)

            btn_logout = self.ft.Container(
                content=self.ft.IconButton(
                    icon=self.ft.Icons.LOGOUT,
                    icon_color=self.ft.Colors.RED_400,
                    icon_size=24,
                    tooltip="Sair",
                    on_click=handle_logout
                ),
                alignment=self.ft.alignment.top_left,
                padding=self.ft.padding.only(top=20, left=40)
            )

            # Botão de Engrenagem (Configurações Globais) no topo
            btn_engrenagem = self.ft.Container(
                content=self.ft.IconButton(
                    icon=self.ft.Icons.SETTINGS,
                    icon_color=self.ft.Colors.GREY_400,
                    icon_size=28,
                    tooltip="Sincronização de Telemetria",
                    on_click=abrir_configuracoes  
                ),
                alignment=self.ft.alignment.top_right,
                padding=self.ft.padding.only(top=20, right=40)
            )

            def criar_bolha_perfil(nome, gradiente_colors, is_add_button=False, carrinho=None):
                letra_inicial = nome[0].upper() if not is_add_button and nome else "+"
                
                circulo_interno = self.ft.Container(
                    width=132, height=132, shape=self.ft.BoxShape.CIRCLE, bgcolor="#050011",
                    content=self.ft.Text(letra_inicial, size=50, weight=self.ft.FontWeight.W_200, color=self.ft.Colors.WHITE),
                    alignment=self.ft.alignment.center,
                )

                circulo_externo = self.ft.Container(
                    width=140, height=140, shape=self.ft.BoxShape.CIRCLE,
                    gradient=self.ft.LinearGradient(
                        begin=self.ft.alignment.top_left, end=self.ft.alignment.bottom_right, colors=gradiente_colors
                    ) if not is_add_button else None,
                    border=self.ft.border.all(2, self.ft.Colors.GREY_700) if is_add_button else None,
                    content=circulo_interno,
                    alignment=self.ft.alignment.center,
                    animate_scale=self.ft.Animation(200, self.ft.AnimationCurve.DECELERATE),
                )

                nome_texto = self.ft.Text(nome, size=16, color=self.ft.Colors.GREY_400, weight=self.ft.FontWeight.W_400)

                lapis_icon = self.ft.IconButton(
                    icon=self.ft.Icons.EDIT, icon_color=self.ft.Colors.GREY_600, icon_size=16,
                    on_click=lambda e, n=nome, c=gradiente_colors: self.system.view.animate.animacaoPagina.animar_widget(
                        self.system,
                        self.main_content, 
                        self.system.view.widget.profileEdit(self.system, n, c, voltar_para_selecao).build()
                    ),
                    visible=not is_add_button
                )

                def on_hover(e):
                    if e.data == "true":
                        circulo_externo.scale = 1.1
                        nome_texto.color = self.ft.Colors.WHITE
                    else:
                        circulo_externo.scale = 1.0
                        nome_texto.color = self.ft.Colors.GREY_400
                    circulo_externo.update()
                    nome_texto.update()

                def on_click_action(e):
                    if is_add_button:
                        # Abre a Criação de Novo Perfil separada usando o animar_widget
                        self.system.view.animate.animacaoPagina.animar_widget(
                            self.system,
                            self.main_content, 
                            self.system.view.widget.profileEdit(self.system, "Novo Perfil", ["#4364F7", "#6FB1FC"], voltar_para_selecao).build()
                        )
                    else:
                        try:
                            if carrinho and carrinho.get('id_dispositivos'):
                                self.system.model.usuario_model.definir_dispositivo(carrinho.get('id_dispositivos'))
                        except Exception as ex:
                            print(f"Erro ao definir dispositivo: {ex}")
                        
                        self.system.view.animate.animacaoPagina.animar_tela(self.system, self.on_profile_selected)

                return self.ft.Container(
                    content=self.ft.Column(
                        [
                            circulo_externo,
                            self.ft.Container(height=10),
                            self.ft.Row([nome_texto, lapis_icon], alignment=self.ft.MainAxisAlignment.CENTER, spacing=0)
                        ],
                        horizontal_alignment=self.ft.CrossAxisAlignment.CENTER, spacing=0
                    ),
                    on_hover=on_hover, on_click=on_click_action
                )

            grid_perfis = self.ft.Row(
                [],  
                alignment=self.ft.MainAxisAlignment.CENTER, spacing=50
            )

            carrinhos = self._load_carrinhos()
            cores_padrao = [
                ["#FF007F", "#7F00FF"],
                ["#0052D4", "#6FB1FC"],
                ["#FF6B6B", "#FF8C42"],
                ["#4ECDC4", "#44A08D"],
                ["#9B59B6", "#8E44AD"],
            ]
            
            bolhas_carrinhos = []
            for idx, carrinho in enumerate(carrinhos):
                nome = carrinho.get('nomes_dispositivos', f'Carrinho {idx + 1}')
                cores = cores_padrao[idx % len(cores_padrao)]
                bolhas_carrinhos.append(criar_bolha_perfil(nome, cores, False, carrinho))
            
            bolhas_carrinhos.append(criar_bolha_perfil("Adicionar", [], is_add_button=True, carrinho=None))
            
            grid_perfis.controls = bolhas_carrinhos

            topbar = self.ft.Row(
                [btn_logout, self.ft.Container(expand=True), btn_engrenagem],
                alignment=self.ft.MainAxisAlignment.SPACE_BETWEEN,
                expand=False
            )

            return self.ft.Column(
                [
                    topbar,
                    self.ft.Container(height=40),
                    titulo,
                    self.ft.Container(height=60),
                    grid_perfis,
                ],
                horizontal_alignment=self.ft.CrossAxisAlignment.CENTER, expand=True
            )

        # --- GERENCIADOR DE ESTADO (TROCA DE TELAS) ---
        self.main_content = self.ft.Container(
            content=build_selection_view(), 
            expand=True,
            gradient=fundo_gradiente,
            opacity=0,
            animate_opacity=800,
        )

        self.system.page.add(self.main_content)
        
        self.system.time.sleep(0.1)
        self.main_content.opacity = 1
        self.main_content.update()