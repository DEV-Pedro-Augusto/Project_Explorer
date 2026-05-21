import flet as ft
from core.app_imports import create_app
from model.database import Database

def main(page: ft.Page):
    service = create_app(page, ft,)
    
    page.add(service.view)
    page.update()

if __name__ == "__main__":
    db_wrapper = Database()
    if db_wrapper.client:
        # Usamos o atributo 'client' da instância para fazer a query
        try:
            resposta = db_wrapper.client.table("dispositivos").select("nomes_dispositivos").execute()
            print(f"Robô encontrado: {resposta.data}")
            Database.exibir_catalogo_de_status(db_wrapper.client)
            Database.buscar_relatorio_por_status(db_wrapper.client, 1)  # Exemplo com
            
        except Exception as e:
            print(f"❌ Erro na query: {e}")
    ft.app(target=main)

