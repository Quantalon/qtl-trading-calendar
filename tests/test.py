from datetime import datetime

from qtl_trading_calendar import FuturesTradingCalendar
from qtl_trading_calendar import OptionsTradingCalendar


def test():
    calendar = FuturesTradingCalendar()
    today = datetime.today()
    r = calendar.has_day_trading(today)
    print(r)

    calendar = OptionsTradingCalendar()
    today = datetime.today()
    r = calendar.has_day_trading(today)
    print(r)


if __name__ == '__main__':
    test()
