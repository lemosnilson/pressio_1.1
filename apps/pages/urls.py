from django.urls import path
from .views import (
    index,
    register_view,
    insercao,
    insercao_mats,
    insercao_props,
    revisao_dados_view, # <-- Importação da view de revisão
    calcular_view,
    resultados_view,
    under_construction,
)

urlpatterns = [
    # Home / Dashboard
    path('',                  index,                name='index'),

    # Cadastro
    path('register/',         register_view,        name='register'),

    # Fluxo do Formulário
    path('insercao/',         insercao,             name='insercao'),
    path('insercao/mats/',    insercao_mats,        name='insercao_mats'),
    path('insercao/props/',   insercao_props,       name='insercao_props'),
    
    # ADICIONAMOS A ROTA PARA A PÁGINA DE REVISÃO
    path('revisao/',          revisao_dados_view,   name='revisao'),

    # Rota final para executar o cálculo
    path('calcular/',         calcular_view,        name='calcular'),
    
    # Rota para exibir os resultados finais
    path('resultados/',       resultados_view,      name='resultados'),

    # Página em construção
    path('under-construction/', under_construction, name='under_construction'),
]