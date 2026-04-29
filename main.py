import flet as ft
from tests.mainTest import MainTest
from view.pages.loginView import LoginView
from view.pages.profileSelectionView import ProfileSelectionView
from view.pages.dashboardView import DashboardView

def main(page: ft.Page):
    # Configurações globais da janela
    page.title = "School Inventory - Sensor Cart"
    page.theme_mode = ft.ThemeMode.DARK # Modo Dark da sua imagem
    page.padding = 0

    # Funções de Roteamento (Avançar as telas)
    def ir_para_dashboard(nome_carrinho):
        tela = DashboardView(page, nome_carrinho)
        tela.render()

    def ir_para_selecao_perfil():
        tela = ProfileSelectionView(page, on_profile_selected=ir_para_dashboard)
        tela.render()

    def ir_para_login():
        tela = LoginView(page, on_login_success=ir_para_selecao_perfil)
        tela.render()

    # 1. Executa o Teste Inicial antes de desenhar a interface
    tester = MainTest()
    sistema_ok = tester.run_all_tests()

    if sistema_ok:
        # 2. Se o teste passar, abre a primeira tela (Login)
        ir_para_login()
    else:
        page.add(ft.Text("Erro Crítico: Falha nos testes de inicialização do sistema.", color=ft.colors.RED))

# Inicia o aplicativo Flet
if __name__ == "__main__":
    ft.app(target=main)