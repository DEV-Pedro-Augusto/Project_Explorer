import flet as ft

class Sidebar(ft.Container):
    def __init__(self, on_navigate=None):
        self.on_navigate = on_navigate
        super().__init__(
            width=60,
            bgcolor="#040730",
            border=ft.border.all(0, "#040C75"),
            shadow=ft.BoxShadow(blur_radius=10, color="black", offset=ft.Offset(0, 2)),
            border_radius=ft.border_radius.only(top_left=20, bottom_left=20, top_right=20, bottom_right=20),
            
            content=ft.Column(
                [
                    ft.IconButton(
                        icon=ft.Icons.HOME_OUTLINED, icon_size=20, icon_color="white",
                        on_click=lambda e: self._handle_nav(0)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.NOTIFICATIONS_OUTLINED, icon_size=20, icon_color="white",
                        on_click=lambda e: self._handle_nav(1)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.SPEED_OUTLINED, icon_size=20, icon_color="white",
                        on_click=lambda e: self._handle_nav(2)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CALENDAR_TODAY_OUTLINED, icon_size=20, icon_color="white",
                        on_click=lambda e: self._handle_nav(3)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.EMOJI_EVENTS_OUTLINED, icon_size=20, icon_color="white",
                        on_click=lambda e: self._handle_nav(5)
                    ),
                     ft.IconButton(
                        icon=ft.Icons.SETTINGS_OUTLINED, icon_size=20, icon_color="white",
                        on_click=lambda e: self._handle_nav(4)
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=20,
                expand=True,
            ),
            padding=10
        )

    def _handle_nav(self, index):
        if self.on_navigate:
            self.on_navigate(index)

"""       sidebar = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.NONE, # Oculta os textos igual na imagem
            bgcolor="#060A14",
            indicator_color="#1A2235",
            min_width=70,
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME),
                ft.NavigationRailDestination(icon=ft.Icons.NOTIFICATIONS_OUTLINED, selected_icon=ft.Icons.NOTIFICATIONS),
                ft.NavigationRailDestination(icon=ft.Icons.SPEED_OUTLINED, selected_icon=ft.Icons.SPEED),
                ft.NavigationRailDestination(icon=ft.Icons.CALENDAR_TODAY_OUTLINED, selected_icon=ft.Icons.CALENDAR_TODAY),
                ft.NavigationRailDestination(icon=ft.Icons.EMOJI_EVENTS_OUTLINED, selected_icon=ft.Icons.EMOJI_EVENTS),
                ft.NavigationRailDestination(icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS),
            ]
        )

"""