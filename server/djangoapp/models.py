from django.db import models
from django.utils.timezone import now

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='')
    description = models.CharField(max_length=1000,default='')
    def __str__(self):
        return  "Name: " + self.name + "," + \
                "Description: " + self.description

# carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    TYPES=[ (SEDAN , 'sedan'),
            (SUV , 'suv'),
            (WAGON , 'wagon')]
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    # carmake = models.ManyToManyField(CarMake)
    dealer_id= models.IntegerField(null=False,  default=1)
    modelname = models.CharField(null=False, max_length=30, default='')
    type = models.CharField(max_length=5, choices=TYPES, default=SEDAN)
    year =models.DateField(default=now)
    def __str__(self):
        return  "modelname:" + self.modelname + "," + \
                "Type: " + self.type 


                # + "," + \
                # "Year: "+ self.year
                # "Dealer: " + self.dealer_id + "," + \
                # "CarMake: " + self.carmake+ ","+\
# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
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

    def __str__(self):
        return "Dealer_name: " + self.full_name + "," + \
            "Dealer_id: " + str(self.id)

# <HINT> Create a plain Python class `DealerReview` to hold review data
# class DealerReview(models.Model):
class DealerReview(models.Model):
    # car_make = models.CharField(null=False, max_length=30, default='Best')
    def __init__(self, car_make, car_model, car_year, dealership, id, name, purchase, purchase_date, review):
        self.car_make = car_make
        # Dealer city
        self.car_model = car_model
        # Dealer Full Name
        self.car_year = car_year
        # Dealer Full Name
        self.dealership = dealership
        # Dealer id
        self.id = id
        # Location lat
        self.name = name
        # Location long
        self.purchase = purchase
        # Dealer short name
        self.purchase_date = purchase_date
        # Dealer state
        self.review = review

    def __str__(self):
        return  "Dealer_Name: " + self.name + "," + \
             "Dealer_Review: " + self.review + "," + \
            "Dealer_id: " + str(self.id)
