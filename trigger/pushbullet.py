from typing import Any, Optional

import pushbullet as pb

from django.conf import LazySettings


class PushBullet:
    _token: str
    __pushbullet: Optional[pb.Pushbullet] = None

    @property
    def pushbullet(self) -> pb.Pushbullet:
        if self.__pushbullet is None:
            # pushbullet.Pushbullet sends a request on initialization,
            # so delay it
            self.__pushbullet = pb.Pushbullet(self._token)
        assert isinstance(self.__pushbullet, pb.Pushbullet)
        return self.__pushbullet

    def __init__(self, settings: LazySettings) -> None:
        self._token = settings.TRIGGER_PUSHBULLET_TOKEN
        assert self._token
        return

    def push_note(self, body: str, title: str = "") -> Any:
        return self.pushbullet.push_note(title, body)
