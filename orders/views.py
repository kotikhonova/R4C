from django.http import HttpResponse
from .models import Order


def send_message(model, version, customer):
    answer = f'Добрый день! \
            Недавно вы интересовались нашим роботом модели {model}, версии {version}. \
            Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами'


def create_order(robot_serial, customer):
    order = Order(customer=customer, robot_serial=robot_serial)
    return HttpResponse(201) if order.save() else HttpResponse(400)


def find_order(robot_serial):
    order = Order.objects.filter(robot_serial=robot_serial)[0]
    if order:
        send_message(order.model, order.version, order.customer)
        order.delete()
        return HttpResponse(200)
    return False
