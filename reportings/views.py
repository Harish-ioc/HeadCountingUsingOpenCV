from django.shortcuts import render, HttpResponse
from process.models import *
from . models import *
import json
from datetime import datetime, timedelta, time
from django.db.models import Q
from django.db.models.functions import ExtractWeekDay
from datetime import datetime, timedelta
import pandas as pd
from django.utils import timezone


# Create your views here.
def index(r):
    ids=1
    block = Block.objects.get(id=ids)
    data = {'data': block.cameras.all(), 'blocks':Block.objects.all()}
    # objects_created_today = MyModel.objects.filter(created_at__date=today)
    return render(r, 'reports.html', data)

def datacam(r, ids):
    block = Block.objects.get(id=int(ids))
    return render(r, "options.html", {'cams': block.cameras.all()})

def nums(r):
    if r.method=="POST":
        body_unicode = r.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        obj = Camera.objects.get(id=body_data['room'])
        date_string = body_data['sdate']
        sdate = datetime.strptime(date_string, '%Y-%m-%d').date()
        edate_string = body_data['edate']
        edate = datetime.strptime(edate_string, '%Y-%m-%d').date()
        aldata = obj.get_data_in_range(sdate, edate)
        delta = edate - sdate

        azdata = {}
        date = sdate
        timetables = obj.timetable.all()
    
        for i in range(0, delta.days+1):
            date = date+timedelta(days=1)
            day_of_week = (date.weekday() + 1) % 7
            shedule=False
            if len(timetables):
                timetable = timetables[0]
                shedule = timetable.get_day(day_of_week)
            nd = aldata.filter(date__date=date)
            if len(nd) > 0:
                actout = list("-"*10)
                for iod in nd:
                    actout[int(iod.period[1:])-1] = [iod.count]
                    if shedule:
                        for si in shedule:
                            if si.period == int(iod.period[1:]):
                                actout[int(iod.period[1:])-1].append(si)

                azdata[date] = actout        
            # azdata.append(aldata.filter(date__date=date))
        # print(date.day)
        print(azdata)
        return render(r, 'table.html', {'aldata': azdata, 'cam':obj.name})
    return HttpResponse("s")


def getDayData(cls, day):
    if day=="Monday":
        return cls.monday.all()
    elif day=="Tuesday":
        return cls.tuesday.all()
    elif day=="Wednesday":
        return cls.wednesday.all()
    elif day=="Thursday":
        return cls.thursday.all()
    elif day=="Friday":
        return cls.friday.all()
    else:
        return cls.saturday.all()

def getTable(start="2024-2-1", end="2024-2-10", teacher=''):
    compare_time = time(13, 9)
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    column_names = ['date', 'day', 'class', 'teacher', 'subject', 'batchsize', 'attendance', 'period', 'room', 'roomsize']
    
    current_date = start_date
    masterDF = pd.DataFrame(columns=column_names)
    while current_date <= end_date:
        aware_current_date = timezone.make_aware(current_date,  timezone=timezone.get_current_timezone())
        day_name = aware_current_date.strftime("%A")
        if day_name == "Sunday":
            current_date += timedelta(days=1)
            continue
        # print(day_name)
        # print(aware_current_date)
        allClasses = Class.objects.all()
        for each_class in allClasses:
            dayPeriods = getDayData(each_class, day_name)
            for eachPeriods in dayPeriods:
                batch = int(eachPeriods.starts_at > compare_time)
                dayData = eachPeriods.timetable.room.data.filter(period='P'+str((eachPeriods.period+(batch*5))),  date__range=[aware_current_date, aware_current_date+timedelta(days=1)])
                if len(dayData):
                    # print(dayData[0].count)
                    new_row = {"date": current_date.date(),
                            "day": day_name,
                            'class': each_class.get_name(),
                            'teacher': eachPeriods.teacher.get_full_name().lower(),
                            'subject': eachPeriods.subject.lower(),
                            'batchsize': each_class.number_of_students,
                            'attendance': dayData[0].count,
                            'period': eachPeriods.period + (batch*5),
                            'room': eachPeriods.timetable.room.name,
                            'roomsize': eachPeriods.timetable.room_capacity
                            }
                    masterDF.loc[len(masterDF)] = new_row
        
        # Process dayData here
        
        # Move to the next date
        current_date += timedelta(days=1)
    
    masterDF['batch_avg'] = (masterDF['attendance'] / masterDF['batchsize']) * 100
    masterDF['room_avg'] = (masterDF['attendance'] / masterDF['roomsize']) * 100
    
    avg_peak_days = masterDF.groupby('day')['batch_avg'].mean()
    avg_peak_hours = masterDF.groupby('period')['batch_avg'].mean()
    avg_class_presence = masterDF.groupby('class')['batch_avg'].mean()
    avg_teacher_presence = masterDF.groupby('teacher')['batch_avg'].mean()
    avg_room_occupancy = masterDF.groupby('room')['room_avg'].mean()
    
    teacher_subject_avg_batchsize = masterDF.groupby(['teacher', 'subject'])['batch_avg'].mean()
    teacher_subject_avg_batchsize = teacher_subject_avg_batchsize.reset_index()
    
    max_batch_avg = masterDF.groupby(['date', 'class'])['batch_avg'].max()
    max_batch_avg = max_batch_avg.reset_index()
    masterDF = masterDF.merge(max_batch_avg, on=['date', 'class'], suffixes=('', '_max'))
    masterDF.rename(columns={'batch_avg_max': 'max_reported'}, inplace=True)
    
    teacher_day_avg = masterDF.groupby(['teacher', 'day']).agg({'batch_avg': 'mean', 'max_reported': 'mean'})
    teacher_day_avg = teacher_day_avg.reset_index()

    # print(teacher_day_avg['batch_avg'])
    dashboards = {'class_result_table': avg_class_presence.sort_values(ascending=False).to_dict().items(),
            'room_result_table': avg_room_occupancy.sort_values(ascending=False).to_dict().items(),
            'teacher_result_table': avg_teacher_presence.sort_values(ascending=False).to_dict().items(),
            'days_report_table': list(avg_peak_days.reindex(day_order).to_dict().values()),
            'first_shift': list(avg_peak_hours[0:5].to_dict().values()),
            'second_shift': list(avg_peak_hours[5:].to_dict().values()),
            'from_date': start,
            'end_date': end
            }
    if teacher != '':
        t_specific = teacher_day_avg[teacher_day_avg['teacher'] == teacher]
        t_specific.set_index('day', inplace=True)
        t_specific = t_specific.reindex(day_order)
        t_specific.fillna(0, inplace=True)
        
        
        t_subject = teacher_subject_avg_batchsize[teacher_subject_avg_batchsize['teacher'] == teacher]
        print(t_subject)
        
        dashboards = {'class_result_table': avg_class_presence.sort_values(ascending=False).to_dict().items(),
            'room_result_table': avg_room_occupancy.sort_values(ascending=False).to_dict().items(),
            'teacher_result_table': avg_teacher_presence.sort_values(ascending=False).to_dict().items(),
            'subject_report_table': list(t_subject['batch_avg'].to_dict().values()),
            'subjects': list(t_subject['subject'].to_dict().values()),
            'first_shift': list(t_specific['max_reported'].to_dict().values()), #done
            'second_shift': list(t_specific['batch_avg'].to_dict().values()),  #done
            'y_max': max(max(list(t_specific['max_reported'].to_dict().values())), max(list(t_specific['batch_avg'].to_dict().values()))),
            'from_date': start, #done
            'end_date': end, #done
            'teacher_name': teacher  #done
            }
    return dashboards


def dayextract(eachClass, dayall, batchlist, roomList, teachersList, maximum_reported, peakHours, dayname, weeknum=2, datesorting=(False, '', '')):
    compare_time = time(13, 9)
    for mon in dayall:
        batch = int(mon.starts_at > compare_time)
        curPeriod = mon.period + (batch*5)
        if curPeriod==11:
            curPeriod=10
        
        if datesorting[0]:
            # print("here we go")
            dayData = mon.timetable.room.data.annotate(weekday=ExtractWeekDay('date')).filter(weekday=weeknum, period='P'+str(curPeriod), date__range=[datesorting[1], datesorting[2]])
        else:
            dayData = mon.timetable.room.data.annotate(weekday=ExtractWeekDay('date')).filter(weekday=weeknum, period='P'+str(curPeriod))
        if len(dayData)==0:
            continue
        
        if mon.period not in peakHours[batch]:
            peakHours[batch][mon.period] = []
        
        total = 0
        allmax = 0
        for edd in dayData:
            total+=edd.count
            if allmax<edd.count:
                allmax = edd.count
        avg = total/len(dayData)
        if eachClass.number_of_students == 0:
            eachClass.number_of_students = 40
            eachClass.save()
        batchP = (avg/eachClass.number_of_students)*100
        allmax = (allmax/eachClass.number_of_students)*100
        
        peakHours[batch][mon.period].append(batchP)
        batchlist[eachClass][dayname].append(batchP)
        if mon.timetable.room not in roomList:
            roomList[mon.timetable.room] = {}
        if dayname not in roomList[mon.timetable.room]:
            roomList[mon.timetable.room][dayname] = []
        roomList[mon.timetable.room][dayname].append((avg/mon.timetable.room_capacity)*100)
        
        if mon.teacher not in teachersList:
            teachersList[mon.teacher] = {'meta': {'subject': mon.subject}, 'metadata': {'subject': {}}}
        # if mon.subject not in teachersList[mon.teacher]['meta']['subject']:
        #     teachersList[mon.teacher]['meta']['subject'].append(mon.subject)
        if dayname not in teachersList[mon.teacher]:
            teachersList[mon.teacher][dayname] = []
        teachersList[mon.teacher][dayname].append((batchP))
        if mon.subject not in teachersList[mon.teacher]['metadata']['subject']:
            teachersList[mon.teacher]['metadata']['subject'][mon.subject.lower()] = []
        teachersList[mon.teacher]['metadata']['subject'][mon.subject.lower()].append(batchP)
    
    return batchlist, roomList, teachersList, peakHours, maximum_reported



def resultDashboard(r):
    final = getTable()
    # return render(r, "dashboard.html", {'class_result_table': sorted_items, "room_result_table": room_sorted_items, "teacher_result_table": teacherSorted, 'days_report_table':days_report_table,
    #                                     "first_shift": fphfinal, 'second_shift':sphfinal, 'from_date':"-", 'end_date':'-', "teachers": teacherDays.keys()})
    return render(r, "dashboard.html", final)

def customDashBoard(r):
    if r.method == "POST":
        sdate = r.POST['startdate']
        edate = r.POST['enddate']
        final = getTable(sdate, edate)
    return render(r, "dashboard.html", final)

def teachers(r, name):
    if r.method == "POST":
        sdate = r.POST['startdate']
        edate = r.POST['enddate']
        print("HELOoooooooo!")
        final = getTable(sdate, edate, teacher=name)
    else:
        final = getTable(teacher=name)
    return render(r, "teachers.html", final)