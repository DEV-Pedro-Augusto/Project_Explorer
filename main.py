import flet as ft
import time
import threading


# Views


# Models


# Services

def main(page: ft.Page):
    service = create_app(page, ft)
    service.construir_page()

if __name__ == "__main__":
    ft.app(target=main)