def validate_kline(kline, trades):
    agg = aggregate_trades(trades)
    return (
        float(kline['o']) == agg['open'] and
        float(kline['c']) == agg['close'] and
        float(kline['h']) == agg['high'] and
        float(kline['l']) == agg['low'] and
        float(kline['v']) == agg['volume'] and
        int(kline['n']) == agg['count']
    )
