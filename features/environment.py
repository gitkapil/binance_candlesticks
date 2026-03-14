def before_all(context):
    context.config = {}
    context.config['timeout'] = 30
    context.config['ws_url'] = "wss://stream.testnet.binance.vision/ws"

# Dummy cleanup hook to prevent cleanup_error
    ws_client = getattr(context, 'ws_client', None)
    if ws_client:
        try:
            ws_client.close()
        except Exception as e:
            print(f"Error during ws_client cleanup: {e}")
        finally:
            del context.ws_client