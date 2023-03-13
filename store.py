import xlwt

filename = "entrega1.xls"

def storeData(route, distances, time):
    wb = xlwt.Workbook(filename)
    newSheet = wb.add_sheet("Constructive")
    for i in range(len(route)):
        for j in range(len(route[i])):
            newSheet.write(i, j, route[i][j])
    wb.save(filename)
