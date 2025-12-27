import datetime
import logging
from threading import Thread
from time import sleep

from grpc import (
    Channel,
    RpcError,
    UnaryStreamMultiCallable,
    UnaryUnaryMultiCallable,
    secure_channel,
    ssl_channel_credentials,
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
    logger = logging.getLogger("finam_grpc_client.FinamClient")

    def __init__(self, secret: str, *, url: str = "api.finam.ru:443"):
        super().__init__(secret, url)
        self.__job: Thread | None = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self) -> None:
        super().start()
        self.__job = Thread(
            target=self.__update_token_job,  # type: ignore
            name="UpdateTokenJob",
            daemon=True,
        )
        self.__job.start()  # type: ignore
        self.logger.debug("Waiting for the session token to be updated")  # type: ignore
        while self.session_token is None:  # type: ignore
            sleep(1)
        self.logger.info("FinamClient has started")  # type: ignore

    def stop(self):
        super().stop()
        self.logger.info("FinamClient has stopped")  # type: ignore

    @property
    def metadata(self) -> tuple[tuple[str, str], ...]:
        return (("authorization", self.session_token),)

    def _create_channel(self):
        return secure_channel(self.url, ssl_channel_credentials())

    def __update_token_job(self):
        response: SubscribeJwtRenewalResponse
        token_details: TokenDetailsResponse
        timezone = datetime.datetime.now().astimezone().tzinfo
        self.logger.info("Launching a session token renewal task")
        while self.started:
            try:
                for response in self.subscribe_jwt_renewal(
                    request=SubscribeJwtRenewalRequest(secret=self.secret)
                ):
                    self.session_token = response.token
                    token_details = self.token_details(
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
                sleep(10)
