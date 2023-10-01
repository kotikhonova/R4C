from django.shortcuts import render
from orders.views import create_order
from robots.models import Robot
import json


def order(request):
    if request.method == 'GET':
        customer = request.user.email
        serial = json.loads(request.body.decode("utf-8"))
        result = Robot.objects.filter(**serial).count()
        if result:
            return create_order(serial, customer)
        return 200
    return 400
