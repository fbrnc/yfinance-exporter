import yfinance 
import logging
import aiocron
import asyncio
import json
import time
import os
from prometheus_client import CollectorRegistry, Gauge, generate_latest, start_http_server

logging.basicConfig(
    # filename='yfinance.log', # defaults to stdout
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

port = os.getenv('YFINANCE_EXPORTER_PORT', 8000)
cron_expression = os.getenv('YFINANCE_EXPORTER_CRON_EXPRESSION', '*/10 * * * *')
metric_name = os.getenv('YFINANCE_EXPORTER_METRIC_NAME', 'yfinance_price')
config = os.getenv('YFINANCE_EXPORTER_CONFIG', "file://config.dist.json")

logging.info("Loading config...")
if config.startswith('file://'):
    with open(config.replace('file://', ''), 'r') as file:
        config = file.read()
config = json.loads(config)

registry = CollectorRegistry()
metric = Gauge(metric_name, 'Current price', ['symbol', 'name', 'currency'], registry=registry)
last_update = Gauge('yfinance_last_update', 'Last API update', registry=registry)


def get_current_price(symbol):
    ticker = yfinance.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]


@aiocron.crontab(cron_expression)
async def cron_update_metric():
    update_metric()


def update_metric():
    global config
    logging.info("Updating...")
    for symbol, labels in config.items():
        try:
            value = get_current_price(symbol)
            metric.labels(symbol=symbol, name=labels['name'], currency=labels['currency']).set(value)
            logging.info(f"Getting value for {labels['name']} ({symbol}) [{labels['currency']}]: {round(value, 2)}")
        except:
            logging.error(f"An exception occurred while getting value for {labels['name']} ({symbol}) [{labels['currency']}]")

    last_update.set(int(time.time()))

    logging.info(generate_latest(registry).decode('utf-8'))


if __name__ == '__main__':
    logging.info("Fetching information...")
    for symbol, labels in config.items():
        ticker = yfinance.Ticker(symbol)
        if 'currency' not in labels:
            config[symbol]['currency'] = ticker.info['currency']
        if 'name' not in labels:
            config[symbol]['name'] = ticker.info['shortName']
            # config[symbol]['financialCurrency'] = ticker.info['financialCurrency']

    logging.info(config)

    logging.info("Initial update...")
    update_metric()

    logging.info(f"Starting http server on port {port}...")
    start_http_server(port, registry=registry)

    logging.info("Starting event loop...")
    asyncio.get_event_loop().run_forever()
