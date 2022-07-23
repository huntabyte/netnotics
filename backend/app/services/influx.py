import asyncio
import os

from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync


# InfluxDB Healthcheck


async def health_check():
    async with InfluxDBClientAsync(
        url="http://localhost:8086",
        token=os.environ.get("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"),
        org=os.environ.get("DOCKER_INFLUXDB_INIT_ORG"),
    ) as client:
        ready = await client.ping()
        print(f"InfluxDB: {ready}")


# async def query():
#     async with InfluxDBClientAsync(
#         url="http://localhost:8086",
#         token="password123",
#         org="netnotics",
#     ) as client:
#         # query_api = client.query_api()
#         # #         records = await query_api.query_raw(f'from(bucket: "telegraf") \
#         # #                 |> range(start: v.timeRangeStart, stop: v.timeRangeStop) \
#         # #                 |> filter(fn: (r) => r["_measurement"] == "Cisco-IOS-XE-native:native") \
#         # #                 |> filter(fn: (r) => r["_field"] == "hostname") \
#         # #                 |> filter(fn: (r) => r["host"] == "9499facd8746")'
#         # # )
#         # print(records)


if __name__ == "__main__":
    asyncio.run(query())
