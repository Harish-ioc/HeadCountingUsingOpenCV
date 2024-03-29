from django.db import models
from django.utils import timezone



class Block(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Create your models here.
class Camera(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name="cameras", null=True)
    name = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    usr = models.CharField(max_length=200)
    pwd = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    def get_data_in_range(self, start_date, end_date, period='p1'):
        data = self.data.filter(
            date__date__range=[start_date, end_date],
            # period=period
        )
        return data
    
    def today(self):
        today = timezone.now()
        info = self.data.filter(date__date=today)
        a = list("-"*10)
        for i in info:
            print(int(i.period[-1])-1, i.period)
            a[int(i.period[1:])-1] = i.count
        
        return a

class Data(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    period = models.CharField(max_length=50)
    cam = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name="data")
    count = models.IntegerField()


class Snaps(models.Model):
    min_hour = models.IntegerField()
    max_hour = models.IntegerField()

class Minutes(models.Model):
    snap = models.ForeignKey(Snaps, on_delete=models.CASCADE, related_name='minutes')
    minute = models.IntegerField()

class Seconds(models.Model):
    snap = models.ForeignKey(Snaps, on_delete=models.CASCADE, related_name='second')
    second = models.IntegerField()

class TimePeriod(models.Model):
    snap = models.ForeignKey(Snaps, on_delete=models.CASCADE, related_name='timeperiod')
    period = models.CharField(max_length=10)
    take_shot = models.TimeField(null=True)
    hour = models.IntegerField()
