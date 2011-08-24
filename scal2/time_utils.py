import time
from time import localtime
import datetime

from scal2.cal_modules.gregorian import J1970

## time() ~~ epoch
## jd == epoch/(24*3600.0) + J1970
## epoch == (jd-J1970)*24*3600
getJdFromEpoch = lambda epoch: int(epoch//(24*3600) + J1970)

getEpochFromJd = lambda jd: (jd-J1970)*(24*3600)

def getJhmsFromEpoch(epoch, local=False):## return a tuple (julain_day, hour, minute, second) from epoch
    #if local:
    #    epoch -= getCurrentTimeZone()
    (days, second) = divmod(epoch, 24*3600)
    (minute, second) = divmod(second, 60)
    (hour, minute) = divmod(minute, 60)
    return (days + J1970, hour, minute, second)

def getSecondsFromHms(hour, minute, second):
    return hour*3600 + minute*60 + second

getEpochFromJhms = lambda jd, hour, minute, second: getEpochFromJd(jd) + getSecondsFromHms(hour, minute, second)

def getJdAndSecondsFromEpoch(epoch):## return a tuple (julain_day, extra_seconds) from epoch
    (days, second) = divmod(epoch, 24*3600)
    return (days + J1970, second)

getTimeZoneByEpoch = lambda epoch: (datetime.datetime.fromtimestamp(epoch) - datetime.datetime.utcfromtimestamp(epoch)).seconds

getTimeZoneByJd = lambda jd: getTimeZoneByEpoch(getEpochFromJd(jd))

getCurrentTimeZone = lambda: getTimeZoneByEpoch(time.time())
#getCurrentTimeZone = lambda: -time.altzone if time.daylight and localtime().tm_isdst else -time.timezone

