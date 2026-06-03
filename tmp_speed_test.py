import flet as ft
from view.pages.elementstheappbar.speedView import SpeedView

class Dummy:
    pass

system = Dummy()
system.ft = ft

class DummyDatabase:
    def listar_sessoes_leituras(self, id_usuario=None, id_dispositivo=None):
        return [{'id_sessoes_leituras': 1, 'datas_uploads': '2026-05-26T20:30:11Z'}]
    def listar_leituras(self, id_sessao=None, id_dispositivo=None):
        return [{'id_leituras':1,'id_sessoes_leituras':1,'id_etiquetas_sensores':'Ultra_01','valores_lidos':'24.5','data_hora':'2026-05-26T20:30:11Z'}]

system.model = Dummy()
system.model.database = DummyDatabase()
system.obter_id_usuario = lambda: 10
system.obter_id_dispositivo = lambda: None

view = SpeedView(system)
control = view.render()
print(type(control))
print('rendered ok')
