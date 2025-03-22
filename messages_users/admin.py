from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'subject', 'timestamp')  # Affiche ces colonnes dans l'admin
    search_fields = ('email', 'subject', 'message')  # Permet de rechercher par email ou sujet
    list_filter = ('timestamp',)  # Ajoute un filtre par date

