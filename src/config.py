import os

def get_config():
    return {
        'timeout': int(os.getenv('TIMEOUT', 30)),
        'ws_url': os.getenv('WS_URL', 'wss://stream.testnet.binance.vision/ws')
    }
