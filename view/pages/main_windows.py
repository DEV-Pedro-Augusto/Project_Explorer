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

        self.controls = [
            Sidebar(),
            ft.Container(
                expand=True,
                bgcolor="#1A1D63",  # cor de fundo principal
                content=ft.Text("Conteúdo principal aqui", color="white")
            )
        ]
