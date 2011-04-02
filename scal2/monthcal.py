# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 Saeed Rasooli <saeed.gnu@gmail.com> (ilius)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/gpl.txt>.
# Also avalable in /usr/share/common-licenses/GPL on Debian systems
# or /usr/share/licenses/common/GPL3/license.txt on ArchLinux

from scal2.locale import rtl, rtlSgn
from scal2.locale import tr as _

from scal2 import core
from scal2.core import myRaise, numLocale, getMonthName, getMonthLen, getNextMonth, getPrevMonth, pixDir

from scal2 import ui

pluginName = 'MonthCal'

class MonthStatus(list): ## FIXME
    ## self[sy<6][sx<7] of cells
    ## list (of 6 lists, each containt 7 cells)
    def __init__(self, cellCache, year, month):
        self.year = year
        self.month = month
        self.monthLen = getMonthLen(year, month, core.primaryMode)
        self.offset = core.getWeekDay(year, month, 1)## month start offset
        self.weekNum = [core.getWeekNumber(year, month, 1+7*i) for i in range(6)]
        #########
        (startJd, endJd) = core.getJdRangeForMonth(year, month, core.primaryMode)
        tableStartJd = startJd - self.offset
        #####
        list.__init__(self, [
            [cellCache.getCell(tableStartJd + yPos*7 + xPos) for xPos in range(7)] \
            for yPos in range(6)
        ])
    #def getDayCell(self, day):## needed? FIXME
    #    (yPos, xPos) = divmod(day + self.offset - 1, 7)
    #    return self[yPos][xPos]


def setParamsFunc(cell):
    offset = core.getWeekDay(cell.year, cell.month, 1)## month start offset
    (yPos, xPos) = divmod(offset + cell.day - 1, 7)
    cell.monthPos = (xPos, yPos)
    ###
    """
    if yPos==0:
        cell.monthPosPrev = (xPos, 5)
    else:
        cell.monthPosPrev = None
    ###
    if yPos==5:
        cell.monthPosNext = (xPos, 0)
    else:
        cell.monthPosNext = None
    """
    ## instead of checking  drawing_cell.gray == 0  ,   check  drawing_cell.month == ui.cell.month

getMonthStatus = lambda year, month: ui.cellCache.getCellGroup(pluginName, year, month)
getCurrentMonthStatus = lambda: ui.cellCache.getCellGroup(pluginName, ui.cell.year, ui.cell.month)

########################

def getMonthDesc(status=None):
    if not status:
        status = getCurrentMonthStatus()
    first = None
    last = None
    for i in xrange(6):
        for j in xrange(7):
            c = status[i][j]
            if first:
                #if c.gray == 0:
                if c.month == status.month:
                    last = c
                else:
                    break
            else:
                #if c.gray == 0:
                if c.month == status.month:
                    first = c
                else:
                    continue
    text = ''
    for item in ui.shownCals:
        if text!='':
            text+='\n'
        mode = item['mode']
        module = core.modules[mode]
        if mode==core.primaryMode:
            (y, m) = first.dates[mode][:2] ## = (status.year, status.month)
            text += '%s %s'%(getMonthName(mode, m), numLocale(y))
        else:
            (y1, m1) = first.dates[mode][:2]
            (y2, m2) = last.dates[mode][:2]
            dy = y2 - y1
            if dy==0:
                dm = m2 - m1
            elif dy==1:
                dm = m2 + 12 - m1
                assert dm > 0
            else:
                raise RuntimeError('y1=%d, m1=%d, y2=%d, m2=%d'%(y1, m1, y2, m2))
            if dm==0:
                text += '%s %s'%(_(module.getMonthName(m1)), numLocale(y1))
            elif dm==1:
                if dy==0:
                    text += '%s %s %s %s'%(_(module.getMonthName(m1)), _('and'),\
                    _(module.getMonthName(m2)), numLocale(y1))
                else:
                    text += '%s %s %s %s %s'%(_(module.getMonthName(m1)), numLocale(y1),\
                    _('and'), _(module.getMonthName(m2)), numLocale(y2))
            elif dm==2:
                if dy==0:
                    text += '%s%s %s %s %s %s'%(_(module.getMonthName(m1)), _(','),\
                        _(module.getMonthName(m1+1)),_('and'),_(module.getMonthName(m2)),\
                        numLocale(y1))
                else:
                    if m1==11:
                        text += '%s %s %s %s %s %s %s'%(_(module.getMonthName(m1)),\
                            _('and'), _(module.getMonthName(m1+1)), numLocale(y1),\
                            _('and'), _(module.getMonthName(1)), numLocale(y2))
                    elif m1==12:
                        text += '%s %s %s %s %s %s %s'%(_(module.getMonthName(m1)),\
                            numLocale(y1), _('and'), _(module.getMonthName(1)),\
                            _('and'), _(module.getMonthName(2)), numLocale(y2))
    return text


########################
ui.cellCache.registerPlugin(pluginName, setParamsFunc, MonthStatus)




