from django.shortcuts import render
from . models import *
import threading
import time

from .yolo import dict_in_list_out
import datetime

def reading(num):
    print("starting")

    while(True):

        a = Snaps.objects.get(id=1)

        minMax_hour=[a.min_hour, a.max_hour]  # [minimum, maximux]

        # time_period={8:'P1',9:'P2',10:'P3',11:'P4',12:'P5',13:'P6',14:'P7',15:'P8',16:'P9',17:'P10'}
        time_period={}

        event=TimePeriod.objects.all()

        take_shot=[event.take_shot for event in event]

        hr = [time.hour for time in take_shot]
        mi = [time.minute for time in take_shot]

        combined = list(zip(hr,mi))

        # print(hr,mi)

        # print(take_shot)

        # print(time_period)

        t = a.timeperiod.all()
        for ti in t:
            time_period[ti.take_shot] = ti.period

        # print(time_period)

        allcam = Camera.objects.all()
        current_time=datetime.datetime.now().time()

        # print(type(current_time))
        # print(type(take_shot))
        # print(time_period)

        if (current_time.hour>=minMax_hour[0] and current_time.hour<minMax_hour[-1]) and ((current_time.hour,current_time.minute) in combined) and (current_time.second==0):
            print('great')
            for cam in allcam:
                input_dict={cam.ip:[cam.usr,cam.pwd]}

                count=dict_in_list_out.count(input_dict)
                if len(count)==0:
                    continue 

                print(cam)
                print("count : ",count)
                dobj = Data(period=time_period[datetime.time(current_time.hour,current_time.minute)], cam=cam, count=count[0])
                dobj.save()
                # print("HIIIII")

t1 = threading.Thread(target=reading, args=(10,))
# try:
#     print("Raw Start")
#     t1.start()
# except:
#     pass

# Create your views here.
def index(r, ids=1):
    block = Block.objects.get(id=ids)
    data = {'data': block.cameras.all(), 'blocks':Block.objects.all()}
    print(data)
    # objects_created_today = MyModel.objects.filter(created_at__date=today)
    try:
        t1.start()
    except:
        pass
    return render(r, 'index.html', data)

