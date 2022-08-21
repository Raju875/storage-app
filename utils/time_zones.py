from datetime import datetime
from django.conf import settings
from pytz import timezone


class TimeZoneUtil():

    @staticmethod
    def utc_to_timezone(datetime=None):
        settings_time_zone = timezone(settings.TIME_ZONE)
        return datetime.astimezone(settings_time_zone)

    @staticmethod
    def get_datetime():
        now = datetime.now()
        settings_time_zone = timezone(settings.TIME_ZONE)

        return now.astimezone(settings_time_zone)

    @staticmethod
    def seconds_to_hours(seconds=None):
        hours = seconds // 3600
        minutes = seconds // 60 - hours * 60

        result = "%d:%02d" % (hours, minutes)

        return result
