# yfinance-exporter

`yfinance-exporter` is a python tool, that uses the [yfinance library](https://github.com/ranaroussi/yfinance)
to query current stock prices from [Yahoo Finance](https://finance.yahoo.com/)

Make sure to read [the yfinance library's important legal disclaimer](https://github.com/ranaroussi/yfinance#-important-legal-disclaimer-)

## Configuration

yfinance-exporter expects a JSON object with the symbols you want to scrape in the following format:

```json
{
  "AMZ.DE": { "name": "Amazon.com Inc", "currency": "EUR" },
  "TL0.DE": { "name": "Tesla Inc", "currency": "EUR" }
}
```

If you omit the `name` or the `currency` attributes, these values will be populated from Yahoo's metadata.

HINT: make sure you pick the correct symbol that matches the currency you're expecting. 
Go to [Yahoo Finance](https://finance.yahoo.com/) and find the matching symbol first.
Also your might want to check other websites (e.g. https://www.boerse-frankfurt.de/) to find
a matching symbol for a given WKN or ISIN.

## Settings

* `YFINANCE_EXPORTER_PORT`: Defaults to `8000`. This is the port that yfinance-exporter exposes the metrics to.
* `YFINANCE_EXPORTER_CRON_EXPRESSION`: Defaults to `*/10 * * * *`. Make sure to not hit any rate limits.
* `YFINANCE_EXPORTER_METRIC_NAME`: Defaults to `yfinance_price`
* `YFINANCE_EXPORTER_CONFIG`: Defaults to `file://config.dist.json`. You can either directly pass a JSON string or - prepended with `file://` a path to a json file you've mounted inside the container

## Example

```
# HELP yfinance_price Current price
# TYPE yfinance_price gauge
yfinance_price{currency="EUR",name="Amazon.com Inc",symbol="AMZ.DE"} 2878.5
yfinance_price{currency="EUR",name="Tesla Inc",symbol="TL0.DE"} 812.0
# HELP yfinance_last_update Last API update
# TYPE yfinance_last_update gauge
yfinance_last_update 1.647635043e+09
```
