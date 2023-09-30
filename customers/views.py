from django.shortcuts import render
from orders.views import create_order
from robots.models import Robot
import json


def order(request):
    if request.method == 'GET':
        serial = json.loads(request.body.decode("utf-8"))
        result = Robot.objects.filter(**serial).count()
        customer = 'a@mail.ru'
        return create_order(serial, customer)
    else:
        pass
