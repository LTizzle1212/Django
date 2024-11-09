from django.db import models

# Create your models here.

class Place(models.Model):
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}, visited? {self.visited}' 
    # When in the django app, this is what is displayed on the places
    
    # This will create a place model for the database