from django.db import models
from django.contrib import admin
from apps.common.models import BaseMetaModel
from django.core.validators import MaxValueValidator,MinValueValidator,RegexValidator
# Create your models here.
class Manufacturer(BaseMetaModel):
    gstin_regex = RegexValidator(regex=r'^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}$', message="Invalid GST Number. Correct Format is: XXAAAAAAAAAABZN(X:state code,A:Pan Number,B(Entity Number),N(Checksum digit)")
    
    full_name = models.CharField("Official Name", max_length=50)
    common_name = models.CharField("Common Name",null=True,blank=True , max_length=50)
    gstin =  models.CharField(validators=[gstin_regex], max_length=15) 
    @property
    @admin.display(
        ordering='full_name',
        description='Organization Name',
    )
    def  name(self):
        if self.common_name is None or len(self.common_name)==0:
            return self.full_name
        return self.common_name
    
    def __str__(self) -> str:
        return self.name

class ManufacturerContact(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


    manufacturer= models.OneToOneField(Manufacturer, related_name=("contact"), on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(null=True, blank=True, max_length=100)
    city  = models.CharField(max_length=50)
    pin = models.IntegerField(max_length=6, null=True,blank=True,validators=[MinValueValidator(100000), MaxValueValidator(999999)])
    contact_1  = models.CharField("Phone Number",validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    contact_2  = models.CharField("Alternate Phone Number",validators=[phone_regex], max_length=17, blank=True) # validators should be a list

    @property
    def address(self):
        return f"""
            {self.address_line_1}\n
            {self.address_line_2}\n
            {self.city}, {self.pin}
        """


class Item(BaseMetaModel):
    name = models.CharField( max_length=50)
    weight_unit_choices=(
        ("mg","mg"),
        ("ml","ml"),
        ("gm","gm"),
    )
    weight_unit= models.CharField(choices=weight_unit_choices, max_length=2, default="mg")
    weight = models.DecimalField("Quantity(in mg/ml)", max_digits=5, decimal_places=2)
    MRP = models.DecimalField("Quantity(in mg/ml)", max_digits=6, decimal_places=2)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    @property
    def full_name(self):
        return f"{self.name}-{self.weight}-{self.weight_unit}".upper()
        
    def __str__(self):
        return self.full_name
    


class Inventory(BaseMetaModel):
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    quantity= models.PositiveIntegerField(default = 0)
    

    def reduce_item(self,qty):
        if self.quantity < qty:
            raise "Only {} are available in the inventory"
