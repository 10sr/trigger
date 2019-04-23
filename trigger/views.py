from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from .pushbullet import PushBullet

def index(req):
    return HttpResponse("""
    hello
    <a href="note">note</a>
    """)


def note_from_web(req):
    pb = PushBullet(settings)
    ret = pb.push_note("note_from_web")
    print(ret)
    return HttpResponse(f"hoehoe {ret}")
