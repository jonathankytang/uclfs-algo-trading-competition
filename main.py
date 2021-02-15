import pandas as pd
from datetime import datetime

class SectorMomentumAlgorithm(QCAlgorithm):

    def Initialize(self):

        self.SetStartDate(2020, 4, 1)
        self.SetEndDate(2020, 12, 31)
        self.SetCash(100000)
        self.data = {}
        period = 3
        self.symbols = ["SPY", "VGT", "QQQ", "BLOK", "BLCN", "LEGR", "GFIN", "KOIN"] #ETFs
        self.SetWarmUp(period)

        for symbol in self.symbols:
            self.AddEquity(symbol, Resolution.Daily)
            self.data[symbol] = self.MOM(symbol, period, Resolution.Daily)

        self.Schedule.On(self.DateRules.MonthStart("SPY"), self.TimeRules.AfterMarketOpen("SPY"), self.Rebalance)

    def OnData(self, data):
        pass

    def Rebalance(self):
        if self.IsWarmingUp:
            return

        top3 = pd.Series(self.data).sort_values(ascending = False)[:3]

        for kvp in self.Portfolio:
            security_hold = kvp.Value

            if security_hold.Invested and (security_hold.Symbol.Value not in top3.index):
                self.Liquidate(security_hold.Symbol)

        for symbol in top3.index:
            self.SetHoldings(symbol, 1/len(top3))
