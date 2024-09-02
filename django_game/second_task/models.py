import csv
import random
from django.db import models
from django.utils import timezone

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
    
    def get_player_level_data(self):
        player_prize_subquery = PlayerPrize.objects.filter(
            player=models.OuterRef('player'),
            prize__level=models.OuterRef('level')
        ).values('prize__prize__title')[:1]  

        queryset = PlayerLevel.objects.select_related('player', 'level').annotate(
            prize_title=models.Subquery(player_prize_subquery)
        ).values(
            'id',
            'player__player_id',
            'level__title',
            'is_completed',
            'prize_title'
        ).distinct()

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
