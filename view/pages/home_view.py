"""Home page."""

from __future__ import annotations

from typing import Any
import flet as ft


class HomeView:
    """Home view page."""

    def __init__(self, ft, animador_pagina, animador_botao, controller_main):
        self.ft = ft
        self.controller_main = controller_main

    def build(self):
        return self.ft.Container(
            expand=True,
            padding=20,
            content=ft.Column([
                self.ft.Text("Bem-vindo ao Sistema de Inventário", size=28, weight="bold", color="white"),
                self.ft.Divider(height=30, color="transparent"),
                self.ft.Container(
                    padding=20, bgcolor="white", border_radius=10,
                    content=ft.Column([
                        self.ft.Text("Visão Geral", size=20, weight="bold"),
                        self.ft.Divider(),
                        self.ft.Row([
                            self.ft.Container(
                                padding=20, bgcolor="#4CAF50", border_radius=10, expand=1,
                                content=ft.Column([
                                    self.ft.Text("Itens Disponíveis", size=14, color="white"),
                                    self.ft.Text("150", size=36, weight="bold", color="white")
                                ])
                            ),
                            self.ft.Container(
                                padding=20, bgcolor="#FF9800", border_radius=10, expand=1,
                                content=ft.Column([
                                    self.ft.Text("Emprestados", size=14, color="white"),
                                    self.ft.Text("45", size=36, weight="bold", color="white")
                                ])
                            ),
                            self.ft.Container(
                                padding=20, bgcolor="#2196F3", border_radius=10, expand=1,
                                content=ft.Column([
                                    self.ft.Text("Total", size=14, color="white"),
                                    self.ft.Text("195", size=36, weight="bold", color="white")
                                ])
                            )
                        ], spacing=15)
                    ])
                )
            ], spacing=10)
        )
