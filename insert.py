import xlrd 

loc = ("data.xls")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

for i in range(1,8):
    username = sheet.row_slice(i, 1,4)
    username, institution, password = sheet.row_slice(i, 1, 4)