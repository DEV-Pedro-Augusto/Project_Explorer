class CreateApp:

    def __init__(self,System):
       self.system = System
       self.system_check()
    
    def system_check(self):
        run = self.system_initialize() if TestInit(self.system) else self.system_exit()

    def system_initialize(self):

        def openApp(system):
            tela = system.view.page.login(system, on_login_success="")
            tela.render()


        openApp(self.system)
    
    def system_exit(self):
        
        system.page.add(self.system.ft.Text("Erro Crítico: Falha nos testes de inicialização do sistema.", color=self.system.ft.colors.RED))

    
class TestInit:
 
    def __init__(self,system):
        self.system = system 

    def run_all_tests(self):
        print("[TESTE] Iniciando verificação do sistema...")
        # Simula checagem de banco de dados e rede
        # system.test.testAPi , etc ...
        time.sleep(1) 
        print("[TESTE] Rede OK.")
        time.sleep(0.5)
        print("[TESTE] Classes carregadas. Tudo pronto!")
        return True # Se fosse False, o app pararia aqui
    


