import xlwt
import os
import xlrd
from xlutils.copy import copy as xl_copy

def storeData(routes, distances, time, autonomy, name, instance):
    wb = None
    if(os.path.isfile("results/mtVRP_DavidCalleGonzalez_" + name + ".xls")):
        rb = xlrd.open_workbook("results/mtVRP_DavidCalleGonzalez_" + name + ".xls", formatting_info=True)
        wb = xl_copy(rb)
    else:
        wb = xlwt.Workbook("results/mtVRP_DavidCalleGonzalez_" + name + ".xls")
    sheet = wb.add_sheet(instance)
    feasable = 0
    for i in range(len(routes)):
        sheet.write(i, len(routes[i]), distances[i])
        localFeasable = 0 if distances[i] <= autonomy else 1
        feasable = feasable or localFeasable
        sheet.write(i, len(routes[i])+1, localFeasable)
        for j in range(len(routes[i])):
            sheet.write(i, j, routes[i][j])
    sheet.write(len(routes), 0, round(sum(distances), 2))
    sheet.write(len(routes), 1, round(time, 3))
    sheet.write(len(routes), 2, feasable)
    wb.save("results/mtVRP_DavidCalleGonzalez_" + name + ".xls")