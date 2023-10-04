from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from robots.models import Robot
from orders.views import find_order

import json
from openpyxl import Workbook
from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import Count, Q


@csrf_exempt
def add_robot(request):
    if request.method == 'POST':
        info = json.loads(request.body.decode("utf-8"))
        info['created'] = datetime.strptime(info['created'], '%Y-%m-%d %H:%M:%S')
        robot = Robot(**info)

        if robot.save():
            find_order(info.serial)
            return HttpResponse(201)
        return HttpResponse(304)
    return HttpResponse(400)


def download_excel(request):
    if request.method == 'GET':
        wb = Workbook()
        header = Robot.header()
        today = datetime.now(tz=timezone.utc)
        start = today - timedelta(today.weekday())
        end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)

        for sheet_name in set(Robot.objects.values_list('model')):
            ws = wb.create_sheet(sheet_name[0])
            for index, item in enumerate(header, 1):
                cell = ws.cell(row=1, column=index)
                cell.value = item

        created = Robot.objects.values('model', 'version').annotate(total=Count('version')).filter(created__gte=start, created__lte=end)
        for item in created:
            ws.append([item['model'], item['version'], item['total']])

        wb.save('output.xlsx')
        return HttpResponse(created)
