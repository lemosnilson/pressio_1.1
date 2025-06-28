from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm  # Importa o formulário customizado


def index(request):
    # Página inicial do tema
    return render(request, 'pages/index.html', {'segment': 'dashboard'})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        # Verifica se o usuário marcou o checkbox de termos
        if not request.POST.get('terms'):
            messages.error(
                request,
                "Você precisa concordar com os Termos e Condições para se cadastrar."
            )
            return render(request, 'register.html', {'form': form})
        # Se marcou, prossegue com a validação do form
        if form.is_valid():
            form.save()
            return redirect('login')  # Redireciona para login após cadastro bem-sucedido
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
