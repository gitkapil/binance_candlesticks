import asyncio
import websockets
import json
import ssl

class BinanceWebSocketClient:
    def kline_open_matches_first_trade(self):
        if not self.trades or not self.klines:
            return False
        first_trade_price = float(self.trades[0]['price'])
        kline_open_price = float(self.klines[-1]['o'])
        return abs(first_trade_price - kline_open_price) < 1e-8

    def kline_close_matches_last_trade(self):
        if not self.trades or not self.klines:
            return False
        last_trade_price = float(self.trades[-1]['price'])
        kline_close_price = float(self.klines[-1]['c'])
        return abs(last_trade_price - kline_close_price) < 1e-8

    def kline_high_matches_max_trade(self):
        if not self.trades or not self.klines:
            return False
        max_trade_price = max(float(t['price']) for t in self.trades)
        kline_high_price = float(self.klines[-1]['h'])
        return abs(max_trade_price - kline_high_price) < 1e-8

    def kline_low_matches_min_trade(self):
        if not self.trades or not self.klines:
            return False
        min_trade_price = min(float(t['price']) for t in self.trades)
        kline_low_price = float(self.klines[-1]['l'])
        return abs(min_trade_price - kline_low_price) < 1e-8

    def kline_volume_matches_trade_sum(self):
        if not self.trades or not self.klines:
            return False
        total_volume = sum(float(t['qty']) for t in self.trades)
        kline_volume = float(self.klines[-1]['v'])
        return abs(total_volume - kline_volume) < 1e-8

    def kline_count_matches_trade_count(self):
        if not self.trades or not self.klines:
            return False
        trade_count = len(self.trades)
        kline_count = int(self.klines[-1]['n'])
        return trade_count == kline_count

    async def _collect_multiple_intervals(self, count, interval):
        self.klines = []
        uri = f"{self.ws_url}?streams={self.kline_stream}"
        async with websockets.connect(uri, ssl=self.ssl_context) as ws:
            collected = 0
            while collected < count:
                msg = await ws.recv()
                data = json.loads(msg)
                kline = data.get('data', {}).get('k', {})
                if kline.get('x'):
                    self.klines.append(kline)
                    collected += 1

    def validate_multiple_klines(self):
        return all(self.validate_all_kline_fields(None) for _ in self.klines)

    def validate_all_kline_fields(self, interval):
        return (self.kline_open_matches_first_trade() and
                self.kline_close_matches_last_trade() and
                self.kline_high_matches_max_trade() and
                self.kline_low_matches_min_trade() and
                self.kline_volume_matches_trade_sum() and
                self.kline_count_matches_trade_count())

    def wait_for_kline_closed(self):
        return self.klines and self.klines[-1].get('x', False)

    def skip_incomplete_kline(self):
        # Returns True if the last kline is not closed (x=False), otherwise False
        return not (self.klines and self.klines[-1].get('x', False))

    def _interval_seconds(self, interval):
        mapping = {'1m': 60, '5m': 300, '15m': 900, '1h': 3600}
        return mapping.get(interval, 60)
    def __init__(self, symbol, ws_url):
        self.symbol = symbol.lower()
        self.ws_url = ws_url
        self.trade_stream = f"{self.symbol}@trade"
        self.kline_stream = None
        self.trades = []
        self.klines = []
        self.ws = None
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    def subscribe_trade_stream(self, symbol):
        self.trade_stream = f"{symbol.lower()}@trade"

    def subscribe_kline_stream(self, symbol, interval):
        self.kline_stream = f"{symbol.lower()}@kline_{interval}"

    async def collect_trades_for_interval(self, interval):
        self.trades = []
        uri = f"{self.ws_url}?streams={self.trade_stream}"
        async with websockets.connect(uri, ssl=self.ssl_context) as ws:
            start_time = None
            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                trade = data.get('data', {})
                if not start_time:
                    start_time = trade['T'] // 1000  # trade time in seconds
                current_time = trade['T'] // 1000
                if current_time - start_time >= self._interval_seconds(interval):
                    break
                self.trades.append(trade)

    async def collect_kline_for_interval(self):
        self.klines = []
        uri = f"{self.ws_url}?streams={self.kline_stream}"
        async with websockets.connect(uri, ssl=self.ssl_context) as ws:
            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                kline = data.get('data', {}).get('k', {})
                if kline.get('x'):  # kline closed
                    self.klines.append(kline)
                    break

    def kline_open_matches_first_trade(self):
        if not self.trades or not self.klines:
            return False
        first_trade_price = float(self.trades[0]['price'])
        kline_open_price = float(self.klines[-1]['o'])
        return abs(first_trade_price - kline_open_price) < 1e-8

    def kline_close_matches_last_trade(self):
        if not self.trades or not self.klines:
            return False
        last_trade_price = float(self.trades[-1]['price'])
        kline_close_price = float(self.klines[-1]['c'])
        return abs(last_trade_price - kline_close_price) < 1e-8

    def kline_high_matches_max_trade(self):
        if not self.trades or not self.klines:
            return False
        max_trade_price = max(float(t['price']) for t in self.trades)
        kline_high_price = float(self.klines[-1]['h'])
        return abs(max_trade_price - kline_high_price) < 1e-8

    def kline_low_matches_min_trade(self):
        if not self.trades or not self.klines:
            return False
        min_trade_price = min(float(t['price']) for t in self.trades)
        kline_low_price = float(self.klines[-1]['l'])
        return abs(min_trade_price - kline_low_price) < 1e-8

    def kline_volume_matches_trade_sum(self):
        if not self.trades or not self.klines:
            return False
        total_volume = sum(float(t['qty']) for t in self.trades)
        kline_volume = float(self.klines[-1]['v'])
        return abs(total_volume - kline_volume) < 1e-8

    def kline_count_matches_trade_count(self):
        if not self.trades or not self.klines:
            return False
        trade_count = len(self.trades)
        kline_count = int(self.klines[-1]['n'])
        return trade_count == kline_count

    async def _collect_multiple_intervals(self, count, interval):
        self.klines = []
        uri = f"{self.ws_url}?streams={self.kline_stream}"
        async with websockets.connect(uri, ssl=self.ssl_context) as ws:
            collected = 0
            while collected < count:
                msg = await ws.recv()
                data = json.loads(msg)
                kline = data.get('data', {}).get('k', {})
                if kline.get('x'):
                    self.klines.append(kline)
                    collected += 1

    def validate_multiple_klines(self):
        return all(self.validate_all_kline_fields(None) for _ in self.klines)

    def validate_all_kline_fields(self, interval):
        return (self.kline_open_matches_first_trade() and
                self.kline_close_matches_last_trade() and
                self.kline_high_matches_max_trade() and
                self.kline_low_matches_min_trade() and
                self.kline_volume_matches_trade_sum() and
                self.kline_count_matches_trade_count())

    def wait_for_kline_closed(self):
        return self.klines and self.klines[-1].get('x', False)

    def skip_incomplete_kline(self):
        # Returns True if the last kline is not closed (x=False), otherwise False
        return not (self.klines and self.klines[-1].get('x', False))

    def _interval_seconds(self, interval):
        mapping = {'1m': 60, '5m': 300, '15m': 900, '1h': 3600}
        return mapping.get(interval, 60)
