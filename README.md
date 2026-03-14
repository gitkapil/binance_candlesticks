
# Binance candlesticks BDD Test Framework

## What Does This Test?
This framework checks if Binance's market summary data candlesticks match the real trading data. It ensures:
- Opening price matches the first trade
- Closing price matches the last trade
- Highest/lowest prices match the highest/lowest trades
- Total volume matches the sum of all trades
- Number of trades matches the summary
- Summaries for different time intervals are correct
- Only checks summaries when the interval is complete

This helps anyone trust Binance's market data for accuracy.

## Step-by-Step Guide

### 1. Install Required Software
- **Python 3.11**: 
  ```sh
  brew install python@3.11
  ```

### 2. Open Terminal and Go to Project Folder
```sh
cd path/to/binance_kline_test
```

### 3. Create a Virtual Environment
```sh
/usr/local/bin/python3.11 -m venv venv
source venv/bin/activate
```

### 4. Install Project Dependencies
```sh
python -m pip install -r requirements.txt
```

### 5. Run the Test Framework
```sh
bash run_tests.sh
```

### 6. View the Results
Open the file `reports/report.html` in your web browser to see the test results.

## Project Structure
- `features/`: Feature files and step definitions
- `src/`: Source code (WebSocket client, aggregator, validator, config)
- `data/`: Test data
- `reports/`: Test reports
- `run_tests.sh`: Script to automate test and report generation

## Dependencies
- behave
- websockets
- pytest
- pytest-html

## Notes
- Step definitions and source code are modular for easy extension.
- HTML report is generated in `reports/report.html`.
- WebSocket client disables SSL verification for testnet.

