import json
from django.core.management.base import BaseCommand
from musicwebsite.models import Chord
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Load chord data from JSON file'

    def handle(self, *args, **kwargs):
        # Open and read the JSON file
        with open('musicwebsite/static/guitar_chords.json', 'r') as f:
            chord_data = json.load(f)  # Load JSON data into a Python list

            # Find the user to associate the chords with (for example, admin user)
            try:
                user = User.objects.get(username='admin')  # Adjust this to your needs
            except User.DoesNotExist:
                user = User.objects.create_superuser(username='admin', email='admin@example.com', password='your_password')
                self.stdout.write(self.style.SUCCESS('Admin user created'))

            # Iterate over each chord in the data
            for chord in chord_data:
                # Create a new Chord object for each entry in the JSON
                Chord.objects.create(
                    name=chord['name'],
                    base=chord['base'],
                    frets=chord['frets'],  # This is a list, thanks to JSONField
                    fingers=chord['fingers'],  # Another list from JSONField
                    user=user  # Associate the chord with a specific user
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded chord data'))