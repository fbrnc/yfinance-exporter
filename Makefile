run_local:
	python main.py

build:
	docker build -t yfinance-exporter:latest .

stop:
	docker stop yfinance-exporter || true && docker rm yfinance-exporter || true

run: stop
	echo "http://localhost:8000"
	docker run -p 8000:8000 --name yfinance-exporter --rm -ti yfinance-exporter:latest
