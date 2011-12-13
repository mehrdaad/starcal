import os
from os.path import isfile, join

from scal2.paths import pixDir, confDir
from scal2.utils import getElementText
from scal2.locale_man import tr as _
from scal2 import event_man
from scal2 import ui

customFile = join(confDir, 'customday.xml')

customdayModes = (
    (_('Birthday'),         'event/birthday.png'),
    (_('Marriage Jubilee'), 'event/marriage.png'),
    (_('Obituary'),         'event/obituary.png'),
    (_('Note'),             'event/note.png'),
    (_('Task'),             'event/task.png'),
    (_('Alarm'),            'event/alarm.png'),
)

def loadCustomDB():
    from xml.dom.minidom import parse
    if not isfile(customFile):
        return []
    db = parse(customFile).documentElement.getElementsByTagName('day')
    customDB = []
    for record in db:
        item = {}
        for element in record.childNodes:
            if element.nodeType != element.TEXT_NODE:
                if element.nodeType != element.TEXT_NODE:
                    name, data = getElementText(element)
                    if name=='num':
                        sp = data.split('/')
                        item['month'] = int(sp[0])
                        item['day'] = int(sp[1])
                    elif name=='kind':
                        item['type'] = int(data)
                    elif name=='desc':
                        item['desc'] = data
        customDB.append(item)
    return customDB


def importAndDeleteCustomDB(mode, groupTitle):
    customDB = loadCustomDB()
    if customDB:
        group = event_man.EventGroup()
        group.mode = mode
        group.title = groupTitle
        for item in customDB:
            event = group.createEvent('yearly')
            event.mode = mode
            try:
                event.setMonth(item['month'])
                event.setDay(item['day'])
                event.summary = item['desc']## desc could be multi-line FIXME
                event.icon = join(pixDir, customdayModes[item['type']][1])
                group.append(event)
                event.saveConfig()
            except:
                myRaise()
            group.saveConfig()
        ui.eventGroups.append(group)
        ui.eventGroups.saveConfig()
    os.remove(customFile)

