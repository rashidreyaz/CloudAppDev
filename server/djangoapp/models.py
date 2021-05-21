from django.db import models
from django.utils.timezone import now

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='Tesla', editable=False)
    description = models.CharField(max_length=1000)
    def __str__(self):
        return "name: " + self.name + "," + \
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
    modelname = models.CharField(null=False, max_length=30, default='Tesla model S')
    dealer_id= models.IntegerField(null=False,  default=1)
    type = models.CharField(max_length=5, choices=TYPES, default=SEDAN)
    year =models.DateField(default=now)
    def __str__(self):
        return  "modelname: " + self.modelname + "," + \
                "CarMake: " + self.carmake+ ","+\
                "Dealer: " + self.dealer_id + "," + \
                "Type: " + self.type + "," + \
                "Year: "+ self.year


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
# class CarDealer(models.Model):
#     name = models.CharField(null=False, max_length=30, default='Best Dealer')
#     def __str__(self):
#         return  "Dealer: " + self.name

# <HINT> Create a plain Python class `DealerReview` to hold review data
# class DealerReview(models.Model):
# class DealerReview(models.Model):
#     name = models.CharField(null=False, max_length=30, default='Best')
#     def __str__(self):
#         return  "DealerReview: " + self.name
