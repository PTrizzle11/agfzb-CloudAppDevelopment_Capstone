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


class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip, state):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
        # Dealer state long
        self.state = state

    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, id, sentiment="neutral"):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id
