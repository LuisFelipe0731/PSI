from django.contrib import admin #isso já vai estar existindo no arquivo

from .models import * #imporata nossos models
admin.site.register(Fabricante) #adiciona a interface do adm
