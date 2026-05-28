import flet as ft
import time

#    VIEW: Elements view all
    
    # Pages
from view.pages.loginView import LoginView
from view.pages.profileSelectionView import ProfileSelectionView
from view.pages.homeView import HomeView
from view.pages.settingsView import SettingView
from view.pages.cadastroView import CadastroView

    # Elements the Appbar 
from view.pages.elementstheappbar.dashboardView import DashboardView
from view.pages.elementstheappbar.eventsView import EventsView
from view.pages.elementstheappbar.notificationsView import NotificationsView
from view.pages.elementstheappbar.settingsView import SettingsView
from view.pages.elementstheappbar.speedView import SpeedView
from view.pages.elementstheappbar.inventoryView import InventoryView
from view.pages.elementstheappbar.calendar import CalendarView

    # Animations
from view.animations.buttonAnimation import AnimationButton
from view.animations.pageAnimation import AnimationPage

    # Widgets
from view.widgets.globalsettingsWidget import GlobalSettingsWidget
from view.widgets.profileeditWidget import ProfileEditWidget
from view.widgets.loadingWidget import LoadingWidget

    # Routes
from view.mainView import MainView
from view.pages.mainWindow import MainWindow
from view.pages.elementstheappbar.mainElementsTheAppbar import MainElementsAppbar
from view.widgets.mainWidget import MainWidget
from view.animations.mainAnimation import MainAnimate



#    MODEL: Elements model all 

    # Models
from model.categoriaModel import CategoriaModel
from model.databaseModel import Database
from model.formatModel import FormatModel
from model.itemModel import ItemModel
from model.usuarioModel import UsuarioModel

    # Routes
from model.mainModel import MainModel
from model.system import System


#    CORE: Elemets core all 

    # Core
from core.appImports import CreateApp



#    TEST: Elemets test all

    # Test
from tests.testApi import TestApi
from tests.testController import TestController
from tests.testView import TestView
from tests.testModel import TestModel

    # Routes
from tests.mainTest import MainTest



#    API: Elemets api  all
    # Api > Service
from api.service.app_services import AppServices


#    CONTROLLER: Elemets controller all


def main(page: ft.Page):
   
    page.title = "Sensor Cart"
    page.theme_mode = ft.ThemeMode.DARK # Modo Dark da sua imagem
    page.padding = 0


    CreateApp(
        System(
        page,
        ft,
        time,
        MainView( 
            MainWindow(
                HomeView, 
                LoginView,
                ProfileSelectionView,
                SettingView,
                CadastroView,
                MainElementsAppbar(
                    DashboardView,
                    NotificationsView,
                    SpeedView,
                    CalendarView,
                    EventsView,
                    SettingsView,
                    InventoryView
                ),
            ),
            MainWidget(
                GlobalSettingsWidget,
                ProfileEditWidget,
                LoadingWidget

            ),
            MainAnimate(
                AnimationButton,
                AnimationPage
    
            )
        ),
        MainModel(
            Database,
            CategoriaModel,
            ItemModel,
            FormatModel,
            UsuarioModel,
        ),
        MainTest(
            TestApi,
            TestController,
            TestModel,
            TestView
        ),
        "Controller",
        AppServices
        )
        )
"""
    # Funções de Roteamento (Avançar as telas)
    def ir_para_dashboard(nome_carrinho):
        tela = DashboardView(page, nome_carrinho)
        tela.render()

    def ir_para_selecao_perfil():
        tela = ProfileSelectionView(page, on_profile_selected=ir_para_dashboard)
        tela.render()

    def open_app():
        tela = LoginView(page, on_login_success=ir_para_selecao_perfil)
        tela.render()

    # 1. Executa o Teste Inicial antes de desenhar a interface
    tester = MainTest()
    sistema_ok = tester.run_all_tests()

    if sistema_ok:
        # 2. Se o teste passar, abre a primeira tela (Login)
        open_app()
    else:
        page.add(ft.Text("Erro Crítico: Falha nos testes de inicialização do sistema.", color=ft.colors.RED))

"""
if __name__ == "__main__":
    ft.app(target=main)