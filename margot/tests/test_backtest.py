from datetime import datetime

import pytz

from margot.data import Symbol, MargotDataFrame, Ratio
from margot.data.column import cboe, alphavantage as av
from margot.data.features import finance
from margot.signals import Position, BaseAlgo
from margot.backtest import BackTest


class Index(Symbol):
    close = cboe.Column(time_series='close')
    sma = finance.SimpleMovingAverage(column='close',
                                        window=3)


class Equity(Symbol):
    close = av.Column(time_series='adjusted_close')
    log_returns = finance.LogReturns(column='close')


class VXBasisDF(MargotDataFrame):
    vix = Index('VIX', trading_calendar='NYSE')
    vix3m = Index('VIX3M', trading_calendar='NYSE')
    ratio = Ratio(numerator=vix.close,
                    denominator=vix3m.close,
                    label='vxbasis')
    ziv = Equity('ZIV', trading_calendar='NYSE')


class VXBasisTrade(BaseAlgo):
    data = VXBasisDF()

    def signal(self):
        if self.data.ratio.latest <= 1.0 and \
            self.data.vix.close.latest <= self.data.vix.sma.latest:
            return [Position(symbol='ZIV', weight=1.0)]
        else:
            return [Position(symbol='ZIV', weight=0.0)]

                    
def test_simulation():
    vxa = VXBasisDF()
    vxb = vxa.to_pandas().copy()
    when = datetime(2020, 1, 1, tzinfo=pytz.UTC)
    vxa.simulate(when)
    assert(vxb[:when].equals(vxa.to_pandas()))


def test_backtest(): 
    vx = VXBasisTrade()   
    bt = BackTest(vx)
    bt.run(periods=100)