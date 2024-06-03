from django.contrib import admin
from .models import Shampoo, Scrub, FaceCleanser, BodySoap, LiquidSoap, Oil

class AbstractProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'weight')

admin.site.register(Shampoo, AbstractProductAdmin)
admin.site.register(Scrub, AbstractProductAdmin)
admin.site.register(FaceCleanser, AbstractProductAdmin)
admin.site.register(BodySoap, AbstractProductAdmin)
admin.site.register(LiquidSoap, AbstractProductAdmin)
admin.site.register(Oil, AbstractProductAdmin)
