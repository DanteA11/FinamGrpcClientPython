import datetime
import logging
from asyncio import Task, create_task, iscoroutine, sleep

from grpc import RpcError, ssl_channel_credentials
from grpc.aio import (
    Channel,
    Metadata,
    UnaryStreamMultiCallable,
    UnaryUnaryMultiCallable,
    secure_channel,
)

from finam_grpc_client.base import AbstractFinamClient
from finam_grpc_client.proto.grpc.tradeapi.v1.auth.auth_service_pb2 import (
    SubscribeJwtRenewalRequest,
    SubscribeJwtRenewalResponse,
    TokenDetailsRequest,
    TokenDetailsResponse,
)


class FinamClient(
    AbstractFinamClient[
        Channel,
        UnaryUnaryMultiCallable,
        UnaryStreamMultiCallable,
    ]
):
    logger = logging.getLogger("finam_grpc_client.asyncio.FinamClient")

    def __init__(self, secret: str, *, url: str = "api.finam.ru:443"):
        super().__init__(secret, url)
        self.__job: Task | None = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()

    async def start(self) -> None:
        super().start()
        self.__job = create_task(
            self.__update_token_job(), name="UpdateTokenJob"  # type: ignore
        )
        self.logger.debug("Waiting for the session token to be updated")  # type: ignore
        while self.session_token is None:  # type: ignore
            await sleep(1)
        self.logger.info("FinamClient has started")  # type: ignore

    async def stop(self) -> None:
        coro = super().stop()
        if iscoroutine(coro):
            await coro
        self.logger.info("FinamClient has stopped")  # type: ignore

    @property
    def metadata(self) -> Metadata:
        return Metadata(
            ("authorization", self.session_token),
        )

    def _create_channel(self):
        return secure_channel(self.url, ssl_channel_credentials())

    async def __update_token_job(self):
        response: SubscribeJwtRenewalResponse
        token_details: TokenDetailsResponse
        timezone = datetime.datetime.now().astimezone().tzinfo
        self.logger.info("Launching a session token renewal task")
        while self.started:
            try:
                async for response in self.subscribe_jwt_renewal(
                    request=SubscribeJwtRenewalRequest(secret=self.secret)
                ):
                    self.session_token = response.token
                    token_details = await self.token_details(
                        request=TokenDetailsRequest(token=response.token)
                    )
                    self.logger.debug(
                        "New auth token received. Expiration: %s",
                        token_details.expires_at.ToDatetime(
                            tzinfo=timezone
                        ).isoformat(),
                    )
            except RpcError as e:
                self.logger.exception(e.details(), exc_info=e)
                await sleep(10)
