from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Only trading VOO
        self.ticker = "VOO"
        self.account_value = 100000  # Assuming an initial account value, this could be dynamically updated

    @property
    def interval(self):
        # Using daily data for analysis
        return "1day"

    @property
    def assets(self):
        # List of assets the strategy will trade, in this case, only VOO
        return [self.ticker]

    @property
    def data(self):
        # No additional data required beyond price data
        return []

    def run(self, data):
        holdings = data["holdings"]
        ohlcv = data["ohlcv"]

        # Assuming we have at least two days of data to compare today's price with yesterday's
        if len(ohlcv) < 2:
            log("Not enough data")
            return TargetAllocation({})

        previous_close = ohlcv[-2][self.ticker]["close"]
        today_close = ohlcv[-1][self.ticker]["close"]

        # Calculate percentage change in price
        percentage_change = ((today_close - previous_close) / previous_close) * 100

        # Strategy logic to decide buy or sell
        allocation_dict = {}

        if percentage_change < -2:
            # If price drops more than 2%, sell 25% of holdings
            log("Price dropped more than 2%, selling 25% of holdings")
            if self.ticker in holdings:
                allocation_dict[self.ticker] = max(0, holdings[self.ticker] - 0.25)
            else:
                # If we have no holdings, no action is taken
                allocation_dict[self.ticker] = 0
        elif percentage_change > 3:
            # If price increases by more than 3%, buy 10% of account value
            log("Price increased by more than 3%, buying 10% of account value")
            # Calculate number of shares to buy. This portion assumes we have access to account value and the price of VOO
            # The actual implementation may need adjustments based on how account value and price data are accessed
            shares_to_buy = (0.1 * self.account_value) / today_close
            if self.ticker in holdings:
                allocation_dict[self.ticker] = holdings[self.ticker] + shares_to_buy
            else:
                allocation_dict[self.ticker] = shares_to_buy
        else:
            # If none of the conditions are met, maintain current holdings
            log("No significant price change, maintaining current holdings")
            if self.ticker in holdings:
                allocation_dict[self.ticker] = holdings[self.ticker]
            else:
                allocation_dict[self.ticker] = 0

        return TargetAllocation(allocation_dict)