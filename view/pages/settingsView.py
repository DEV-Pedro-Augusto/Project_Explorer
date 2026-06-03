"""Settings page."""

from __future__ import annotations

from typing import Any


class SettingView:
    """Settings view page."""

    def __init__(self, parent: Any = None):
        self.parent = parent
        self.ft = parent.ft if parent is not None else None
        self.dark_mode = True
        self.alert_notifications = True
        self.battery_saver = False
        self.update_rate = "Tempo Real"

    def _on_toggle_dark_mode(self, e: Any) -> None:
        self.dark_mode = e.control.value
        if self.parent and hasattr(self.parent, 'page'):
            self.parent.page.update()

    def _on_toggle_alerts(self, e: Any) -> None:
        self.alert_notifications = e.control.value
        if self.parent and hasattr(self.parent, 'page'):
            self.parent.page.update()

    def _on_toggle_battery_saver(self, e: Any) -> None:
        self.battery_saver = e.control.value
        if self.parent and hasattr(self.parent, 'page'):
            self.parent.page.update()

    def _on_change_update_rate(self, e: Any) -> None:
        self.update_rate = e.control.value
        if self.parent and hasattr(self.parent, 'page'):
            self.parent.page.update()

    def render(self) -> Any:
        """Render the settings view."""
        if self.ft is None:
            raise RuntimeError("Flet runtime environment is required to render settings view.")

        return self.ft.Column(
            controls=[
                self.ft.Text("Configurações do Sistema", size=28, weight=self.ft.FontWeight.BOLD, color=self.ft.Colors.WHITE),
                self.ft.Container(height=20),

                self.ft.Text("Preferências do Aplicativo", size=16, weight=self.ft.FontWeight.W_500, color=self.ft.Colors.BLUE_400),
                self.ft.Container(
                    content=self.ft.Column(
                        controls=[
                            self.ft.ListTile(
                                leading=self.ft.Icon(self.ft.Icons.DARK_MODE, color=self.ft.Colors.WHITE),
                                title=self.ft.Text("Modo Escuro", color=self.ft.Colors.WHITE),
                                subtitle=self.ft.Text("Tema visual do painel", color=self.ft.Colors.GREY_500),
                                trailing=self.ft.Switch(value=self.dark_mode, active_color=self.ft.Colors.BLUE_400, on_change=self._on_toggle_dark_mode),
                            ),
                            self.ft.ListTile(
                                leading=self.ft.Icon(self.ft.Icons.NOTIFICATIONS_ACTIVE, color=self.ft.Colors.WHITE),
                                title=self.ft.Text("Notificações de Alerta", color=self.ft.Colors.WHITE),
                                subtitle=self.ft.Text("Avisos sobre gases ou bloqueios", color=self.ft.Colors.GREY_500),
                                trailing=self.ft.Switch(value=self.alert_notifications, active_color=self.ft.Colors.BLUE_400, on_change=self._on_toggle_alerts),
                            ),
                        ]
                    ),
                    bgcolor="#111827",
                    border_radius=10,
                    padding=10,
                ),

                self.ft.Container(height=20),

                self.ft.Text("Controle de Hardware", size=16, weight=self.ft.FontWeight.W_500, color=self.ft.Colors.BLUE_400),
                self.ft.Container(
                    content=self.ft.Column(
                        controls=[
                            self.ft.ListTile(
                                leading=self.ft.Icon(self.ft.Icons.BATTERY_SAVER, color=self.ft.Colors.WHITE),
                                title=self.ft.Text("Modo Economia de Bateria", color=self.ft.Colors.WHITE),
                                subtitle=self.ft.Text("Reduz o brilho e frequência de leitura", color=self.ft.Colors.GREY_500),
                                trailing=self.ft.Switch(value=self.battery_saver, active_color=self.ft.Colors.BLUE_400, on_change=self._on_toggle_battery_saver),
                            ),
                            self.ft.ListTile(
                                leading=self.ft.Icon(self.ft.Icons.SYNC, color=self.ft.Colors.WHITE),
                                title=self.ft.Text("Taxa de Atualização", color=self.ft.Colors.WHITE),
                                subtitle=self.ft.Text("Frequência de envio de dados do sensor", color=self.ft.Colors.GREY_500),
                                trailing=self.ft.Dropdown(
                                    width=150,
                                    options=[
                                        self.ft.dropdown.Option("Tempo Real"),
                                        self.ft.dropdown.Option("A cada 1 min"),
                                        self.ft.dropdown.Option("A cada 5 min"),
                                    ],
                                    value=self.update_rate,
                                    color=self.ft.Colors.WHITE,
                                    bgcolor="#1A2235",
                                    border_color=self.ft.Colors.TRANSPARENT,
                                    text_size=14,
                                    on_change=self._on_change_update_rate,
                                ),
                            ),
                        ]
                    ),
                    bgcolor="#111827",
                    border_radius=10,
                    padding=10,
                ),

                self.ft.Container(height=20),

                self.ft.Text("Conta", size=16, weight=self.ft.FontWeight.W_500, color=self.ft.Colors.BLUE_400),
                self.ft.Container(
                    content=self.ft.Column(
                        controls=[
                            self.ft.ListTile(
                                leading=self.ft.Icon(self.ft.Icons.PERSON, color=self.ft.Colors.WHITE),
                                title=self.ft.Text("Editar Perfil", color=self.ft.Colors.WHITE),
                                trailing=self.ft.Icon(self.ft.Icons.CHEVRON_RIGHT, color=self.ft.Colors.GREY_400),
                            ),
                            self.ft.ListTile(
                                leading=self.ft.Icon(self.ft.Icons.LOGOUT, color=self.ft.Colors.RED_400),
                                title=self.ft.Text("Sair da Conta", color=self.ft.Colors.RED_400),
                            ),
                        ]
                    ),
                    bgcolor="#111827",
                    border_radius=10,
                    padding=10,
                ),
            ],
            expand=True,
            scroll=self.ft.ScrollMode.AUTO,
        )
