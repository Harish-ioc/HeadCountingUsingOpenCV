from django.db import models
from django.contrib.auth.models import User
from process.models import Camera



class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
class Teacher(models.Model):
    name = models.CharField(max_length=100, unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    
    def get_full_name(self):
        return self.name + " " + self.branch.name
    
    def __str__(self):
        return self.name + " " + self.branch.name

class Class(models.Model):
    course = models.CharField(max_length=100)
    section = models.CharField(max_length=10)
    semester = models.CharField(max_length=10)
    number_of_students = models.IntegerField(default=0)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="classes", null=True)
    
    def __str__(self) -> str:
        return self.course + " " + str(self.section) + " " + str(self.semester) 
    
    def get_name(self):
        return self.course + " " + str(self.section) + " " + str(self.semester) 

# Create your models here.
class TimeTable(models.Model):
    department = models.ForeignKey(User, on_delete=models.CASCADE, related_name="timetable")
    room = models.ForeignKey(Camera, on_delete=models.PROTECT, related_name="timetable")
    room_capacity = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.room.name
    
    def get_day(self, num):
        if num == 0:
            return self.monday.all()
        elif num == 1:
            return self.tuesday.all()
        elif num == 2:
            return self.wednesday.all()
        elif num == 3:
            return self.thursday.all()
        elif num == 4:
            return self.friday.all()
        elif num == 5:
            return self.saturday.all()
        else:
            return []

class Monday(models.Model):
    timetable=models.ForeignKey(TimeTable, on_delete=models.CASCADE, related_name='monday')
    class_name = models.ForeignKey(Class, on_delete=models.PROTECT, related_name='monday', null=True, blank=True)
    subject = models.CharField(max_length=100)
    # teacher = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, null=True)
    period = models.IntegerField()
    starts_at = models.TimeField()
    ends_at = models.TimeField()

    def __str__(self) -> str:
        return self.subject

class Tuesday(models.Model):
    timetable=models.ForeignKey(TimeTable, on_delete=models.CASCADE, related_name='tuesday')
    class_name = models.ForeignKey(Class, on_delete=models.PROTECT, related_name='tuesday', null=True, blank=True)
    subject = models.CharField(max_length=100)
    # teacher = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, null=True)
    period = models.IntegerField()
    starts_at = models.TimeField()
    ends_at = models.TimeField()

    def __str__(self) -> str:
        return self.subject
    
class Wednesday(models.Model):
    timetable=models.ForeignKey(TimeTable, on_delete=models.CASCADE, related_name='wednesday')
    class_name = models.ForeignKey(Class, on_delete=models.PROTECT, related_name='wednesday', null=True, blank=True)
    subject = models.CharField(max_length=100)
    # teacher = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, null=True)
    period = models.IntegerField()
    starts_at = models.TimeField()
    ends_at = models.TimeField()

    def __str__(self) -> str:
        return self.subject
    
class Thursday(models.Model):
    timetable=models.ForeignKey(TimeTable, on_delete=models.CASCADE, related_name='thursday')
    class_name = models.ForeignKey(Class, on_delete=models.PROTECT, related_name='thursday', null=True, blank=True)
    subject = models.CharField(max_length=100)
    # teacher = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, null=True)
    period = models.IntegerField()
    starts_at = models.TimeField()
    ends_at = models.TimeField()

    def __str__(self) -> str:
        return self.subject
    
class Friday(models.Model):
    timetable=models.ForeignKey(TimeTable, on_delete=models.CASCADE, related_name='friday')
    class_name = models.ForeignKey(Class, on_delete=models.PROTECT, related_name='friday', null=True, blank=True)
    subject = models.CharField(max_length=100)
    # teacher = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, null=True)
    period = models.IntegerField()
    starts_at = models.TimeField()
    ends_at = models.TimeField()

    def __str__(self) -> str:
        return self.subject
    
class Saturday(models.Model):
    timetable=models.ForeignKey(TimeTable, on_delete=models.CASCADE, related_name='saturday')
    class_name = models.ForeignKey(Class, on_delete=models.PROTECT, related_name='saturday', null=True, blank=True)
    subject = models.CharField(max_length=100)
    # teacher = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, null=True)
    period = models.IntegerField()
    starts_at = models.TimeField()
    ends_at = models.TimeField()

    def __str__(self) -> str:
        # return self.teacher.name + " - " + self.subject
        return self.subject
    

