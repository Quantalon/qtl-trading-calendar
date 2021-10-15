from datetime import datetime

from qtl_trading_calendar import FuturesTradingCalendar


def test():
    calendar = FuturesTradingCalendar()
    today = datetime.today()
    r = calendar.has_day_trading(today)
    print(r)


if __name__ == '__main__':
    test()
