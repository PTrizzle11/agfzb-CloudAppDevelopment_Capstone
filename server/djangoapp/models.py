from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length = 100, null = False)
    description = models.CharField(max_length=500)

    def __str__(self):
        return "Name: " + self.name + "," + \
        "Description: " + self.description

class CarModel(models.Model):
    SEDAN = "sedan"
    SUV = "suv"
    WAGON = "wagon"
    HATCHBACK = "hatchback"
    MODEL_CHOICES = [
        (SEDAN,"Sedan"),
        (SUV,"Suv"),
        (WAGON,"Wagon"),
        (HATCHBACK,"Hatchback")
    ]
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100, null = False)
    dealerid = models.IntegerField()
    Type = models.CharField(null=False,
    max_length=20,
    choices=MODEL_CHOICES,
    default=SEDAN
    )
    year = models.DateField(null=True)

    def __str__ (self):
        return "Name: " + self.name + "," + \
               "Dealer ID: " + str(self.dealerid) + "," + \
               "Type: " + self.Type + "," + \
               "Year: " + str(self.year)


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
