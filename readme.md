# Adaptive Quant

AI Trading Assistant

## Installation

```bash
pip install -r requirements.txt
```

Run

```bash
python app/main.py
```

Telegram

```
/send AAPL
/send NVDA
/send TSLA
```

Backtest

```python
from backtest.runner import Runner

Runner().run("AAPL")
```
