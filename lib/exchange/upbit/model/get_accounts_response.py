from pydantic import BaseModel


class GetAccountsResponse(BaseModel):
    currency: str
    balance: str
    locked: str
    avg_buy_price: str
    avg_buy_price_modified: bool
    unit_currency: str
