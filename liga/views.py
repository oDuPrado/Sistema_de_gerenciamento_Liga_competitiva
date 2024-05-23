# liga/views.py

from django.shortcuts import render, redirect  # Não se esqueça de importar redirect
from .forms import PlayerRegistrationForm
from django.contrib import messages
from .models import Tournament, Ranking, TournamentResult, Deck, Player
from .forms import PlayerRegistrationForm, TournamentRegistrationForm, TournamentResultForm, DeckRegistrationForm
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404
import csv
from django.http import HttpResponse
from django.db.models import Count
from django.db import models

def home(request):
    return render(request, 'home.html')

def tournament_day(request):
    # Obter todos os torneios
    tournaments = Tournament.objects.all()
    # Passar os torneios para o template
    return render(request, 'tournament_day.html', {'tournaments': tournaments})

def player_registration(request):
    if request.method == 'POST':
        form = PlayerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jogador cadastrado com sucesso!')
            return redirect('player_registration')
    else:
        form = PlayerRegistrationForm()
    return render(request, 'player_registration.html', {'form': form})

def register_tournament(request):
    if request.method == 'POST':
        form = TournamentRegistrationForm(request.POST)
        if form.is_valid():
            new_tournament = form.save()
            messages.success(request, 'Torneio cadastrado com sucesso!')
            # Aqui você redireciona para a próxima etapa, que seria selecionar jogadores
            return redirect('tournament_results', tournament_id=new_tournament.id)
    else:
        form = TournamentRegistrationForm()
    return render(request, 'tournament_registration.html', {'form': form})

def list_tournaments(request):
    tournaments = Tournament.objects.all()
    return render(request, 'list_tournaments.html', {'tournaments': tournaments})

def view_ranking(request):
    rankings = Ranking.objects.all().order_by('-total_points')
    return render(request, 'ranking.html', {'rankings': rankings})

def tournament_results(request, tournament_id):
    # Obtenha o objeto do torneio
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    
    # Calcule o número de formulários extras com base no número de jogadores e resultados existentes
    extra_forms = tournament.number_of_players - TournamentResult.objects.filter(tournament=tournament).count()
    extra_forms = max(0, extra_forms)
    
    # Crie o formset com o número correto de formulários extras
    TournamentFormSet = modelformset_factory(
        TournamentResult,
        form=TournamentResultForm,
        extra=extra_forms,
    )

    if request.method == 'POST':
        formset = TournamentFormSet(request.POST, queryset=TournamentResult.objects.filter(tournament=tournament))
        
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.tournament = tournament
                
                # Verifique se já existe um registro para o mesmo torneio e jogador
                existing_result = TournamentResult.objects.filter(tournament=tournament, player=instance.player).first()
                if existing_result:
                    existing_result.position = instance.position
                    existing_result.points = instance.points
                    existing_result.save()
                else:
                    instance.save()
                
                # Atualize ou crie o ranking do jogador
                ranking, created = Ranking.objects.get_or_create(player=instance.player)
                ranking.add_points(instance.points)
            
            # Atualize ou crie o registro na página "Dia de Torneio"
            tournament_day_record, created = Tournament.objects.get_or_create(
                pk=tournament_id,
                defaults={'name': tournament.tournament_type, 'date': tournament.date}
            )

            if not created:
                tournament_day_record.name = tournament.tournament_type
                tournament_day_record.date = tournament.date
                tournament_day_record.save()
                print(f"Registro atualizado - Nome: {tournament_day_record.name}, Data: {tournament.date}")
                
            messages.success(request, 'Resultados do torneio salvos com sucesso.')
            return redirect('view_ranking')
    else:
        formset = TournamentFormSet(queryset=TournamentResult.objects.filter(tournament=tournament))

    return render(request, 'tournament_results.html', {'formset': formset, 'tournament': tournament})

def export_rankings_csv(request):
    # Crie uma resposta HTTP com o cabeçalho de conteúdo correto
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rankings.csv"'

    # Crie um escritor CSV usando a resposta HTTP como arquivo
    writer = csv.writer(response)

    # Escreva o cabeçalho do CSV
    writer.writerow(['Posição', 'Nome do Jogador', 'Deck', 'Pontos'])

    # Busque os dados de ranking do seu modelo
    rankings = Ranking.objects.all().order_by('-total_points')

    # Escreva os dados no CSV usando o índice do loop como a posição
    for idx, rank in enumerate(rankings, 1):
        writer.writerow([idx, rank.player.name, 'Deck', rank.total_points])  # Substitua 'Deck' conforme necessário

    # Retorne a resposta HTTP com o CSV
    return response

from .forms import DeckRegistrationForm

def deck_registration(request):
    if request.method == 'POST':
        form = DeckRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_decks')  # Substitua pela URL de redirecionamento desejada
    else:
        form = DeckRegistrationForm()
    return render(request, 'deck_registration.html', {'form': form})

def view_decks(request):
    deck_stats = Deck.objects.annotate(num_players=models.Count('tournamentresult'))
    total_players = TournamentResult.objects.count()
    deck_stats = [{'name': deck.name, 'count': deck.num_players, 'percentage': (deck.num_players / total_players) * 100} for deck in deck_stats]
    return render(request, 'view_decks.html', {'deck_stats': deck_stats})

def view_players(request):
    players = Player.objects.all()
    return render(request, 'view_players.html', {'players': players})

def show_decks(request):
    decks = Deck.objects.all()
    for deck in decks:
        deck.special_info = deck.get_special_info()  # Utilizando o método que você adicionou
    return render(request, 'show_decks.html', {'decks': decks})



