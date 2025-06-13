from google.protobuf.timestamp_pb2 import Timestamp
from google.type.decimal_pb2 import Decimal
from google.type.money_pb2 import Money

from finam_grpc_client.grpc.tradeapi.v1.accounts.accounts_service_pb2 import (
    Position,
)
from finam_grpc_client.grpc.tradeapi.v1.marketdata.marketdata_service_pb2 import (
    Bar,
    OrderBook,
    Quote,
    Trade,
)
from finam_grpc_client.grpc.tradeapi.v1.orders.orders_service_pb2 import (
    Leg,
    Order,
    OrderState,
)
from finam_grpc_client.grpc.tradeapi.v1.trade_pb2 import AccountTrade


class TypeChecker:
    symbol = "VTBR@MISX"

    @classmethod
    def check_order_state_type(cls, os: OrderState):
        assert isinstance(os.order_id, str)
        assert isinstance(os.exec_id, str)
        assert isinstance(os.status, int)
        cls.check_order_type(os.order)
        assert isinstance(os.transact_at, Timestamp)
        assert isinstance(os.accept_at, Timestamp)
        assert isinstance(os.withdraw_at, Timestamp)

    @classmethod
    def check_order_type(cls, o: Order):
        assert isinstance(o.account_id, str)
        assert isinstance(o.symbol, str)
        assert isinstance(o.quantity, Decimal)
        assert isinstance(o.side, int)
        assert isinstance(o.type, int)
        assert isinstance(o.time_in_force, int)
        assert isinstance(o.limit_price, Decimal)
        assert isinstance(o.stop_price, Decimal)
        assert isinstance(o.stop_condition, int)
        for l in o.legs:
            cls.check_leg_type(l)
        assert isinstance(o.client_order_id, str)

    @staticmethod
    def check_money_type(m: Money):
        assert isinstance(m.currency_code, str)
        assert isinstance(m.units, int)
        assert isinstance(m.nanos, int)

    @staticmethod
    def check_quote_type(q: Quote):
        def check_quote_option_type(o: Quote.Option):
            assert isinstance(o.open_interest, Decimal)
            assert isinstance(o.implied_volatility, Decimal)
            assert isinstance(o.theoretical_price, Decimal)
            assert isinstance(o.delta, Decimal)
            assert isinstance(o.gamma, Decimal)
            assert isinstance(o.theta, Decimal)
            assert isinstance(o.vega, Decimal)
            assert isinstance(o.rho, Decimal)

        assert isinstance(q.symbol, str)
        assert isinstance(q.ask, Decimal)
        assert isinstance(q.ask_size, Decimal)
        assert isinstance(q.bid, Decimal)
        assert isinstance(q.bid_size, Decimal)
        assert isinstance(q.last, Decimal)
        assert isinstance(q.last_size, Decimal)
        assert isinstance(q.volume, Decimal)
        assert isinstance(q.turnover, Decimal)
        assert isinstance(q.open, Decimal)
        assert isinstance(q.high, Decimal)
        assert isinstance(q.low, Decimal)
        assert isinstance(q.close, Decimal)
        assert isinstance(q.change, Decimal)
        check_quote_option_type(q.option)

    @staticmethod
    def check_bar_type(b: Bar):
        assert isinstance(b.timestamp, Timestamp)
        assert isinstance(b.open, Decimal)
        assert isinstance(b.high, Decimal)
        assert isinstance(b.low, Decimal)
        assert isinstance(b.close, Decimal)
        assert isinstance(b.volume, Decimal)

    @staticmethod
    def check_leg_type(l: Leg):
        assert isinstance(l.symbol, str)
        assert isinstance(l.quantity, Decimal)
        assert isinstance(l.side, int)

    @staticmethod
    def check_position_type(p: Position):
        assert isinstance(p.symbol, str)
        assert isinstance(p.quantity, Decimal)
        assert isinstance(p.average_price, Decimal)
        assert isinstance(p.current_price, Decimal)

    @staticmethod
    def check_order_book_row_type(r: OrderBook.Row):
        assert isinstance(r.price, Decimal)
        assert isinstance(r.sell_size, Decimal)
        assert isinstance(r.buy_size, Decimal)
        assert isinstance(r.action, OrderBook.Row.Action.ValueType)
        assert isinstance(r.mpid, str)
        assert isinstance(r.timestamp, Timestamp)

    @staticmethod
    def check_trade_type(t: Trade):
        assert isinstance(t.trade_id, str)
        assert isinstance(t.mpid, str)
        assert isinstance(t.side, int)
        assert isinstance(t.timestamp, Timestamp)
        assert isinstance(t.price, Decimal)
        assert isinstance(t.size, Decimal)

    @staticmethod
    def check_account_trade_type(t: AccountTrade):
        assert isinstance(t.trade_id, str)
        assert isinstance(t.symbol, str)
        assert isinstance(t.price, Decimal)
        assert isinstance(t.size, Decimal)
        assert isinstance(t.order_id, str)
        assert isinstance(t.side, int)
        assert isinstance(t.timestamp, Timestamp)
