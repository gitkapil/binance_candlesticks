import json
from behave import given, when, then
from src.websocket_client import BinanceWebSocketClient

@given('I subscribe to trade stream for {symbol}')
def step_subscribe_trade_stream(context, symbol):
    context.ws_client = BinanceWebSocketClient(symbol, context.config['ws_url'])
    context.ws_client.subscribe_trade_stream(symbol)

@given('I subscribe to kline stream for {symbol} with interval {interval}')
def step_subscribe_kline_stream(context, symbol, interval):
    context.ws_client.subscribe_kline_stream(symbol, interval)

@when('I receive trade data for a complete {interval} interval')
def step_receive_trade_data(context, interval):
    context.ws_client.collect_trades_for_interval(interval)

@when('I receive the corresponding kline for that interval')
def step_receive_kline(context):
    context.ws_client.collect_kline_for_interval()

@then('the kline open price should equal the first trade price in that minute')
def step_validate_kline_open(context):
    assert context.ws_client.kline_open_matches_first_trade()

@then('the kline close price should equal the last trade price in that minute')
def step_validate_kline_close(context):
    assert context.ws_client.kline_close_matches_last_trade()

@then('the kline high price should equal the maximum trade price in that minute')
def step_validate_kline_high(context):
    assert context.ws_client.kline_high_matches_max_trade()

@then('the kline low price should equal the minimum trade price in that minute')
def step_validate_kline_low(context):
    assert context.ws_client.kline_low_matches_min_trade()

@then('the kline base asset volume should equal the sum of all trade quantities in that minute')
def step_validate_kline_volume(context):
    assert context.ws_client.kline_volume_matches_trade_sum()

@then('the kline number of trades should equal the count of trades in that minute')
def step_validate_kline_count(context):
    assert context.ws_client.kline_count_matches_trade_count()

@when('I receive data for {count} consecutive {interval} intervals')
def step_receive_multiple_intervals(context, count, interval):
    context.ws_client.collect_multiple_intervals(int(count), interval)

@then('each kline should correctly aggregate the trades within its respective time window')
def step_validate_multiple_klines(context):
    assert context.ws_client.validate_multiple_klines()

@then('all kline fields should correctly aggregate trades for the {interval} window')
def step_validate_all_kline_fields(context, interval):
    assert context.ws_client.validate_all_kline_fields(interval)

@then('I should not validate it against trades')
def step_skip_incomplete_kline(context):
    assert context.ws_client.skip_incomplete_kline()

@then('wait for the next update with x=true before validation')
def step_wait_for_kline_closed(context):
    assert context.ws_client.wait_for_kline_closed()

@when('I receive a kline with x=false (not closed)')
def step_receive_incomplete_kline(context):
    # Implement logic or mark as pending
    pass