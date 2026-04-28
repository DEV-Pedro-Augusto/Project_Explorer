import flet as ft
from core.app_imports import create_app
from model.database import Database

def main(page: ft.Page):
    service = create_app(page, ft,)
    page.add(service.view)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
    db_wrapper = Database()
    if db_wrapper.client:
        # Usamos o atributo 'client' da instância para fazer a query
        try:
            resposta = db_wrapper.client.table("dispositivos").select("nomes_dispositivos").execute()
            print(f"Robô encontrado: {resposta.data}")
            robo = resposta.data
            
        except Exception as e:
            print(f"❌ Erro na query: {e}")

