import copy
import logging

from django.conf import settings
from django.views.debug import ExceptionReporter
from behind import jarvis


class SlackExceptionHandler(logging.Handler):
    """
    Code from djang-slack app
    An exception log handler that sends log entries to a Slack channel.
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        logging.Handler.__init__(self)

    def emit(self, record):
        try:
            request = record.request

            internal = 'internal' if request.META.get('REMOTE_ADDR') in \
                                     settings.INTERNAL_IPS else 'EXTERNAL'

            subject = '{} ({} IP): {}'.format(
                record.levelname,
                internal,
                record.getMessage(),
            )
        except Exception:
            subject = '{}: {}'.format(
                record.levelname,
                record.getMessage(),
            )
            request = None
        subject = self.format_subject(subject)

        # Since we add a nicely formatted traceback on our own, create a copy
        # of the log record without the exception data.
        no_exc_record = copy.copy(record)
        no_exc_record.exc_info = None
        no_exc_record.exc_text = None

        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)

        reporter = ExceptionReporter(request, is_email=True, *exc_info)

        try:
            tb = reporter.get_traceback_text()
        except:
            tb = "(An exception occured when getting the traceback text)"

            if reporter.exc_type:
                tb = "{} (An exception occured when rendering the " \
                     "traceback)".format(reporter.exc_type.__name__)
        message = "{}\n\n{}".format(self.format(no_exc_record), tb)
        text = f'{subject} - {message}'
        jarvis.send_slack(text, channel='#monitoring')

    def format_subject(self, subject):
        """
        Escape CR and LF characters, and limit length. RFC 2822's hard limit is
        998 characters per line. So, minus "Subject: " the actual subject must
        be no longer than 989 characters.
        """

        formatted_subject = subject.replace('\n', '\\n').replace('\r', '\\r')

        return formatted_subject[:989]
