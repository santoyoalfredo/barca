from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Fixture, TeamStanding

@receiver(post_delete, sender=Fixture)
def updateStandings(sender, instance, **kwargs):
	TeamStanding.objects.save_standing(instance.season, instance.home_team)
	TeamStanding.objects.save_standing(instance.season, instance.away_team)
