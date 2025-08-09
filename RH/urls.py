from django.urls import path
from .views.viewsFuncionario import IndexView, AddFuncionarioView, EditFuncionarioView, ListFuncionarioView, DelFuncionarioView, ConfigGeralEmpresaView, RelatorioExcelView
from .views.viewsEventos import GestaoEventosView, AddEventoView, UpdateEventoView, GetEventoView, DeleteEventoView, ExportEventosExcelView, GestaoTiposEventoView, AddTipoEventoView, UpdateTipoEventoView, GetTipoEventoView, DeleteTipoEventoView, GetInscricoesEventoView, AddInscricaoView, UpdateInscricaoView, GetInscricaoView, DeleteInscricaoView, ExportInscricoesExcelView, GetDiasEventoView, AddDiaEventoView, UpdateDiaEventoView, GetDiaEventoView, DeleteDiaEventoView, GetFrequenciasEventoView, AddFrequenciaView, UpdateFrequenciaView, GetFrequenciaView, DeleteFrequenciaView, ExportFrequenciasExcelView, SalvarFrequenciasLoteView, GestaoAbsenteismoView, CadastroAbsenteismoView, SalvarAbsenteismoLoteView, DashboardRHView


urlpatterns = [
       
     #Funcionario
    # path('', IndexView.as_view(), name="IndexViewevol"),
    path('listFuncionario/', ListFuncionarioView.as_view(), name="listFuncionario"),
    path('addFuncionario/', AddFuncionarioView.as_view(), name="addFuncionario"),
    path('editFuncionario/<int:id>/', EditFuncionarioView.as_view(), name="editFuncionario"),
    path('delFuncionario/<int:id>/', DelFuncionarioView.as_view(), name="delFuncionario"),
    path('getConfigGeral/', ConfigGeralEmpresaView.as_view(), name="getConfigGeral"),
    path('ExportExcel/', RelatorioExcelView.as_view(), name="ExportExcel"),
    path('ExportExcel', RelatorioExcelView.as_view(), name="ExportExcelNoSlash"),
   
    
    # Eventos - Nova gestão completa
    path('gestaoEventos/', GestaoEventosView.as_view(), name="gestaoEventos"),
    path('addEvento/', AddEventoView.as_view(), name="addEvento"),
    path('updateEvento/<int:id>/', UpdateEventoView.as_view(), name="updateEvento"),
    path('getEvento/<int:id>/', GetEventoView.as_view(), name="getEvento"),
    path('deleteEvento/<int:id>/', DeleteEventoView.as_view(), name="deleteEvento"),
    path('exportEventosExcel/', ExportEventosExcelView.as_view(), name="exportEventosExcel"),
    
    # Tipos de Evento
    path('gestaoTiposEvento/', GestaoTiposEventoView.as_view(), name="gestaoTiposEvento"),
    path('addTipoEvento/', AddTipoEventoView.as_view(), name="addTipoEvento"),
    path('updateTipoEvento/<int:id>/', UpdateTipoEventoView.as_view(), name="updateTipoEvento"),
    path('getTipoEvento/<int:id>/', GetTipoEventoView.as_view(), name="getTipoEvento"),
    path('deleteTipoEvento/<int:id>/', DeleteTipoEventoView.as_view(), name="deleteTipoEvento"),
    
    # Inscrições de Funcionários em Eventos
    path('getInscricoesEvento/<int:evento_id>/', GetInscricoesEventoView.as_view(), name="getInscricoesEvento"),
    path('addInscricao/', AddInscricaoView.as_view(), name="addInscricao"),
    path('updateInscricao/<int:inscricao_id>/', UpdateInscricaoView.as_view(), name="updateInscricao"),
    path('getInscricao/<int:inscricao_id>/', GetInscricaoView.as_view(), name="getInscricao"),
    path('deleteInscricao/<int:inscricao_id>/', DeleteInscricaoView.as_view(), name="deleteInscricao"),
    path('exportInscricoesExcel/<int:evento_id>/', ExportInscricoesExcelView.as_view(), name="exportInscricoesExcel"),
    
    # Dias do Evento
    path('getDiasEvento/<int:evento_id>/', GetDiasEventoView.as_view(), name="getDiasEvento"),
    path('addDiaEvento/', AddDiaEventoView.as_view(), name="addDiaEvento"),
    path('updateDiaEvento/<int:dia_evento_id>/', UpdateDiaEventoView.as_view(), name="updateDiaEvento"),
    path('getDiaEvento/<int:dia_evento_id>/', GetDiaEventoView.as_view(), name="getDiaEvento"),
    path('deleteDiaEvento/<int:dia_evento_id>/', DeleteDiaEventoView.as_view(), name="deleteDiaEvento"),
    
    # Frequências do Evento
    path('getFrequenciasEvento/<int:evento_id>/', GetFrequenciasEventoView.as_view(), name="getFrequenciasEvento"),
    path('addFrequencia/', AddFrequenciaView.as_view(), name="addFrequencia"),
    path('updateFrequencia/<int:frequencia_id>/', UpdateFrequenciaView.as_view(), name="updateFrequencia"),
    path('getFrequencia/<int:frequencia_id>/', GetFrequenciaView.as_view(), name="getFrequencia"),
    path('deleteFrequencia/<int:frequencia_id>/', DeleteFrequenciaView.as_view(), name="deleteFrequencia"),
    path('exportFrequenciasExcel/<int:evento_id>/', ExportFrequenciasExcelView.as_view(), name="exportFrequenciasExcel"),
    path('salvarFrequenciasLote/<int:evento_id>/', SalvarFrequenciasLoteView.as_view(), name="salvarFrequenciasLote"),
    
    # Gestão de Absenteísmo
    path('gestaoAbsenteismo/', GestaoAbsenteismoView.as_view(), name="gestaoAbsenteismo"),
    path('cadastroAbsenteismo/', CadastroAbsenteismoView.as_view(), name="cadastroAbsenteismo"),
    path('salvarAbsenteismoLote/', SalvarAbsenteismoLoteView.as_view(), name="salvarAbsenteismoLote"),
    
    # Dashboard RH
    path('dashboardRH/', DashboardRHView.as_view(), name="dashboardRH"),
    
]