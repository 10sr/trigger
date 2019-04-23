import pushbullet


class PushBullet:
    _token = None
    __pushbullet = None
    @property
    def pushbullet(self):
        if self.__pushbullet is None:
            # pushbullet.Pushbullet sends a request on initialization,
            # so delay it
            self.__pushbullet = pushbullet.Pushbullet(self._token)
        return self.__pushbullet

    def __init__(self, settings):
        self._token = settings.TRIGGER_PUSHBULLET_TOKEN
        assert self._token
        return

    def push_note(self, body, title=""):
        return self.pushbullet.push_note(title, body)
