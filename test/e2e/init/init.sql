USE `bitrush`;

CREATE TABLE IF NOT EXISTS `account` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `vendor` varchar(100) NOT NULL COMMENT 'api 제공업체',
  `enabled` tinyint(1) NOT NULL DEFAULT '1',
  `access_key` varchar(120) NOT NULL COMMENT 'access key (algo=AES256_GCM)',
  `secret_key` varchar(120) NOT NULL COMMENT 'secret key (algo=AES256_GCM)',
  `expired_at` datetime NOT NULL COMMENT 'api key 만료일자',
  `alias` varchar(100) NOT NULL COMMENT 'api key 별칭',
  `data_key` blob NOT NULL COMMENT 'encryption key',
  PRIMARY KEY (`id`),
  UNIQUE KEY `credential_alias_unique` (`alias`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COMMENT='계정';

CREATE TABLE IF NOT EXISTS `candle` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ticker` varchar(100) NOT NULL,
  `closed_at` datetime NOT NULL,
  `open` decimal(19,8) NOT NULL COMMENT '시가',
  `high` decimal(19,8) NOT NULL COMMENT '고가',
  `low` decimal(19,8) NOT NULL COMMENT '저가',
  `close` decimal(19,8) NOT NULL COMMENT '종가',
  `volume` decimal(21,8) NOT NULL COMMENT '거래량',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ohlc_daily_ticker_date_idx` (`ticker`,`closed_at` DESC)
) ENGINE=InnoDB AUTO_INCREMENT=4158 DEFAULT CHARSET=utf8 COMMENT='가격변화';

CREATE TABLE IF NOT EXISTS `order` (
  `id` varchar(36) NOT NULL COMMENT 'uuid',
  `created_at` datetime NOT NULL COMMENT '주문일시',
  `exchange` varchar(100) DEFAULT NULL COMMENT '거래소',
  `type` enum('BUY','SELL') NOT NULL COMMENT '거래타입',
  `ticker` varchar(100) NOT NULL,
  `strategy` varchar(100) NOT NULL COMMENT '전략',
  `avg_price` decimal(19,8) NOT NULL COMMENT '거래평균단가',
  `volume` decimal(19,8) NOT NULL COMMENT '거래수량',
  `amount` decimal(19,8) NOT NULL COMMENT '거래금액',
  `raw_data` json NOT NULL COMMENT 'api로부터 전달받은 trade 데이터',
  `account_id` bigint NOT NULL COMMENT '계정',
  `status` varchar(20) NOT NULL COMMENT '거래 상태 (wait = ''미체결'', filled = ''체결'')',
  PRIMARY KEY (`id`),
  KEY `idx_account_id_ticker_strategy` (`account_id`,`ticker`,`strategy`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='주문';

INSERT INTO account (vendor, access_key, secret_key, expired_at, alias, data_key) values ('upbit', 'oWjhnsLBf2ywMfeeqg+pfY4ccyBjIGQhnYa4ti4bdK1Fv+LGgPywX9DAF8ljB7XMvHHS3KLO0Q6zGkNa3h76k+LmI0d62RxqameFVGZC2PI1YESCtX7Klg==', 'IyrZ8bnh6KruY/npeJxbgkhYgLz+jzzwXE+QtwkyEtU8fO0G1wyTXYHs1iiN/V7Q1RM/v0ztbYjd4ukTlIcvtaogydhQTgiBEbhoUG2c0BJXuX1Ibadizw==', '2022-12-12 00:15:00', 'gompro-local', 0x0102030078FCAA630269436416634D0331A61A9037C9C3360A504B31D73834A4F53D3CC9E001933801E4D740A8C02BC33C7BAED8DACC0000007E307C06092A864886F70D010706A06F306D020100306806092A864886F70D010701301E060960864801650304012E3011040CA00960F9C89647B9ECE91576020110803BEC77171A315EF268947F7CA244B1385E134F144E3B948AD65CE98E06E27F84FF691B474ECE811E53DB19D60BF510706E0E7BD79C4F2DFA8F179339);

