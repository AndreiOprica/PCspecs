from django.db import models

class Comp(models.Model):
    username = models.CharField(max_length=255)
    architecture = models.CharField(max_length=255)
    systemname = models.CharField(max_length=255)
    nocores = models.CharField(max_length=255)
    nothreads = models.CharField(max_length=255)
    maxfrq = models.CharField(max_length=255)
    minfrq = models.CharField(max_length=255)
    memory = models.CharField(max_length=255)
    memoryavailable = models.CharField(max_length=255)
    memoryused = models.CharField(max_length=255)
