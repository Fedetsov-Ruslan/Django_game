from django.contrib import admin

from .models import Player, UserLogin, Boosts, BostsPlayer

admin.site.register(Player)
admin.site.register(UserLogin)
admin.site.register(Boosts)
admin.site.register(BostsPlayer)

