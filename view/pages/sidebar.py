import flet as ft

class Sidebar(ft.Container):
    def __init__(self):
        super().__init__(
            width=100,
            bgcolor="#7CA3C4",  # cor da barra lateral
            border_radius=ft.border_radius.only(top_left=0, bottom_left=0, top_right=40, bottom_right=40),
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.HOME, weight=40, color="black"),
                    ft.Icon(ft.Icons.CHANGE_HISTORY, weight=40, color="black"),
                    ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE, weight=40, color="black"),
                    ft.Icon(ft.Icons.CLOUD, weight=40, color="black"),
                    ft.Icon(ft.Icons.CONFIRMATION_NUM_OUTLINED, weight=40, color="black"),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=40,
                expand=True,
            ),
            padding=20
        )
