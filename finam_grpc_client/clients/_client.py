import logging
from datetime import date, datetime
from typing import Any, Iterable, Literal

from google.protobuf.timestamp_pb2 import Timestamp

from finam_grpc_client.models.grpc.securities_pb2 import (
    GetSecuritiesRequest,
    GetSecuritiesResult,
)
from finam_grpc_client.models.proto.candles_pb2 import (
    DayCandleTimeFrame,
    GetDayCandlesRequest,
    GetDayCandlesResult,
    GetIntradayCandlesRequest,
    GetIntradayCandlesResult,
    IntradayCandleTimeFrame,
)
from finam_grpc_client.models.proto.common_pb2 import BuySell, OrderValidBefore
from finam_grpc_client.models.proto.events_pb2 import (
    OrderBookSubscribeRequest,
    OrderBookUnsubscribeRequest,
    OrderTradeSubscribeRequest,
    OrderTradeUnsubscribeRequest,
    SubscriptionRequest,
)
from finam_grpc_client.models.proto.orders_pb2 import (
    CancelOrderRequest,
    CancelOrderResult,
    GetOrdersRequest,
    GetOrdersResult,
    NewOrderRequest,
    NewOrderResult,
    OrderCondition,
    OrderProperty,
)
from finam_grpc_client.models.proto.portfolios_pb2 import (
    GetPortfolioRequest,
    GetPortfolioResult,
    PortfolioContent,
)
from finam_grpc_client.models.proto.stops_pb2 import (
    CancelStopRequest,
    CancelStopResult,
    GetStopsRequest,
    GetStopsResult,
    NewStopRequest,
    NewStopResult,
    StopLoss,
    TakeProfit,
)

from .base import BaseGrpcClient
from .subscribes import SubscribesMixin


class FinamGrpcClient(SubscribesMixin, BaseGrpcClient):
    """
    Класс для подключения к Api.

    Перед началом работы необходимо вызвать метод open().
    После окончания использования нужно закрыть канал.
    Сделать это можно вызвав метод close().

    Либо можно воспользоваться асинхронным менеджером контекста.

    :param token: Токен доступа к Api.
    :param keep_alive_request_id: ID для запроса на поддержание активности.
    """

    logger = logging.getLogger("finam_grpc_client.ApiClient")

    class _TimeFrames:
        D1, W1 = DayCandleTimeFrame.values()[1:]
        M1, M5, M15, H1 = IntradayCandleTimeFrame.values()[1:]

    def __init__(
        self, token: str, *, keep_alive_request_id: str = "keep_alive"
    ):
        url = "trade-api.finam.ru"
        metadata = (("x-api-key", token),)
        super().__init__(
            keep_alive_request_id,
            url,
            metadata,
        )

    async def get_candles(
        self,
        security_board: str,
        security_code: str,
        time_frame: Literal["M1", "M5", "M15", "H1", "D1", "W1"],
        to: date | datetime,
        count: int = 1,
    ) -> GetDayCandlesResult | GetIntradayCandlesResult | None:
        """
        Получение свечей.

        :param security_board: Код площадки;
        :param security_code: код инструмента;
        :param time_frame: тайм-фрейм;
        :param to: конец интервала, datetime для внутридневных,
          для остальных date;
        :param count: количество свечей.

        :return: Свечи.
        """
        self.logger.info(
            "Метод запущен с параметрами: security_board=%s, "
            "security_code=%s, time_frame=%s, to=%s, count=%s.",
            security_board,
            security_code,
            time_frame,
            to,
            count,
        )
        model_type: type[GetDayCandlesRequest | GetIntradayCandlesRequest]
        interval: dict[str, Any] = dict(count=count)
        params = dict(
            security_board=security_board,
            security_code=security_code,
            time_frame=getattr(self._TimeFrames, time_frame),
            interval=interval,
        )
        if time_frame in ("D1", "W1"):
            model_type = GetDayCandlesRequest
            method = self._candles.GetDayCandles
            interval["to"] = dict(year=to.year, month=to.month, day=to.day)
        else:
            model_type = GetIntradayCandlesRequest
            method = self._candles.GetIntradayCandles
            interval["to"] = to
        model = model_type(**params)
        result = await self._execute_request(method, model)
        if result:
            self.logger.info("Получены свечи: %s.", result)
        return result

    async def get_portfolio(
        self,
        client_id: str,
        include_currencies: bool = True,
        include_money: bool = True,
        include_positions: bool = True,
        include_max_buy_sell: bool = True,
    ) -> GetPortfolioResult | None:
        """
        Получение портфеля.

        :param client_id: Торговый код клиента;
        :param include_currencies: запросить информацию по
          валютам портфеля;
        :param include_money: запросить информацию по денежным
          позициям портфеля;
        :param include_positions: запросить информацию по позициям портфеля;
        :param include_max_buy_sell: запросить информацию о максимальном
          доступном объеме на покупку/продажу.

        :return: Модель портфеля.
        """
        self.logger.info(
            "Запрос информации о портфеле: client_id=%s, "
            "include_currencies=%s, include_money=%s, "
            "include_positions=%s, include_max_buy_sell=%s.",
            client_id,
            include_currencies,
            include_money,
            include_positions,
            include_max_buy_sell,
        )
        model = GetPortfolioRequest(
            client_id=client_id,
            content=PortfolioContent(
                include_currencies=include_currencies,
                include_money=include_money,
                include_positions=include_positions,
                include_max_buy_sell=include_max_buy_sell,
            ),
        )
        result = await self._execute_request(
            self._portfolio.GetPortfolio, model
        )
        if result:
            self.logger.info("Получена информация о портфеле: %s.", result)
        return result

    async def get_securities(
        self, board: str | None = None, seccode: str | None = None
    ) -> GetSecuritiesResult | None:
        """
        Получение списка инструментов.

        :param board: Режим торгов;
        :param seccode: тикер инструмента.

        :return: Модель инструментов.
        """
        self.logger.info(
            "Запрос информации об инструментах: board=%s, seccode=%s.",
            board,
            seccode,
        )
        model = GetSecuritiesRequest(
            board={"value": board} if board else None,
            seccode={"value": seccode} if seccode else None,
        )
        result = await self._execute_request(
            self._securities.GetSecurities, model
        )
        if result:
            self.logger.info("Получена информация об инструментах: %s", result)
        return result

    async def get_orders(
        self,
        client_id: str,
        include_active: bool = True,
        include_canceled: bool = True,
        include_matched: bool = True,
    ) -> GetOrdersResult | None:
        """
        Получение списка ордеров.

        :param client_id: Торговый код клиента;
        :param include_matched: вернуть исполненные заявки;
        :param include_canceled: вернуть отмененные заявки;
        :param include_active: вернуть активные заявки.

        :return: Модель ответа на запрос списка ордеров.
        """
        self.logger.info(
            "Запрос информации о заявках: client_id=%s, include_active=%s, "
            "include_canceled=%s, include_matched=%s",
            client_id,
            include_active,
            include_canceled,
            include_matched,
        )
        model = GetOrdersRequest(
            client_id=client_id,
            include_matched=include_matched,
            include_canceled=include_canceled,
            include_active=include_active,
        )
        result = await self._execute_request(self._orders.GetOrders, model)
        if result:
            self.logger.info("Получена информация о заяках: %s", result)
        return result

    async def create_order(
        self,
        client_id: str,
        security_board: str,
        security_code: str,
        buy_sell: Literal["BUY_SELL_BUY", "BUY_SELL_SELL"] | BuySell,
        quantity: int,
        use_credit: bool = True,
        property: (
            Literal[
                "ORDER_PROPERTY_PUT_IN_QUEUE",
                "ORDER_PROPERTY_CANCEL_BALANCE",
                "ORDER_PROPERTY_IMM_OR_CANCEL",
            ]
            | OrderProperty
        ) = OrderProperty.ORDER_PROPERTY_PUT_IN_QUEUE,
        price: float | None = None,
        condition: OrderCondition | None = None,
        valid_before: OrderValidBefore | None = None,
    ) -> NewOrderResult | None:
        """
        Создание нового ордера.

        :param client_id: Торговый код клиента;
        :param security_board: режим торгов;
        :param security_code: тикер инструмента;
        :param buy_sell: направление сделки;
          BUY_SELL_BUY - Покупка
          BUY_SELL_SELL - Продажа
        :param quantity: объем заявки в лотах;
        :param use_credit: использование кредита (недоступно для
          срочного рынка);
        :param price: цена исполнения заявки. Для рыночной заявки
          указать значение None (или не передавать это поле).
          Для условной заявки необходимо указать цену исполнения;
        :param property: свойства исполнения частично исполненных заявок;
          ORDER_PROPERTY_PUT_IN_QUEUE - неисполненная часть заявки помещается
            в очередь заявок Биржи;
          ORDER_PROPERTY_CANCEL_BALANCE - неисполненная часть
            заявки снимается с торгов;
          ORDER_PROPERTY_IMM_OR_CANCEL - сделки совершаются только
            в том случае, если заявка может быть удовлетворена полностью
            и сразу при выставлении;
        :param condition: типы условных ордеров:
          type - Тип условия:
            ORDER_CONDITION_TYPE_BID - лучшая цена покупки;
            ORDER_CONDITION_TYPE_BID_OR_LAST - лучшая цена покупки или
              сделка по заданной цене и выше;
            ORDER_CONDITION_TYPE_ASK - лучшая цена продажи;
            ORDER_CONDITION_TYPE_ASK_OR_LAST - лучшая цена продажи
              или сделка по заданной цене и ниже;
            ORDER_CONDITION_TYPE_TIME - время выставления заявки на Биржу.
              Параметр OrderCondition.time должен быть установлен;
            ORDER_CONDITION_TYPE_COV_DOWN - обеспеченность ниже заданной;
            ORDER_CONDITION_TYPE_COV_UP: - обеспеченность выше заданной;
            ORDER_CONDITION_TYPE_LAST_UP - сделка на рынке по заданной цене
              или выше;
            ORDER_CONDITION_TYPE_LAST_DOWN - сделка на рынке по заданной
              цене или ниже;
          price - значение цены для условия;
          time - время выставления в UTC;
        :param valid_before: условие по времени действия заявки:
          type - установка временных рамок действия заявки:
            ORDER_VALID_BEFORE_TYPE_TILL_END_SESSION - заявка действует
              до конца сессии;
            ORDER_VALID_BEFORE_TYPE_TILL_CANCELLED - заявка действует,
              пока не будет отменена
            ORDER_VALID_BEFORE_TYPE_EXACT_TIME - заявка действует до
              указанного времени. Параметр OrderValidBefore.time
              должно быть установлен;
          time: время действия заявки в UTC.

        :return: Модель ответа на создание нового ордера.
        """
        self.logger.info(
            "Создание заявки: client_id=%s, security_board=%s, "
            "security_code=%s, buy_sell=%s, quantity=%s, use_credit=%s, "
            "property=%s, price=%s, condition=%s, valid_before=%s.",
            client_id,
            security_board,
            security_code,
            buy_sell,
            quantity,
            use_credit,
            property,
            price,
            condition,
            valid_before,
        )
        model = NewOrderRequest(
            client_id=client_id,
            security_board=security_board,
            security_code=security_code,
            buy_sell=buy_sell,
            quantity=quantity,
            use_credit=use_credit,
            property=property,
            price={"value": price} if price else None,
            condition=condition,
            valid_before=valid_before,
        )
        result = await self._execute_request(self._orders.NewOrder, model)
        if result:
            self.logger.info(
                "Получен ответ на запрос создания заявки: %s.", result
            )
        return result

    async def cancel_order(
        self, client_id: str, transaction_id: int
    ) -> CancelOrderResult | None:
        """
        Отмена ордера.

        Важно: если к лимитной заявке была привязана стоп-заявка,
        то стоп-заявка не будет отменена, пока есть еще
        лимитные заявки по инструменту.

        :param client_id: Торговый код клиента;
        :param transaction_id: идентификатор отменяемой заявки.

        :return: Модель ответа на отмену ордера.
        """
        self.logger.info(
            "Отмена заявки: client_id=%s, transaction_id=%s.",
            client_id,
            transaction_id,
        )
        model = CancelOrderRequest(
            client_id=client_id, transaction_id=transaction_id
        )
        result = await self._execute_request(self._orders.CancelOrder, model)
        if result:
            self.logger.info(
                "Получен ответ на запрос отмены заявки: %s.", result
            )
        return result

    async def get_stops(
        self,
        client_id: str,
        include_active: bool = True,
        include_canceled: bool = True,
        include_executed: bool = True,
    ) -> GetStopsResult | None:
        """
        Получение списка стоп-ордеров.

        :param client_id: Торговый код клиента;
        :param include_executed: вернуть исполненные стоп-заявки;
        :param include_canceled: вернуть отмененные заявки;
        :param include_active: вернуть активные заявки.

        :return: Модель ответа на запрос списка стоп-ордеров.
        """
        self.logger.info(
            "Запрос информации о стоп-заявках: "
            "client_id=%s, include_active=%s, "
            "include_canceled=%s, include_executed=%s.",
            client_id,
            include_active,
            include_canceled,
            include_executed,
        )
        model = GetStopsRequest(
            client_id=client_id,
            include_active=include_active,
            include_canceled=include_canceled,
            include_executed=include_executed,
        )
        result = await self._execute_request(self._stops.GetStops, model)
        if result:
            self.logger.info("Получена информация о стоп-заявках: %s.", result)
        return result

    async def create_stop(
        self,
        client_id: str,
        security_board: str,
        security_code: str,
        buy_sell: Literal["BUY_SELL_BUY", "BUY_SELL_SELL"] | BuySell,
        stop_loss: StopLoss | None = None,
        take_profit: TakeProfit | None = None,
        expiration_date: Timestamp | None = None,
        link_order: int | None = None,
        valid_before: OrderValidBefore | None = None,
    ) -> NewStopResult | None:
        """
        Создание нового стоп-ордера.

        :param client_id: Торговый код клиента;
        :param security_board: режим торгов;
        :param security_code: тикер инструмента;
        :param buy_sell: направление сделки;
          BUY_SELL_BUY - Покупка
          BUY_SELL_SELL - Продажа
        :param stop_loss: стоп-лосс:
          activation_price - цена активации;
          price - цена заявки;
          market_price - по рынку;
          quantity - объем стоп-заявки;
            value - значение объема;
            units - единицы объема:
              STOP_QUANTITY_UNITS_PERCENT - значение а процентах;
              STOP_QUANTITY_UNITS_LOTS - значение в лотах;
            time: защитное время, сек;
            use_credit: использовать кредит.
        :param take_profit: тейк профит заявка:
          activation_price - цена активации
          correction_price - коррекция
            value - Значение цены
            units - Единицы цены
              STOP_PRICE_UNITS_PERCENT - Значение в процентах
              STOP_PRICE_UNITS_PIPS - Значение в лотах
          spread_price - Защитный спрэд:
            value - значение цены;
            units - единицы цены:
              STOP_PRICE_UNITS_PERCENT - значение в процентах;
              STOP_PRICE_UNITS_PIPS - значение в лотах;
            market_price - по рынку;
            quantity - Количество тейк-профит заявки:
              value - значение объема;
              units - единицы объема:
                STOP_QUANTITY_UNITS_PERCENT - значение а процентах;
                STOP_QUANTITY_UNITS_LOTS - значение в лотах;
            time - защитное время, сек;
            use_credit - использовать кредит.
        :param expiration_date: дата экспирации заявки FORTS;
        :param link_order: биржевой номер связанной (активной) заявки;
        :param valid_before: условие по времени действия заявки:
          type - установка временных рамок действия заявки:
            ORDER_VALID_BEFORE_TYPE_TILL_END_SESSION - заявка действует
              до конца сессии;
            ORDER_VALID_BEFORE_TYPE_TILL_CANCELLED - заявка действует,
              пока не будет отменена
            ORDER_VALID_BEFORE_TYPE_EXACT_TIME - заявка действует до
              указанного времени. Параметр OrderValidBefore.time
              должно быть установлен;
          time: время действия заявки в UTC.

        :return: Модель ответа на создание новго стоп-ордера.
        """
        self.logger.info(
            "Создание стоп-заявки: client_id=%s, security_board=%s, "
            "security_code=%s, buy_sell=%s, stop_loss=%s, take_profit=%s, "
            "expiration_date=%s, link_order=%s, valid_before=%s.",
            client_id,
            security_board,
            security_code,
            buy_sell,
            stop_loss,
            take_profit,
            expiration_date,
            link_order,
            valid_before,
        )
        model = NewStopRequest(
            client_id=client_id,
            security_board=security_board,
            security_code=security_code,
            buy_sell=buy_sell,
            stop_loss=stop_loss,
            take_profit=take_profit,
            expiration_date=expiration_date,
            link_order=link_order,
            valid_before=valid_before,
        )
        result = await self._execute_request(self._stops.NewStop, model)
        if result:
            self.logger.info(
                "Получен ответ на запрос создания стоп-заявки: %s.", result
            )
        return result

    async def cancel_stop(
        self, client_id: str, stop_id: int
    ) -> CancelStopResult | None:
        """
        Отмена стоп-ордера.

        :param client_id: Торговый код клиента;
        :param stop_id: идентификатор отменяемой стоп-заявки.

        :return: Модель ответа на отмену стоп-ордера.
        """
        self.logger.info(
            "Отмена стоп-заявки: " "client_id=%s, stop_id=%s.",
            client_id,
            stop_id,
        )
        model = CancelStopRequest(client_id=client_id, stop_id=stop_id)
        result = await self._execute_request(self._stops.CancelStop, model)
        if result:
            self.logger.info(
                "Получен ответ на запрос отмены стоп-заявки: %s.", result
            )
        return result

    async def subscribe_orders_trades(
        self,
        request_id: str,
        client_ids: Iterable[str],
        include_trades: bool = True,
        include_orders: bool = True,
    ) -> None:
        """
        Подписка на заявки и сделки.

        :param request_id: ID запроса;
        :param client_ids: id счетов;
        :param include_trades: включить информацию о сделках;
        :param include_orders: включить информацию о заявках.
        """
        self.logger.info(
            "Подписка на заявки и сделки: request_id=%s, "
            "client_ids=%s, include_trades=%s, include_orders=%s",
            request_id,
            client_ids,
            include_trades,
            include_orders,
        )
        model = OrderTradeSubscribeRequest(
            client_ids=client_ids,
            request_id=request_id,
            include_trades=include_trades,
            include_orders=include_orders,
        )
        request = SubscriptionRequest(order_trade_subscribe_request=model)
        await self._execute_subscribe_request(request)

    async def unsubscribe_orders_trades(self, request_id: str) -> None:
        """
        Отмена подписки на ордера и сделки.

        :param request_id: ID запроса.
        """
        self.logger.info(
            "Отписка от заявок и сделок: request_id=%s.", request_id
        )
        model = OrderTradeUnsubscribeRequest(request_id=request_id)
        request = SubscriptionRequest(order_trade_unsubscribe_request=model)
        await self._execute_subscribe_request(request)

    async def subscribe_order_book(
        self, request_id: str, security_board: str, security_code: str
    ) -> None:
        """
        Подписка на стакан.

        :param request_id: ID запроса;
        :param security_board: режим торгов;
        :param security_code: тикер инструмента.
        """
        self.logger.info(
            "Подиска на стакан: request_id=%s, "
            "security_board=%s, security_code=%s."
        )
        model = OrderBookSubscribeRequest(
            request_id=request_id,
            security_board=security_board,
            security_code=security_code,
        )
        request = SubscriptionRequest(order_book_subscribe_request=model)
        await self._execute_subscribe_request(request)

    async def unsubscribe_order_book(
        self, request_id: str, security_board: str, security_code: str
    ) -> None:
        """
        Отмена подписки на стакан.

        :param request_id: ID запроса;
        :param security_board: режим торгов;
        :param security_code: тикер инструмента.
        """
        self.logger.info(
            "Отписка от стакана: request_id=%s, "
            "security_board=%s, security_code=%s."
        )
        model = OrderBookUnsubscribeRequest(
            request_id=request_id,
            security_board=security_board,
            security_code=security_code,
        )
        request = SubscriptionRequest(order_book_unsubscribe_request=model)
        await self._execute_subscribe_request(request)
