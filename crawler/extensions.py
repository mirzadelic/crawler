import sentry_sdk


class SentryLogging(object):
    """
    Send exceptions and errors to Sentry.
    """

    @classmethod
    def from_crawler(cls, crawler):
        # instantiate the extension object
        ext = cls()
        sentry_dsn = crawler.settings.get("SENTRY_DSN", None)
        if sentry_dsn:
            sentry_sdk.init(sentry_dsn, traces_sample_rate=1.0)

        # return the extension object
        return ext
