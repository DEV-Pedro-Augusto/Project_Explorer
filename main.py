import flet as ft
import time
import threading

from service.app_services import AppServices

# Views

from view.main_windows import MainWindow  
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

from core.app_imports import create_app

def main(page: ft.Page):
    service = create_app(page, ft)
    service.construir_page()

if __name__ == "__main__":
    ft.app(target=main)