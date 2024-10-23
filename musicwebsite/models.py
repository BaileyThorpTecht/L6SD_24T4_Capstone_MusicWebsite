from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# This is the defined 'Song' model 
class Song(models.Model):
    
    # This is the Forgeign Key to User aspect of the model
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs')

    # These are the fields related to the 'Song' model
    title = models.CharField(max_length=50)

    # These are Timestaps for when the song was created or updated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return super().__str__()

# This is the defined 'Chord' model
class Chord(models.Model):

    # This is the Forgeign Key to user aspect of the model
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chords')

    # These are the fields related to the 'Chord' model
    notes = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    iscustom = models.BooleanField()
    fingerpositions = models.JSONField()

    def __str__(self):
        return f"{self.name} : {self.notes}"


# This is the defined 'SongChord' model
class SongChord(models.Model):

    # These are the Forgeign Keys to the Song and Chord Models
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='songchords')
    chord = models.ForeignKey(Chord, on_delete=models.CASCADE, related_name='songchords')

    # These are the fields related to the 'SongChord' model
    position = models.IntegerField()
    length = models.IntegerField()

    def __str__(self):
        return super().__str__()
    