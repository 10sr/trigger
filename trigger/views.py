from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .pushbullet import PushBullet

def index(req):
    return HttpResponse("""
    hello
    <a href="note">note</a>
    """)


def note_from_web(req):
    tpl = loader.get_template("trigger/note_from_web.html.dtl")
    return HttpResponse(tpl.render({}, req))


def note_from_web_post(req):
    try:
        body = req.POST["body"]
    except KeyError:
        return HttpResponseBadRequest("Body not given")

    pb = PushBullet(settings)
    ret = pb.push_note(body)
    # print(ret)

    return HttpResponseRedirect(reverse("trigger:note_from_web"))
