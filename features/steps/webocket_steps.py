from behave import given, when, then

@given('Binance Testnet WebSocket streams are available at "{ws_url}"')
def step_ws_url(context, ws_url):
    context.config['ws_url'] = ws_url

@given('I have configured the test with timeout of {timeout} seconds')
def step_timeout(context, timeout):
    context.config['timeout'] = int(timeout)
