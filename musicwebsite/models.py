from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# This is the defined 'Song' model 
class Song(models.Model):
    
    # This is the Forgeign Key to User aspect of the model
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # These are the fields related to the 'Song' model
    title = models.CharField(max_length=50)

    def __str__(self):
        return super().__str__()

# This is the defined 'Chord' model
class Chord(models.Model):

    # This is the Forgeign Key to user aspect of the model
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # These are the fields related to the 'Chord' model
    name = models.CharField(max_length=50)
    base = models.IntegerField()
    frets = models.JSONField()
    fingers = models.JSONField()
    isCustom = models.BooleanField(db_default = False)

    def __str__(self):
        return self.name


# This is the defined 'SongChord' model
class SongChord(models.Model):

    # These are the Forgeign Keys to the Song and Chord Models
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    chord = models.ForeignKey(Chord, on_delete=models.CASCADE)

    # These are the fields related to the 'SongChord' model
    position = models.IntegerField()
    length = models.IntegerField()

    def __str__(self):
        return super().__str__()

