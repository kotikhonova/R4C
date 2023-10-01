from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from robots.models import Robot
from orders.views import find_order
import json
from openpyxl import Workbook
from datetime import timedelta



@csrf_exempt
def add_robot(request):
    if request.method == 'POST':
        info = json.loads(request.body.decode("utf-8"))
        robot = Robot(**info)
        if robot.save():
            find_order(info.serial)
            return HttpResponse(201)
        return HttpResponse(304)
    return HttpResponse(400)


def download_excel(request):
    if request.method == 'GET':
        wb = Workbook()
        sheet_names = set(Robot.objects.values_list('model'))
        header = [f.name.capitalize() for f in Robot._meta.get_fields()]
        for sheet_name in sheet_names:
            ws = wb.create_sheet(sheet_name[0])
            for index, item in enumerate(header, 1):
                cell = ws.cell(row=1, column=index)
                cell.value = item
            for row in Robot.objects.filter(model=sheet_name[0]).values():
                start = row['created'].date() - timedelta(days=7)
                today = row['created'].date()
                row['created'] = Robot.objects.filter(created__range=[start, today]).count()
                ws.append([row[x] for x in row])

        wb.save('output.xlsx')
        return HttpResponse(header)

        # for row in ws.iter_rows(min_row=1, max_col=len(header)):
           #     pass



        # ws = wb.active


