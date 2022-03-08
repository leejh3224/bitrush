import uuid
from decimal import Decimal
from typing import Optional, List

from lib.account.account import Account
from lib.asset.asset import Asset
from lib.candle.candle import Candle
from lib.exchange.alpaca.adapter.bar_adapter import BarAdapter
from lib.exchange.alpaca.adapter.account_adapter import AccountAdapter
from lib.exchange.alpaca.adapter.order_adapter import OrderAdapter
from lib.exchange.alpaca.adapter.position_adapter import PositionAdapter
from lib.exchange.exchange import Exchange
from lib.order.order import Order
from lib.exchange.alpaca.model.order import Order as AlpacaOrder
from alpaca_trade_api import REST
from alpaca_trade_api.common import URL


# us equity
class AlpacaExchange(Exchange):
	client: REST

	access_key: str
	secret_key: str

	@staticmethod
	def build(account: Account, is_paper=False):
		base_url_live = "https://api.alpaca.markets"
		base_url_paper = "https://paper-api.alpaca.markets"

		return AlpacaExchange(
			account=account,
			base_url=base_url_paper if is_paper else base_url_live
		)

	def __init__(self, account: Account, base_url: str):
		super().__init__()
		self.client = REST(
			key_id=account.get_access_key(),
			secret_key=account.get_secret_key(),
			base_url=URL(base_url)
		)

	def get_day_candles(self, ticker: str, start: str, end: str) -> List[Candle]:
		pass

	def get_last_candle(self, ticker: str) -> Candle:
		snapshot = self.client.get_snapshot(symbol=ticker)
		return BarAdapter(ticker=ticker, bar=snapshot.minute_bar)

	def get_all_assets(self) -> List[Asset]:
		account = self.client.get_account()
		positions = self.client.list_positions()

		cash = AccountAdapter(account.__dict__.get('_raw'))
		stocks = [PositionAdapter(position.__dict__.get('_raw')) for position in positions]
		return [cash, *stocks]

	def buy(self, ticker: str, amount: Decimal) -> Optional[Order]:
		return self.__order(side="buy", ticker=ticker, amount=amount)

	def sell(self, ticker: str, volume: Decimal) -> Optional[Order]:
		return self.__order(side="sell", ticker=ticker, volume=volume)

	def get_order(self, order_id: str) -> Optional[Order]:
		order = self.client.get_order_by_client_order_id(client_order_id=order_id)
		return OrderAdapter(AlpacaOrder(**order.__dict__.get("_raw")))

	def __order(self, side: str, ticker: str, amount: Decimal = None, volume: Decimal = None) -> Optional[Order]:
		if amount is None and volume is None:
			raise ValueError("order amount or volume should not be None")

		if not self.__is_open_now():
			return None

		custom_order_id = str(uuid.uuid4())
		qty = float(volume) if volume is not None else None
		notional = float(amount) if amount is not None else None

		order = self.client.submit_order(
			symbol=ticker,
			qty=qty,
			notional=notional,
			side=side,
			type="market",
			client_order_id=custom_order_id
		)
		return OrderAdapter(AlpacaOrder(**order.__dict__.get("_raw")))

	def __is_open_now(self):
		"""check if US exchanges (NYSE, NASDAQ, etc) are open
		09:30 (EST) ~ 16:00 (EST)
		"""
		clock = self.client.get_clock()
		return clock.is_open
