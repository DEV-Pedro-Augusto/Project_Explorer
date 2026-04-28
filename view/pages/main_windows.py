"""Main window implementation."""

from __future__ import annotations
from typing import Any, Optional
import flet as ft
from view.pages.sidebar import Sidebar

class MainWindows(ft.Row):
    def __init__(self, page, ft, AnimacoesPage, AnimacoesBotao, service, main_view, time, threading):
        super().__init__()
        self.expand = True
        self.page = page
        self.ft = ft
        self.animacoes_page = AnimacoesPage
        self.animacoes_botao = AnimacoesBotao
        self.service = service
        self.main_view = main_view
        self.time = time
        self.threading = threading

        # Container de conteúdo que será atualizado pela navegação
        self.container_conteudo = ft.Container(
            expand=True,
            content=ft.Text("Carregando...", color="white"),
            padding=20
        )

        # Passa o container para o main_view
        if hasattr(self.main_view, 'set_container'):
            self.main_view.set_container(self.container_conteudo)

        self.controls = [
            Sidebar(on_navigate=self.on_navigate),
            ft.Container(
                expand=True,
                bgcolor="#1A1D63",
                content=self.container_conteudo
            )
        ]

    def on_navigate(self, index):
        """Handle navigation from sidebar."""
        if hasattr(self.main_view, 'navegar'):
            self.main_view.navegar(index)
