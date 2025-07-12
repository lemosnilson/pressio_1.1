from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from engine.pressio_engine import realizar_analise_completa


# --- VIEWS DO FLUXO DE INSERÇÃO DE DADOS ---

@login_required
def insercao(request):
    """Passo 1: Coleta dados da Grua e do Solo."""
    if request.method == 'POST':
        request.session['c'] = request.POST.get('c')
        request.session['p_tf'] = request.POST.get('p_tf')
        request.session['qa'] = request.POST.get('qa')
        return redirect('insercao_mats')
    return render(request, 'pages/insercao.html')

@login_required
def insercao_mats(request):
    """Passo 2: Coleta dados Geométricos dos Mats."""
    if request.method == 'POST':
        request.session['l_real'] = request.POST.get('l_real')
        request.session['b'] = request.POST.get('b')
        request.session['d'] = request.POST.get('d')
        return redirect('insercao_props')
    return render(request, 'pages/insercao_mats.html')

@login_required
def insercao_props(request):
    """Passo 3: Coleta dados das Propriedades Mecânicas."""
    if request.method == 'POST':
        request.session['densidade'] = request.POST.get('densidade')
        request.session['fb'] = request.POST.get('fb')
        request.session['fv'] = request.POST.get('fv')
        request.session['e_gpa'] = request.POST.get('e_gpa')
        return redirect('revisao')
    return render(request, 'pages/insercao_props.html')

# --- VIEWS DE REVISÃO E CÁLCULO ---

@login_required
def revisao_dados_view(request):
    """Passo 4: Junta todos os dados da sessão para mostrar na página de revisão."""
    context = {
        'c': request.session.get('c'),
        'p_tf': request.session.get('p_tf'),
        'qa': request.session.get('qa'),
        'l_real': request.session.get('l_real'),
        'b': request.session.get('b'),
        'd': request.session.get('d'),
        'densidade': request.session.get('densidade'),
        'fb': request.session.get('fb'),
        'fv': request.session.get('fv'),
        'e_gpa': request.session.get('e_gpa'),
    }
    return render(request, 'pages/revisao_dados.html', context)

@login_required
def calcular_view(request):
    """
    Esta view é o ponto final do fluxo. Ela é acionada pelo botão "Calcular"
    da página de revisão e é responsável por executar a análise.
    """
    # Garante que esta view só seja acessada via POST (formulário)
    if request.method == 'POST':
        # 1. Coleta os dados do formulário de revisão.
        dados_para_engine = request.POST.dict()

        # 2. Envia os dados para o nosso motor de cálculo para fazer a análise completa.
        resultados = realizar_analise_completa(dados_para_engine)

        # 3. Guarda os resultados na sessão para serem exibidos na página seguinte.
        #    Isso evita que os dados se percam se o usuário atualizar a página de resultados.
        request.session['resultados_finais'] = resultados
        
        # 4. Redireciona o usuário para a URL final que irá exibir os resultados.
        return redirect('resultados')
    
    # Se alguém tentar acessar a URL /calcular diretamente (via GET),
    # redirecionamos para o início do fluxo para evitar erros.
    return redirect('insercao')

@login_required
def resultados_view(request):
    """Exibe a página final com os resultados da análise."""
    resultados = request.session.get('resultados_finais', {})
    return render(request, 'pages/resultados.html', {'resultados': resultados})

# --- Outras Views ---
def index(request):
    return redirect('login')

def under_construction(request):
    return render(request, 'pages/under_construction.html')

# A view de registro não foi fornecida, então mantenho um placeholder
def register_view(request):
    # Sua lógica de registro aqui
    pass