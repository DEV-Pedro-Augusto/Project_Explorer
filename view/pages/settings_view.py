"""Settings page."""

from __future__ import annotations

from typing import Any
import flet as ft


class SettingsView:
    """Settings view page."""

    def __init__(self, ft, animador_pagina, animador_botao, controller_main):
        self.ft = ft
        self.controller_main = controller_main

    def build(self):
        return self.ft.Container(
            expand=True,
            padding=20,
            content=ft.Column([
                self.ft.Text("Configurações", size=28, weight="bold", color="white"),
                self.ft.Divider(height=30, color="transparent"),
                self.ft.Container(
                    padding=20, bgcolor="white", border_radius=10,
                    content=ft.Column([
                        self.ft.Text("Perfil", size=20, weight="bold"),
                        self.ft.Divider(),
                        self.ft.TextField(label="Nome", value="Administrador"),
                        self.ft.TextField(label="Email", value="admin@sistema.com"),
                        self.ft.ElevatedButton("Salvar", bgcolor="blue", color="white", height=50)
                    ], spacing=15)
                )
            ], spacing=10)
        )
