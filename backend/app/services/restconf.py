from typing import Optional

import httpx
from fastapi import HTTPException, status


BASE_URL = "https://{host}/restconf/data"
HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}


class RESTCONF:
    """
    A class which handles and saves HTTP sessions. Currently only for IOS-XE.
    Will eventually be extended to support other platforms.
    """

    def __init__(self, host: str, username: str, password: str) -> "RESTCONF":
        """
        Save information needed to establish the RESTCONF connection/HTTP session
        """
        self.host = host
        self.username = username
        self.password = password
        self.url = BASE_URL.format(host=host)
        self.client = httpx.AsyncClient(
            auth=(self.username, self.password), verify=False, headers=HEADERS
        )

    async def request(
        self,
        method: str,
        path: str,
        data: dict = None,
        headers: Optional[dict] = HEADERS,
    ) -> httpx.Response:
        """
        Generic request method with ability to pass method, path, and request data

        Args:
            method: HTTP method to be used with request
            path: API endpoint
            data: Request data as a python dictionary
        """

        try:
            response = await self.client.request(
                method=method, url=f"{self.url}{path}", data=data, headers=headers
            )
            response.raise_for_status()
            return response
        except httpx.HTTPError as err:
            raise HTTPException(
                status_code=err.response.status_code, detail=err.response.json()
            )
        finally:
            await self.close()

    async def get(self, path: str, headers: Optional[dict] = HEADERS) -> httpx.Response:
        """
        Generic get request to return data from a specific path after base url

        Args:
            path: API endpoint to retrieve data from
        """
        return await self.request(method="GET", path=path, headers=headers)

    async def post(
        self, path: str, data: dict = None, headers: Optional[dict] = HEADERS
    ) -> httpx.Response:
        """
        Generic get request to return data from a specific path after base url

        Args:
            path: API endpoint to retrieve data from
        """
        return await self.request(method="POST", path=path, data=data, headers=headers)

    async def verify_connectivity(self):
        """
        Verifies RESTCONF connectivity to the device
        """
        try:
            response = await self.client.get(f"https://{self.host}/restconf")
            response.raise_for_status()
        except httpx.HTTPError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Could not verify device",
            )
        return True

    async def get_xpath_data(self, xpath: str):
        """
        Builds a get request using the xpath passed to the given device and returns JSON data
        """
        response = await self.get(path=f"/{xpath}")
        return response.json()

    async def get_os_version(self) -> str:
        """
        Returns the device's OS Version
        """
        response = await self.get(path="/Cisco-IOS-XE-native:native/version")
        data = response.json()
        return data["Cisco-IOS-XE-native:version"]

    async def get_hostname(self) -> str:
        """
        Returns the device's hostname
        """
        response = await self.get(path="/Cisco-IOS-XE-native:native/hostname")
        data = response.json()
        return data["Cisco-IOS-XE-native:hostname"]

    async def close(self) -> None:
        """Close the session"""
        return await self.client.aclose()