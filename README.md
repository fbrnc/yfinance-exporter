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
# TYPE yfinance_price gauge
yfinance_price{currency="EUR",name="Amazon.com Inc",symbol="AMZ.DE",type="Open"} 2999.5
yfinance_price{currency="EUR",name="Amazon.com Inc",symbol="AMZ.DE",type="High"} 3023.0
yfinance_price{currency="EUR",name="Amazon.com Inc",symbol="AMZ.DE",type="Low"} 2966.5
yfinance_price{currency="EUR",name="Amazon.com Inc",symbol="AMZ.DE",type="Close"} 3009.0
yfinance_price{currency="EUR",name="Amazon.com Inc",symbol="AMZ.DE",type="Volume"} 5249.0
yfinance_price{currency="EUR",name="Amazon.com Inc",symbol="AMZ.DE",type="Dividends"} 0.0
yfinance_price{currency="EUR",name="Amazon.com Inc",symbol="AMZ.DE",type="Stock Splits"} 0.0
yfinance_price{currency="EUR",name="Tesla Inc",symbol="TL0.DE",type="Open"} 896.0
yfinance_price{currency="EUR",name="Tesla Inc",symbol="TL0.DE",type="High"} 945.5
yfinance_price{currency="EUR",name="Tesla Inc",symbol="TL0.DE",type="Low"} 888.7999877929688
yfinance_price{currency="EUR",name="Tesla Inc",symbol="TL0.DE",type="Close"} 928.5
yfinance_price{currency="EUR",name="Tesla Inc",symbol="TL0.DE",type="Volume"} 79857.0
yfinance_price{currency="EUR",name="Tesla Inc",symbol="TL0.DE",type="Dividends"} 0.0
yfinance_price{currency="EUR",name="Tesla Inc",symbol="TL0.DE",type="Stock Splits"} 0.0
# HELP yfinance_last_update Last API update
# TYPE yfinance_last_update gauge
yfinance_last_update 1.648106591e+09


```

## Docker compose example (with inline configuration)   

Hint: You need to login via `docker login ghcr.io -u USERNAME` first to pull the image. (see [Github documentation](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-to-the-container-registry))

```
version: "3.7"
services:
  yfinance-exporter:
    image: ghcr.io/fbrnc/yfinance-exporter:v0.0.4
    container_name: yfinance-exporter
    restart: unless-stopped
    environment:
      # YFINANCE_EXPORTER_PORT: 8000
      # YFINANCE_EXPORTER_METRIC_NAME: yfinance_price
      # YFINANCE_EXPORTER_CRON_EXPRESSION: '*/10 * * * *'
      YFINANCE_EXPORTER_CONFIG: |
        {
          "AMZ.DE": { "name": "Amazon.com Inc", "currency": "EUR" },
          "TL0.DE": { "name": "Tesla Inc", "currency": "EUR" }
        }
    ports:
      - "8000:8000"
```
