from django.db import models
from django.utils import timezone

class Player(models.Model):
    nickname = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)

    class Meta:
        ordering = ['id']
        verbose_name = 'игрок'
        verbose_name_plural = 'игроки'

    def __str__(self):
        return self.nickname


class UserLogin(models.Model):
    user = models.ForeignKey(Player, on_delete=models.CASCADE)
    login_date = models.DateField(default=timezone.now)


    class Meta:
        unique_together = ('user', 'login_date')
        ordering = ['-login_date']

class Boosts(models.Model):
    name = models.CharField(max_length=30)
    title = models.CharField(max_length=100)

class BostsPlayer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    boosts = models.ForeignKey(Boosts, on_delete=models.CASCADE)



