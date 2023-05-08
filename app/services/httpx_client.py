import httpx
from fastapi import HTTPException
from loguru import logger
from starlette import status

from app.resources.strings import ERROR_MESSAGE_UNPROCESSABLE_ENTITY


class HttpxClient:
    def __init__(self, base_url: str = "") -> None:
        self.base_url = base_url
        self.timeout = 20

    async def get(
        self, url: str, query_params: dict | None = None, headers: dict | None = None
    ) -> dict:
        return await self._request("GET", url, query_params=query_params, headers=headers)

    async def post(self, url: str, json: dict, headers: dict | None = None) -> dict:
        return await self._request("POST", url, json=json, headers=headers)

    async def _request(
        self,
        method: str,
        url: str,
        query_params: dict | None = None,
        json: dict | None = None,
        headers: dict | None = None,
    ) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                logger.info(f"Sending {method} request to {self.base_url + url}")
                response = await client.request(
                    method=method,
                    url=self.base_url + url,
                    params=query_params,
                    json=json,
                    headers=headers,
                )

                response.raise_for_status()
                logger.info(f"Received response: {response.status_code}")

                return response.json()
            except httpx.ConnectError as e:
                logger.error(f"Connection error: {e}")
                raise Exception(
                    "Не удалось установить соединение с сервером. Пожалуйста, проверьте ваше соединение и URL."
                )
            except httpx.HTTPStatusError as http:
                logger.error(f"Server error {http.response.status_code}: {http.response.text}")
                if http.response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
                    logger.error(f"Server error 422: {response.text}")
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail=ERROR_MESSAGE_UNPROCESSABLE_ENTITY,
                    )
