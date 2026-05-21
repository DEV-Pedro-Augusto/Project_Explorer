"""Dashboard page."""

from __future__ import annotations

from typing import Any
import flet as ft


class Dashboard:
    """Dashboard page widget."""

    def __init__(self, ft, animador_pagina, animador_botao, controller_main):
        self.ft = ft
        self.controller_main = controller_main

    def build(self):
        return self.ft.Container(
            expand=True,
            padding=20,
            content=ft.Column([
                self.ft.Text("Dashboard", size=28, weight="bold", color="white"),
                self.ft.Divider(height=30, color="transparent"),
                self.ft.Container(
                    padding=20, bgcolor="white", border_radius=10,
                    content=ft.Column([
                        self.ft.Text("Estatísticas", size=20, weight="bold"),
                        self.ft.Divider(),
                        self.ft.Text("Carrinhos Ativos: 1", size=16),
                        self.ft.Text("Carrinhos Inativos: 12", size=16),
                        self.ft.Text("Carrinhos Mortos: 3", size=16),
                        self.ft.Text("Perdidos: 5", size=16)
                    ], spacing=10)
                )
            ], spacing=10)
        )
