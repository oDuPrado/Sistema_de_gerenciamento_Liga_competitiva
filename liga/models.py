# liga/models.py

from django.db import models
from django.core.validators import RegexValidator

# Validador para restringir caracteres especiais
alphanumeric_validator = RegexValidator(r'^[0-9a-zA-Z ]*$', 'Apenas letras, números e espaços são permitidos.')

class Player(models.Model):
    official_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    tournament_points = models.IntegerField(default=0)

    def update_points(self, points):
        self.tournament_points += points
        self.save()

    def __str__(self):
        return self.name

class TournamentType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Tournament(models.Model):
    name = models.CharField(max_length=100, validators=[alphanumeric_validator])
    tournament_type = models.CharField(max_length=100, validators=[alphanumeric_validator])
    date = models.DateField()
    number_of_rounds = models.IntegerField(default=1)
    number_of_players = models.IntegerField(default=1)
    results = models.TextField(blank=True, null=True)
    
    # Pode ser interessante ter um campo ManyToMany para jogadores para armazenar quem participou
    participants = models.ManyToManyField('Player', through='TournamentResult', related_name='tournaments_participated')
    
    def __str__(self):
        return self.name

class Deck(models.Model):
    name = models.CharField(max_length=100)  # Nome do deck
    image = models.ImageField(upload_to='deck_images/', default='default_deck_image.jpg')

    def __str__(self):
        return self.name

    def get_special_info(self):
        # Alguma lógica para retornar informações específicas
        return "Informação Especial"

class TournamentResult(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    position = models.IntegerField()  # 1º lugar, 2º lugar, etc.
    points = models.IntegerField()  # Pontos baseados na posição
    deck = models.ForeignKey(Deck, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('tournament', 'player')

class Ranking(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)  # Soma dos pontos de todos os torneios

    def add_points(self, points):
        self.total_points += points
        self.save()

