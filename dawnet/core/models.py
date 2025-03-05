from django.db import models


from django.contrib.auth.models import AbstractUser
from django.db import models



# Create your models here.

class Capital(models.Model):
    amount = models.CharField(max_length=100, null=True)
    reason = models.CharField(max_length=100, null=True)
    method = models.CharField(max_length=100, null=True)
    date = models.CharField(max_length=100, null=True)
    time = models.CharField(max_length=100, null=True)
    created_date = models.CharField(max_length=100, null=True)
    created_by = models.CharField(max_length=100, null=True)

class Loan(models.Model):
    amount = models.CharField(max_length=100, null=True)
    reason = models.CharField(max_length=100, null=True)
    method = models.CharField(max_length=100, null=True)
    date = models.CharField(max_length=100, null=True)
    time = models.CharField(max_length=100, null=True)
    created_date = models.CharField(max_length=100, null=True)
    created_by = models.CharField(max_length=100, null=True)


class Income(models.Model):
    amount = models.CharField(max_length=100, null=True)
    reason = models.CharField(max_length=100, null=True)
    method = models.CharField(max_length=100, null=True)
    date = models.CharField(max_length=100, null=True)
    time = models.CharField(max_length=100, null=True)
    created_date = models.CharField(max_length=100, null=True)
    created_by = models.CharField(max_length=100, null=True)

class Bank_Credit(models.Model):
    amount = models.CharField(max_length=100, null=True)
    reason = models.CharField(max_length=100, null=True)
    
    date = models.CharField(max_length=100, null=True)
    time = models.CharField(max_length=100, null=True)
    created_date = models.CharField(max_length=100, null=True)
    created_by = models.CharField(max_length=100, null=True)


class Bank_Debit(models.Model):
    amount = models.CharField(max_length=100, null=True)
    reason = models.CharField(max_length=100, null=True)
    
    date = models.CharField(max_length=100, null=True)
    time = models.CharField(max_length=100, null=True)
    created_date = models.CharField(max_length=100, null=True)
    created_by = models.CharField(max_length=100, null=True)


class Cash_Credit(models.Model):
    amount = models.CharField(max_length=100, null=True)
    reason = models.CharField(max_length=100, null=True)
    
    date = models.CharField(max_length=100, null=True)
    time = models.CharField(max_length=100, null=True)
    created_date = models.CharField(max_length=100, null=True)
    created_by = models.CharField(max_length=100, null=True)


class Cash_Debit(models.Model):
    amount = models.CharField(max_length=100, null=True)
    reason = models.CharField(max_length=100, null=True)
    
    date = models.CharField(max_length=100, null=True)
    time = models.CharField(max_length=100, null=True)
    created_date = models.CharField(max_length=100, null=True)
    created_by = models.CharField(max_length=100, null=True)

class Expense(models.Model):
    amount = models.CharField(max_length=100, null=True)
    reason = models.CharField(max_length=100, null=True)
    method = models.CharField(max_length=100, null=True)
    date = models.CharField(max_length=100, null=True)
    time = models.CharField(max_length=100, null=True)
    created_date = models.CharField(max_length=100, null=True)
    created_by = models.CharField(max_length=100, null=True)

class Purchase(models.Model):
    amount = models.CharField(max_length=100, null=True)
    reason = models.CharField(max_length=100, null=True)
    method = models.CharField(max_length=100, null=True)
    date = models.CharField(max_length=100, null=True)
    time = models.CharField(max_length=100, null=True)
    created_date = models.CharField(max_length=100, null=True)
    created_by = models.CharField(max_length=100, null=True)

class Asset(models.Model):
    amount = models.CharField(max_length=100, null=True)
    reason = models.CharField(max_length=100, null=True)
    method = models.CharField(max_length=100, null=True)
    decrease = models.CharField(max_length=100, null=True)
    date = models.CharField(max_length=100, null=True)
    time = models.CharField(max_length=100, null=True)
    created_date = models.CharField(max_length=100, null=True)
    created_by = models.CharField(max_length=100, null=True)

