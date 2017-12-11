import time, datetime
ts = time.strftime("%H:%M:%S", time.gmtime())
def getSec(s):
    l = s.split(':')
    return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])
username = "lewis"
limit = 5

floodPrevention = {}
#if message sent to box:
if username in floodPrevention:
    if getSec(time.strftime("%H:%M:%S", time.gmtime()))- floodPrevention[username] >= limit:
        #message sent
        floodPrevention[username] = getSec(time.strftime("%H:%M:%S", time.gmtime()))
    else:
        #wait message
else:
    #message sent
    floodPrevention[username] = getSec(time.strftime("%H:%M:%S", time.gmtime()))
    

#if message sent to box:
if username in floodPrevention:
    time.sleep(6)
    if getSec(time.strftime("%H:%M:%S", time.gmtime()))- floodPrevention[username] >= limit:
        #message updates
        floodPrevention[username] = getSec(time.strftime("%H:%M:%S", time.gmtime()))
    else:
        print("Wait!!!")
else:
    #message updates
    floodPrevention[username] = getSec(time.strftime("%H:%M:%S", time.gmtime()))
    print("2")
