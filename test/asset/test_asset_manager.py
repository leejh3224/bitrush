from lib.asset.asset_manager import AssetManager


def test_get_cash(asset_manager: AssetManager):
    cash = asset_manager.get_cash()
    print(cash)


def test_get_account_size(asset_manager: AssetManager):
    account_size = asset_manager.get_account_size()
    print(account_size)


def test_get_asset(asset_manager: AssetManager):
    asset = asset_manager.get_asset(ticker="BTC")
    print(asset)
