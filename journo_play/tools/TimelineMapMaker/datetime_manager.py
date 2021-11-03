from abc import ABC
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

DAY = 'day'
WEEK = 'week'
MONTH = 'month'
YEAR = 'year'

possible_manager_arguments = {DAY: ['day', 'd'],
                              WEEK: ['week', 'w'],
                              MONTH: ['month', 'm'],
                              YEAR: ['year', 'y']
                              }


class DateTimeManager:

    @classmethod
    def set_first_processing_range(cls, start_date):
        raise NotImplementedError('set_first_processing_range not implemented for this Incrementer')

    @classmethod
    def make_date_str(cls, processing_range_start, processing_range_end):
        raise NotImplementedError('make_date_str not implemented for this incrementer')

    @classmethod
    def increment_date_range(cls, processing_range_start, processing_range_end):
        raise NotImplementedError('increment_date_range not implemented for this incrementer')

    @classmethod
    def get_processing_df(cls, processing_range_start, processing_range_end, df):
        raise NotImplementedError('get_processing_df not implemented for this incrementer')

    @classmethod
    def prepare_df(cls, df):
        raise NotImplementedError('prepare not implemented')

class WholeDayManager(DateTimeManager):
    @classmethod
    def prepare_df(cls, df):
        df['date_start'] = df['date_start'].dt.date
        return df

class DayDateTimeManager(WholeDayManager):

    @classmethod
    def set_first_processing_range(cls, start_date):
        processing_range_start = start_date
        processing_range_end = start_date

        return processing_range_start, processing_range_end

    @classmethod
    def make_date_str(cls, processing_range_start, processing_range_end):
        return processing_range_start.strftime('%m %d %Y')

    @classmethod
    def increment_date_range(cls, processing_range_start, processing_range_end):
        processing_range_start += timedelta(days=1)
        processing_range_end += timedelta(days=1)

        return processing_range_start, processing_range_end

    @classmethod
    def get_processing_df(cls, processing_range_start, processing_range_end, df):

        return df[df['date_start'] == processing_range_start.date()]


class WeekDateTimeManager(WholeDayManager):

    @classmethod
    def set_first_processing_range(cls, start_date):
        day_of_week = start_date.isoweekday()
        processing_range_start = start_date - timedelta(days=day_of_week)
        processing_range_end = start_date + timedelta(days=6 - day_of_week)
        return processing_range_start, processing_range_end

    @classmethod
    def make_date_str(cls, processing_range_start, processing_range_end):
        return '{0}  {1}'.format(processing_range_start.strftime('%m %d %Y'),
                                 processing_range_end.strftime('%m %d %Y'))

    @classmethod
    def increment_date_range(cls, processing_range_start, processing_range_end):
        processing_range_start += relativedelta(weeks=+1)
        processing_range_end += relativedelta(weeks=+1)
        return processing_range_start, processing_range_end

    @classmethod
    def get_processing_df(cls, processing_range_start, processing_range_end, df):
        return df[df['date_start'].between(processing_range_start.date, processing_range_end.date)]


class MonthDateTimeManager(WholeDayManager):

    @classmethod
    def set_first_processing_range(cls, start_date):

        processing_range_start = datetime(day=1, month=start_date.month, year=start_date.year)
        processing_range_end = (processing_range_start + relativedelta(months=+1)) - timedelta(days=1)
        return processing_range_start, processing_range_end

    @classmethod
    def make_date_str(cls, processing_range_start, processing_range_end):
        return processing_range_start.strftime('%b %Y')

    @classmethod
    def increment_date_range(cls, processing_range_start, processing_range_end):
        processing_range_start = processing_range_start + relativedelta(months=+1)
        processing_range_end = (processing_range_start + relativedelta(months=+1)) - timedelta(days=1)
        return processing_range_start, processing_range_end

    @classmethod
    def get_processing_df(cls, processing_range_start, processing_range_end, df):
        return df[df['date_start'].between(processing_range_start.date(), processing_range_end.date())]


class YearDateTimeManager(WholeDayManager):

    @classmethod
    def set_first_processing_range(cls, start_date):
        processing_range_start = datetime(day=1, month=1, year=start_date.year)
        processing_range_end = datetime(day=1, month=start_date, year=(start_date.year + 1)) - timedelta(
            days=1)
        return processing_range_start, processing_range_end

    @classmethod
    def make_date_str(cls, processing_range_start, processing_range_end):
        return processing_range_start.strftime('%Y')

    @classmethod
    def increment_date_range(cls, processing_range_start, processing_range_end):
        processing_range_start += relativedelta(years=+1)
        processing_range_end += relativedelta(years=+1)
        return processing_range_start, processing_range_end

    @classmethod
    def get_processing_df(cls, processing_range_start, processing_range_end, df):
        return df[df['date_start'].between(processing_range_start.date, processing_range_end.date)]


def get_manager(manager_argument):
    managers = {DAY: DayDateTimeManager,
                WEEK: WeekDateTimeManager,
                MONTH: MonthDateTimeManager,
                YEAR: YearDateTimeManager
                }

    manager_str = [key for key in possible_manager_arguments.keys() if manager_argument in
                   possible_manager_arguments[key]]

    manager_str = '' if len(manager_str) == 0 else manager_str[0]

    manager = managers.get(manager_str, None)

    if manager is None:
        error_str = '{0} is not a valid manager'.format(manager_argument)

        raise TypeError(error_str)

    return manager
