import httpx
import asyncio


async def main():

    username = "developer"
    password = "C1sco12345"
    BASE_URL = "https://sandbox-iosxe-latest-1.cisco.com/restconf/data"
    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    }

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(
            f"{BASE_URL}/Cisco-IOS-XE-native:native/version",
            auth=(
                username,
                password,
            ),
            headers=headers,
        )
        print(response.json())


if __name__ == "__main__":
    asyncio.run(main())
