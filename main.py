import flet as ft
from core.app_imports import create_app

def main(page: ft.Page):
    controller = create_app(page, ft)
    controller.construir_page()

if __name__ == "__main__":
    ft.app(target=main)