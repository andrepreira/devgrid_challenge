from http import HTTPStatus

import requests
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry, disable_warnings, exceptions

disable_warnings(
    exceptions.InsecureRequestWarning
)  # Disabling insecure requests warning


class RequestSession:

    @staticmethod
    def create_session_request(proxy: bool = False) -> requests.Session:
        retries = Retry(
            total=5,
            backoff_factor=1,  # type: ignore
            status_forcelist=[
                HTTPStatus.BAD_REQUEST.value,
                HTTPStatus.FORBIDDEN.value,
                HTTPStatus.NOT_FOUND.value,
                HTTPStatus.UNPROCESSABLE_ENTITY.value,
                HTTPStatus.INTERNAL_SERVER_ERROR.value,
                HTTPStatus.BAD_GATEWAY.value,
                HTTPStatus.SERVICE_UNAVAILABLE.value,
                HTTPStatus.GATEWAY_TIMEOUT.value,
            ],
        )
        request_session = Session()
        request_session.mount("http://", HTTPAdapter(max_retries=retries))
        request_session.mount("https://", HTTPAdapter(max_retries=retries))

        return request_session
