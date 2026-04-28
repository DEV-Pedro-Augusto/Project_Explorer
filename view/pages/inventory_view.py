"""Inventory page."""

from __future__ import annotations

from typing import Any
import flet as ft


class InventoryView:
    """Inventory page view."""

    def __init__(self, ft, animador_pagina, animador_botao, controller_main):
        self.ft = ft
        self.controller_main = controller_main
        
        # Grid para exibir itens
        self.grid = self.ft.GridView(expand=True, runs_count=5, max_extent=300, child_aspect_ratio=0.8, spacing=10)
        self.txt_total = self.ft.Text("0", size=24, weight="bold")
        
        # Constrói a página
        self.page = self.build()

    def build(self):
        return self.ft.Container(
            expand=True, padding=20, bgcolor="#f4f7f6",
            content=self.ft.Column([
                self.ft.Container(
                    padding=15, bgcolor="white", border_radius=10,
                    content=self.ft.Row([
                        self.ft.Icon(self.ft.Icons.INVENTORY, size=30),
                        self.ft.Column([
                            self.ft.Text("Total no Inventário"),
                            self.txt_total
                        ])
                    ])
                ),
                self.ft.Divider(height=20, color="transparent"),
                self.ft.ElevatedButton(
                    "Adicionar Item", icon=self.ft.Icons.ADD, height=50,
                    bgcolor="blue", color="white", on_click=self.abrir_add
                ),
                self.ft.Divider(),
                self.grid
            ])
        )

    def carregar(self):
        """Carrega os itens do inventário."""
        self.grid.controls.clear()
        
        # Placeholder - itens de exemplo
        itens_exemplo = [
            {'id': 1, 'cod_item': 'ITEM-001', 'nome_item': 'Notebook Dell', 'number_local': 'Sala 101', 'status': True},
            {'id': 2, 'cod_item': 'ITEM-002', 'nome_item': 'Projetor Epson', 'number_local': 'Sala 102', 'status': False},
            {'id': 3, 'cod_item': 'ITEM-003', 'nome_item': 'Mouse Wireless', 'number_local': 'Sala 103', 'status': True},
        ]
        
        self.txt_total.value = str(len(itens_exemplo))
        for i in itens_exemplo:
            self.grid.controls.append(self._card(i))
        
        if hasattr(self, 'page') and self.page:
            self.page.update()

    def _card(self, i):
        disp = i.get('status', True)
        cor = "green" if disp else "red"
        txt_btn = "Emprestar" if disp else "Devolver"
        cor_btn = "blue" if disp else "orange"
        
        return self.ft.Card(
            elevation=4,
            content=self.ft.Container(
                padding=10, bgcolor="white", border_radius=10,
                content=self.ft.Column([
                    self.ft.Row([
                        self.ft.Container(
                            bgcolor="#f0f0f0", padding=5, border_radius=5,
                            content=self.ft.Text(i.get('cod_item', ''), size=10, weight="bold")
                        ),
                        self.ft.Container(expand=True),
                        self.ft.IconButton(
                            self.ft.Icons.INFO, icon_size=20, icon_color="blue",
                            tooltip="Ver Detalhes", on_click=lambda e: self.ver_info(e, i)
                        ),
                        self.ft.IconButton(
                            self.ft.Icons.DELETE, icon_size=20, icon_color="red",
                            tooltip="Remover", on_click=lambda e: self.deletar(i.get('id'))
                        )
                    ]),
                    self.ft.Text(i.get('nome_item', ''), weight="bold", size=16, max_lines=1),
                    self.ft.Text(f"Loc: {i.get('number_local', '')}", size=12, color="grey"),
                    self.ft.Container(
                        padding=5, bgcolor=cor+"100", border_radius=15,
                        content=self.ft.Text("Disponível" if disp else "Emprestado", color=cor, size=11)
                    ),
                    self.ft.Divider(height=10, color="transparent"),
                    self.ft.ElevatedButton(
                        text=txt_btn, width=float("inf"), bgcolor=cor_btn, color="white",
                        on_click=lambda e: self.acao(e, i.get('id'))
                    )
                ])
            )
        )

    def abrir_add(self, e):
        """Abre diálogo para adicionar item."""
        pass

    def ver_info(self, e, item):
        """Mostra informações do item."""
        pass

    def deletar(self, item_id):
        """Deleta um item."""
        pass

    def acao(self, e, item_id):
        """Ação de emprestar/devolver."""
        pass
        self.txt_nome = self.ft.TextField(label="Nome do Item", width=400)
        self.txt_cat = self.ft.TextField(label="Categoria", width=400)
        self.txt_tipo = self.ft.TextField(label="Tipo", width=400)
        self.txt_qtd = self.ft.TextField(label="Quantidade", width=400, value="1")
        self.txt_local = self.ft.TextField(label="Localização (id)", width=400)
        self.txt_estado = self.ft.TextField(label="Estado de Uso (id)", width=400)
        self.txt_desc = self.ft.TextField(label="Descrição", width=400, multiline=True, min_lines=3)

        self.dialog_add = self.ft.AlertDialog(
            modal=True,
            title=self.ft.Text("Cadastrar Novo Item"),
            content=self.ft.Column([
                self.txt_cod,
                self.txt_nome,
                self.txt_cat,
                self.txt_tipo,
                self.txt_qtd,
                self.txt_local,
                self.txt_estado,
                self.txt_desc
            ], spacing=10),
            actions=[
                self.ft.TextButton("Cancelar", on_click=lambda _: self.fechar_dialogo()),
                self.ft.ElevatedButton("Salvar", icon=self.ft.Icons.SAVE, bgcolor="green", color="white", on_click=self.salvar_item)
            ],
            actions_alignment="end"
        )

    
        e.page.dialog = self.dialog_add
        self.dialog_add.open = True
        e.page.update()



    def fechar_dialogo(self):
        if hasattr(self, 'dialog_add'):
            self.dialog_add.open = False
            self.page.update()

    def salvar_item(self, e):
        try:
            inventario = [{
                "Nome_do_Item": self.txt_nome.value.strip(),
                "Cod_Item": self.txt_cod.value.strip(),
                "Categoria": self.txt_cat.value.strip(),
                "Tipo": self.txt_tipo.value.strip(),
                "Localizacao": int(self.txt_local.value.strip()),
                "Estado_de_Uso": int(self.txt_estado.value.strip()),
                "Status": False,
                "Descricao": self.txt_desc.value.strip(),
                "Quantidade": int(self.txt_qtd.value.strip() or 1)
            }]

            self.db.add_items(inventario)

            self.fechar_dialogo()
            self.carregar()
            self.page.snack_bar = self.ft.SnackBar(self.ft.Text("Item cadastrado com sucesso!"), bgcolor="green")
            self.page.snack_bar.open = True
            self.page.update()

        except Exception as ex:
            self.page.snack_bar = self.ft.SnackBar(self.ft.Text(f"Erro: {ex}"), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()

    def deletar(self, uid):
        self.controller.deletar_item(uid)
        self.carregar()
