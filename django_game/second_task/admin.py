from django.contrib import admin

from .models import Player, Level, Prize, PlayerLevel, LevelPrize, PlayerPrize

admin.site.register(Player)
admin.site.register(Level)
admin.site.register(Prize)
admin.site.register(PlayerLevel)
admin.site.register(LevelPrize)
admin.site.register(PlayerPrize)
