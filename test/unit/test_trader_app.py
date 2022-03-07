from unittest.mock import patch

from freezegun import freeze_time

from lib.account.account import Account
from datetime import datetime

from trader_app import send_credential_expiry_reminder


@freeze_time("2000-12-01 00:00:00")
def test_send_credential_expiry_reminder_30_day_reminder(mock_upbit_account):
    with patch('lib.telegram_bot.send_message') as mock_send_message:
        mock_upbit_account.get_expired_at.return_value = datetime.strptime("2000-12-31 00:00:00", "%Y-%m-%d %H:%M:%S")
        send_credential_expiry_reminder(mock_upbit_account)

        mock_send_message.assert_called_once()
