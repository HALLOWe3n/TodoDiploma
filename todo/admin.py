from django.contrib import admin

# Register your models here.
from todo.models import Profile, Todo, Board, TypeBoiler


@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Todo)
class TodoModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Board)
class BoardModelAdmin(admin.ModelAdmin):
    pass


@admin.register(TypeBoiler)
class TypeBoilerModelAdmin(admin.ModelAdmin):
    pass
