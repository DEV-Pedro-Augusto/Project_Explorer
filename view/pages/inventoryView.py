import flet as ft


class InventoryView:
    def __init__(self, page: ft.Page, db_client, on_back=None):
        self.page = page
        self.db_client = db_client
        self.on_back = on_back

    def _load_items(self) -> list:
        if not self.db_client:
            return []

        try:
            resposta = self.db_client.table(
                "dispositivos"
            ).select(
                "id_dispositivos, codigos_dispositivos, nomes_dispositivos, fabricacoes_dispositivos, ativacoes_dispositivos, ultimas_conexoes_dispositivos, status_dispositivos(nomes_status_dispositivos)"
            ).execute()
            return resposta.data or []
        except Exception as e:
            print(f"Erro ao carregar itens do banco: {e}")
            return []

    def _build_item_card(self, item: dict) -> ft.Container:
        status_nome = item.get("status_dispositivos", {}).get("nomes_status_dispositivos", "Sem status")
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row([
                        ft.Text(f"Código: {item.get('codigos_dispositivos', '-')}", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text(status_nome, color=ft.Colors.GREEN_400)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(f"Nome: {item.get('nomes_dispositivos', '-')}", color=ft.Colors.GREY_200),
                    ft.Text(f"Fabricado em: {item.get('fabricacoes_dispositivos', '-')}", color=ft.Colors.GREY_400, size=12),
                    ft.Text(f"Ativado em: {item.get('ativacoes_dispositivos', '-')}", color=ft.Colors.GREY_400, size=12),
                    ft.Text(f"Última conexão: {item.get('ultimas_conexoes_dispositivos', '-')}", color=ft.Colors.GREY_400, size=12),
                ],
                spacing=6
            ),
            bgcolor="#0F172A",
            padding=16,
            border_radius=10,
            border=ft.border.all(1, ft.Colors.BLUE_GREY_900)
        )

    def render(self) -> None:
        self.page.clean()
        self.page.title = "Inventário"
        self.page.bgcolor = "#060A14"
        self.page.padding = 20

        items = self._load_items()

        if items:
            cards = [self._build_item_card(item) for item in items]
            content = ft.Column([
                ft.Row([
                    ft.Text("Inventário", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.ElevatedButton("Voltar", on_click=lambda e: self.on_back() if self.on_back else None, bgcolor="#334155", color=ft.Colors.WHITE)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(f"Total de itens: {len(items)}", color=ft.Colors.GREY_400),
                ft.Container(height=20),
                ft.Column(cards, spacing=12)
            ], expand=True)
        else:
            content = ft.Column([
                ft.Row([
                    ft.Text("Inventário", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.ElevatedButton("Voltar", on_click=lambda e: self.on_back() if self.on_back else None, bgcolor="#334155", color=ft.Colors.WHITE)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text("Não foi possível carregar itens do banco de dados ou não existem dispositivos cadastrados.", color=ft.Colors.GREY_400),
            ], expand=True)

        self.page.add(content)

