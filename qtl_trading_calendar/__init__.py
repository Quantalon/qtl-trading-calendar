from datetime import datetime, timedelta
from pathlib import Path
import warnings
import urllib.request

import toml


def load_toml_by_url(url):
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    data = toml.loads(content)
    return data


def is_weekend(dt: datetime):
    weekday = dt.weekday()
    #  Saturday, Sunday
    if weekday in (5, 6):
        return True
    return False


class BaseTradingCalendar:
    meta_url = 'https://quantalon.gd2.qingstor.com/trading-calendar/meta.toml'
    type = None

    def __init__(self):
        self.data_file_path = None
        self.current_dir = Path(__file__).parent
        self.meta = load_toml_by_url(self.meta_url)

        if self.type is not None:
            self.download_data_file()
            self.load_data()

    def download_data_file(self):
        filename = self.meta[self.type]['filename']
        self.data_file_path = self.current_dir / filename
        if self.data_file_path.exists():
            return
        url = self.meta[self.type]['url']
        response = urllib.request.urlopen(url)
        data = response.read()
        self.data_file_path.write_bytes(data)


class FuturesTradingCalendar(BaseTradingCalendar):
    type = 'futures'

    def load_data(self):
        # tips
        #   这里的日期为自然日，非交易结算日
        #   周末没有日盘与夜盘，程序逻辑排除

        self.config = toml.load(self.data_file_path)

        now = datetime.now()
        if now.date() > self.config['expire_date']:
            warnings.warn('the trading calendar config is expired...')

        # Special cases
        self.no_day_trading_dates = set(self.config['holiday_dates'])
        self.no_night_trading_dates = set(self.config['holiday_dates']) | set(self.config['no_night_trading_dates'])

    def has_day_trading(self, dt: datetime):
        if is_weekend(dt):
            return False
        if dt.date() in self.no_day_trading_dates:
            return False
        return True

    def has_night_trading(self, dt: datetime):
        dt = dt - timedelta(hours=4)  # 夜盘跨自然日的情况
        if is_weekend(dt):
            return False
        if dt.date() in self.no_night_trading_dates:
            return False
        return True


class OptionsTradingCalendar(BaseTradingCalendar):
    type = 'options'

    def load_data(self):
        self.config = toml.load(self.data_file_path)

        now = datetime.now()
        if now.date() > self.config['expire_date']:
            warnings.warn('the trading calendar config is expired...')

        # Special cases
        self.no_day_trading_dates = set(self.config['holiday_dates'])

    def has_day_trading(self, dt: datetime):
        if is_weekend(dt):
            return False
        if dt.date() in self.no_day_trading_dates:
            return False
        return True
