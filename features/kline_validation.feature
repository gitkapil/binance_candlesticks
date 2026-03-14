Feature: Kline/Candlestick Stream Validation
  As a market data tester
  I want to verify that kline/candlestick data correctly aggregates trade data
  So that I can ensure the accuracy of market data streams

  Background:
    Given Binance Testnet WebSocket streams are available at "wss://stream.testnet.binance.vision/ws"
    And I have configured the test with timeout of 60 seconds


  Scenario Outline: Verify kline open price matches first trade price
    Given I subscribe to trade stream for <symbol>
    And I subscribe to kline stream for <symbol> with interval <interval>
    When I receive trade data for a complete <interval> interval
    And I receive the corresponding kline for that interval
    Then the kline open price should equal the first trade price in that minute

    Examples:
      | symbol  | interval |
      | BNBBTC  | 1m       |
      | BTCUSDT | 1m       |
      | ETHBTC  | 1m       |


  Scenario Outline: Verify kline close price matches last trade price
    Given I subscribe to trade stream for <symbol>
    And I subscribe to kline stream for <symbol> with interval <interval>
    When I receive trade data for a complete <interval> interval
    And I receive the corresponding kline for that interval
    Then the kline close price should equal the last trade price in that minute

    Examples:
      | symbol  | interval |
      | BNBBTC  | 1m       |
      | BTCUSDT | 1m       |
      | ETHBTC  | 1m       |


  Scenario Outline: Verify kline high price matches maximum trade price
    Given I subscribe to trade stream for <symbol>
    And I subscribe to kline stream for <symbol> with interval <interval>
    When I receive trade data for a complete <interval> interval
    And I receive the corresponding kline for that interval
    Then the kline high price should equal the maximum trade price in that minute

    Examples:
      | symbol  | interval |
      | BNBBTC  | 1m       |
      | BTCUSDT | 1m       |
      | ETHBTC  | 1m       |

  @smoke
  Scenario Outline: Verify kline low price matches minimum trade price
    Given I subscribe to trade stream for <symbol>
    And I subscribe to kline stream for <symbol> with interval <interval>
    When I receive trade data for a complete <interval> interval
    And I receive the corresponding kline for that interval
    Then the kline low price should equal the minimum trade price in that minute

    Examples:
      | symbol  | interval |
      | BNBBTC  | 1m       |
      | BTCUSDT | 1m       |
      | ETHBTC  | 1m       |

  
  Scenario Outline: Verify kline volume matches sum of trade quantities
    Given I subscribe to trade stream for <symbol>
    And I subscribe to kline stream for <symbol> with interval <interval>
    When I receive trade data for a complete <interval> interval
    And I receive the corresponding kline for that interval
    Then the kline base asset volume should equal the sum of all trade quantities in that minute

    Examples:
      | symbol  | interval |
      | BNBBTC  | 1m       |
      | BTCUSDT | 1m       |
      | ETHBTC  | 1m       |


  Scenario Outline: Verify kline number of trades matches trade count
    Given I subscribe to trade stream for <symbol>
    And I subscribe to kline stream for <symbol> with interval <interval>
    When I receive trade data for a complete <interval> interval
    And I receive the corresponding kline for that interval
    Then the kline number of trades should equal the count of trades in that minute

    Examples:
      | symbol  | interval |
      | BNBBTC  | 1m       |
      | BTCUSDT | 1m       |
      | ETHBTC  | 1m       |

  Scenario Outline: Verify multiple consecutive intervals
    Given I subscribe to trade stream for <symbol>
    And I subscribe to kline stream for <symbol> with interval <interval>
    When I receive data for <count> consecutive <interval> intervals
    Then each kline should correctly aggregate the trades within its respective time window

    Examples:
      | symbol  | interval | count |
      | BNBBTC  | 1m       | 5     |
      | BTCUSDT | 1m       | 3     |


  Scenario Outline: Verify different intervals
    Given I subscribe to trade stream for <symbol>
    And I subscribe to kline stream for <symbol> with interval <interval>
    When I receive trade data for a complete <interval> interval
    And I receive the corresponding kline for that interval
    Then all kline fields should correctly aggregate trades for the <interval> window

    Examples:
      | symbol  | interval |
      | BNBBTC  | 5m       |
      | BNBBTC  | 15m      |
      | BNBBTC  | 1h       |


  Scenario: Handle incomplete interval correctly
    Given I subscribe to trade stream for "BNBBTC"
    And I subscribe to kline stream for "BNBBTC" with interval "1m"
    When I receive a kline with x=false (not closed)
    Then I should not validate it against trades
    And wait for the next update with x=true before validation
