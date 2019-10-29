from django.contrib import admin
from .models import Beacon, ExtendedUser, Quest, QuestStep


@admin.register(Beacon)
class BeaconAdmin(admin.ModelAdmin):
    pass


@admin.register(ExtendedUser)
class ExtendedUserAdmin(admin.ModelAdmin):
    pass

# Quests


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    pass


@admin.register(QuestStep)
class QuestStepAdmin(admin.ModelAdmin):
    pass
