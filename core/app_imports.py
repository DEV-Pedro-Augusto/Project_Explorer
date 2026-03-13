import time
import threading

from service.app_services import AppServices

# Views
from view.iu.main_view import MainView
from view.main_windows import MainWindow  # Supondo que você usa essa classe para janela principal

from view.animations.button_animate import AnimacoesBotao
from view.animations.page_animate import AnimacoesPage

from view.pages.dashboard import Dashboard
from view.pages.home_view import HomeView
from view.pages.inventory_view import InventoryView
from view.pages.login_view import LoginView
from view.pages.settings_view import SettingsView

# Models
from model.main_model import MainModel
from model.categoria_model import CategoriaModel
from model.item_model import ItemModel
from model.acao_model import AcaoPageItem
from model.usuario_model import UsuarioModel

from core.database import Database
from core.config_database import CONFIG_DB_SCHOOL

# Services
from service.app_services import AppServices


def create_app(page, ft):
    service = AppServices()

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
        service,
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

    service.view = view
    service.models = models
    service.services = services

    return service
