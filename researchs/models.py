from django.db import models

# Create your models here.
class Researchers(models.Model):
    id = models.UUIDField(primary_key=True)

    class Meta:
        db_table = 'researchers'

class Researchdata(models.Model):
    dob = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    postal_code = models.TextField(blank=True, null=True)
    list_of_vaccines = models.TextField(blank=True, null=True)
    last_close_contact = models.TextField(blank=True, null=True)
    last_infected_date = models.TextField(blank=True, null=True)
    total_infection = models.BigIntegerField(blank=True, null=True)
    total_close_contact_as_infected = models.BigIntegerField(blank=True, null=True)
    total_close_contact_with_infected = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'researchdata'