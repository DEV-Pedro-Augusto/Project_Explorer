
import time
import threading

from api.service.app_services import AppServices

# Views
from view.main_view import MainView
from view.pages.main_windows import MainWindows
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
from model.formate_model import DadosBruto, DadosFormatados
from model.usuario_model import UsuarioModel

from model.database import Database
# Services
from api.service.app_services import AppServices



def create_app(page, ft):
    service = AppServices()

    # Cria um objeto para armazenar as views
    class ViewsContainer:
        pass
    
    views_container = ViewsContainer()
    views_container.homeView = HomeView
    views_container.configuracoesView = SettingsView
    views_container.devolucaoView = None
    views_container.emprestimoView = Dashboard
    views_container.cadastroItemView = None
    views_container.inventarioView = InventoryView

    # Cria o container principal de páginas
    main_view = MainView(
        page,
        ft,
        AnimacoesPage,      # animador_pagina
        AnimacoesBotao,     # animador_botao
        service,            # controller
        views_container,    # main_view (contêiner de views)
        time,               # time
        threading           # threading
    )

    view = MainWindows(
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
        Database(),
        CategoriaModel,
        ItemModel,
        UsuarioModel

    )

    services = AppServices(models) 

    service.view = view
    service.main_view = main_view
    service.models = models
    service.services = services

    return service