import time
import threading

from controllers.app_controller import ControllerMain

# Views
from views.iu.main_view import MainView
from views.main_windows import MainWindow  # Supondo que você usa essa classe para janela principal

from views.animations.button_animate import AnimacoesBotao
from views.animations.page_animate import AnimacoesPage

from views.pages.dashboard import Dashboard
from views.pages.home_view import HomeView
from views.pages.inventory_view import InventoryView
from views.pages.login_view import LoginView
from views.pages.settings_view import SettingsView

# Models
from models.main_model import MainModel
from models.categoria_model import CategoriaModel
from models.item_model import ItemModel
from models.acao_model import AcaoPageItem
from models.usuario_model import UsuarioModel

from core.database import Database
from core.config_database import CONFIG_DB_SCHOOL

# Services
from services.app_services import AppServices


def create_app(page, ft):
    controller = ControllerMain()

    # Cria o container principal de páginas
    main_view = MainView(
        Dashboard,
        HomeView,
        InventoryView,
        LoginView,
        SettingsView
    )

    view = MainWindow(
        page,
        ft,
        AnimacoesPage,
        AnimacoesBotao,
        controller,
        main_view,
        time,
        threading,
    )

    models = MainModel(
        Database(CONFIG_DB_SCHOOL),
        CategoriaModel,
        ItemModel,
        AcaoPageItem,
        UsuarioModel
    )

    services = AppServices(models)  # Exemplo de injeção dos models nos serviços

    controller.view = view
    controller.models = models
    controller.services = services

    return controller