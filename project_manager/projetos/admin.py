from django.contrib import admin

from .models import (
    Area,
    Responsavel,
    Projeto,
    Etapa
)

admin.site.register(Area)
admin.site.register(Responsavel)
admin.site.register(Projeto)
admin.site.register(Etapa)