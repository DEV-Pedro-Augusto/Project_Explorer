import flet as ft

class Sidebar(ft.Container):
    def __init__(self, on_navigate=None):
        self.on_navigate = on_navigate
        super().__init__(
            width=100,
            bgcolor="#7CA3C4",
            border_radius=ft.border_radius.only(top_left=0, bottom_left=0, top_right=40, bottom_right=40),
            content=ft.Column(
                [
                    ft.IconButton(
                        icon=ft.Icons.HOME, icon_size=30, icon_color="black",
                        on_click=lambda e: self._handle_nav(0)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CHANGE_HISTORY, icon_size=30, icon_color="black",
                        on_click=lambda e: self._handle_nav(1)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CHAT_BUBBLE_OUTLINE, icon_size=30, icon_color="black",
                        on_click=lambda e: self._handle_nav(2)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CLOUD, icon_size=30, icon_color="black",
                        on_click=lambda e: self._handle_nav(3)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CONFIRMATION_NUM_OUTLINED, icon_size=30, icon_color="black",
                        on_click=lambda e: self._handle_nav(4)
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=20,
                expand=True,
            ),
            padding=20
        )

    def _handle_nav(self, index):
        if self.on_navigate:
            self.on_navigate(index)
