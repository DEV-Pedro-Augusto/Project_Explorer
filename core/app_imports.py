
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

    services = AppServices(models) 

    service.view = view
    service.models = models
    service.services = services

    return service
