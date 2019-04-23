from django.shortcuts import render
from django.http import HttpResponse

def index(req):
    return HttpResponse("""
    hello
    <a href="note">note</a>
    """)


def note_from_web(req):
    return HttpResponse("hoehoe")
