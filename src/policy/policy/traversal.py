# -*- coding: utf-8 -*-

import os
import urllib
import json
import logging

from Products.statusmessages.interfaces import IStatusMessage
from Products.Five import BrowserView
from .i18n import MessageFactory as _

pk = os.environ.get("GOOGLE_RECAPTCHA_PUBLIC")
pr = os.environ.get("GOOGLE_RECAPTCHA_SECRET")


def get_ip(request):
    """ Extract the client IP address from the HTTP request in a proxy-compatible way.

    @return: IP address as a string or None if not available
    """
    if "HTTP_X_FORWARDED_FOR" in request.environ:
        ip = request.environ["HTTP_X_FORWARDED_FOR"]
    elif "HTTP_HOST" in request.environ:
        ip = request.environ["REMOTE_ADDR"]
    else:
        ip = None

    return ip


class PublicKeyView(BrowserView):
    def __call__(self):
        return pk


def recaptcha(event):
    if not pk or not pr:
        return

    url = event.request.getURL()
    if event.request.method == 'POST' and url.endswith('/sendto_form'):
        messages = IStatusMessage(event.request)

        cr = event.request.form.get('g-recaptcha-response')
        if cr:
            URIReCaptcha = 'https://www.google.com/recaptcha/api/siteverify'
            remote_ip = get_ip(event.request)

            params = urllib.urlencode({
                'secret': pr,
                'response': cr,
                'remote_ip': remote_ip,
            })

            data = urllib.urlopen(URIReCaptcha, params).read()
            result = json.loads(data)
            success = result.get('success', None)
            logging.getLogger("recaptcha").info(
                "Google reCaptcha: %s" % int(bool(success))
            )

            if success:
                return

            messages.add(_(u"Recaptcha failed."), type=u"info")
        else:
            messages.add(_(u"Recaptcha missing."), type=u"warning")

        event.request.form.pop("form.submitted", None)

