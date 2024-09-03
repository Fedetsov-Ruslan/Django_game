import csv
import random
from django.db import models
from django.utils import timezone
from django.db.models import F

class Player(models.Model):
    player_id = models.CharField(max_length=100)
    
    
class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    
    
    
class Prize(models.Model):
    title = models.CharField(max_length=100)
    
    
class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField()
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)

    # мутод получегия приза
    def assign_prize(self):
        if self.is_completed:
            level_prizes = LevelPrize.objects.filter(level=self.level)
        
            prize_count = level_prizes.count()
            if prize_count > 0:
                random_index = random.randint(0, prize_count - 1)
                random_prize = level_prizes[random_index]

                PlayerPrize.objects.create(
                    player=self.player,
                    prize=random_prize,
                    received=timezone.now().date()
                )
            print(f"Приз {random_prize.prize.title} получен игроком {self.player.player_id}  за прохождение уровня {self.level.title}")
    
    # метод получения данных
    def get_player_level_data(self):
        queryset = (
            Player.objects
            .prefetch_related(
                'playerlevel_set__level',  
                'playerprize_set__prize__levelprize__level'  
            )
            .annotate(
                level_title=F('playerlevel_set__level__title'),
                is_completed=F('playerlevel_set__is_completed'),
                prize_title=F('playerprize_set__prize__title')
            )
            .values(
                'player_id',
                'level_title',
                'is_completed',
                'prize_title'
            )
        )

        with open('data.csv', mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(['player_id', 'level_title', 'is_completed', 'prize_title'])

        while queryset.exists():
            batch = queryset[:1000]
            if not batch:
                break
            write_csv_data(batch)
            processed_ids = {record['id'] for record in batch}
            queryset = queryset.exclude(id__in=processed_ids)


    
class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField()


class PlayerPrize(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    prize = models.ForeignKey(LevelPrize, on_delete=models.CASCADE)
    received = models.DateField()

     


def write_csv_data(records):
    with open ('data.csv', mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        rows =[
            [
            record['player__player_id'],
            record['level__title'],
            record['is_completed'],
            record['prize_title']
        ]
        for record in records
        ]
        writer.writerows(rows)
