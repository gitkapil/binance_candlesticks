def aggregate_trades(trades):
    prices = [float(t['p']) for t in trades]
    quantities = [float(t['q']) for t in trades]
    return {
        'open': prices[0] if prices else 0,
        'close': prices[-1] if prices else 0,
        'high': max(prices) if prices else 0,
        'low': min(prices) if prices else 0,
        'volume': sum(quantities),
        'count': len(trades)
    }
