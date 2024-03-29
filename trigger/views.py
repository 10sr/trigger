import html

from pprint import pformat

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.template import loader
from django.urls import reverse

from .pushbullet import PushBullet


def index(req: HttpRequest) -> HttpResponse:
    # print(settings.HANIHO)
    meta = ""
    if req.user.is_authenticated:
        meta = pformat(req.META)
    return HttpResponse(
        f"""
    hello
    <a href="note">note</a>
    <pre><code>{html.escape(meta)}</code></pre>
    """
    )


@login_required  # type: ignore   # disallow_untyped_decorators
def note_from_web(req: HttpRequest) -> HttpResponse:
    tpl = loader.get_template("trigger/note_from_web.html.dtl")
    return HttpResponse(tpl.render({}, req))


@login_required  # type: ignore   # disallow_untyped_decorators
def note_from_web_post(req: HttpRequest) -> HttpResponse:
    try:
        body = req.POST["body"]
    except KeyError:
        return HttpResponseBadRequest("Body not given")

    pb = PushBullet(settings)
    ret = pb.push_note(body)
    # print(ret)

    return HttpResponseRedirect(reverse("trigger:note_from_web"))
