#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from django.utils.timezone import now
from rapidsms.messages.base import MessageBase
from rapidsms.messages.error import ErrorMessage


class IncomingMessage(MessageBase):
    """Inbound message that provides an API to handle responses."""

    def __init__(self, *args, **kwargs):
        self.received_at = kwargs.pop('received_at', now())
        super(IncomingMessage, self).__init__(*args, **kwargs)
        # list of messages created by IncomingMessage.respond()
        self.responses = []

    @property
    def date(self):
        return self.received_at

    def respond(self, text, **kwargs):
        """
        Respond to this message. Router will process responses automatically.
        """
        if 'template' in kwargs:
            raise TypeError("`template` is no longer valid usage for "
                            "respond().  Pass the message text as `text`.")

        context = {'text': text, 'connections': self.connections,
                   'in_response_to': self}
        context.update(kwargs)
        self.responses.append(context)
        return context

    def error(self, text, **kwargs):
        return self.respond(class_=ErrorMessage, text=text, **kwargs)
