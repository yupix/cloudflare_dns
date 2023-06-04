import asyncio
import os
from typing import Any
import aiohttp
from dotenv import load_dotenv

from type import ICustomZone, IDNSRecord, IResponse, IZone
from utils import input_int

load_dotenv()


CLOUDFLARE_TOKEN = os.environ.get("CLOUDFLARE_TOKEN")
CLOUDFLARE_MAIL = os.environ.get("CLOUDFLARE_MAIL")

if all([CLOUDFLARE_TOKEN, CLOUDFLARE_MAIL]) is False:
    raise Exception("CLOUDFLARE_TOKEN or CLOUDFLARE_MAIL is not set")

headers = {
    "X-Auth-Email": CLOUDFLARE_MAIL,
    "X-Auth-Key": CLOUDFLARE_TOKEN,
    "Content-Type": "application/json",
}


class CloudFlare:
    def __init__(self):
        self.session: aiohttp.ClientSession
        self.zones: list[ICustomZone] = []

    async def create_session(self):
        self.session = aiohttp.ClientSession(
            "https://api.cloudflare.com", headers=headers
        )

    async def get_zone_id(self):
        res = await self.session.get(f"/client/v4/zones")
        res_zones: IResponse[list[IZone]] = await res.json()
        for zone in res_zones["result"]:
            zone_id = zone["id"]
            domain = zone["name"]
            self.zones.append({"zone_id": zone_id, "domain": domain})
        return self.zones

    async def get_dns_records(self, zone: ICustomZone):
        res = await self.session.get(f"/client/v4/zones/{zone['zone_id']}/dns_records")
        res_records: IResponse[list[IDNSRecord]] = await res.json()
        return res_records["result"]

    async def patch_dns_record(self, record: IDNSRecord, updated_ip_address: str):
        res = await self.session.patch(
            f"/client/v4/zones/{record['zone_id']}/dns_records/{record['id']}",
            json={
                "content": updated_ip_address,
                "name": record["name"],
                "type": record["type"],
            },
        )
        res_record: IResponse[IDNSRecord] = await res.json()
        return res_record

    async def close_session(self):
        await self.session.close()


async def main():
    cloudflare = CloudFlare()
    await cloudflare.create_session()
    zones = await cloudflare.get_zone_id()
    print("変更したいドメインを選択してください")
    can_select_number: list[int] = []
    for i, zone in enumerate(zones):
        can_select_number.append(i)
        print(i, zone["domain"])
    selected_domain = input_int(">>>", can_select_number)
    use_zone = zones[int(selected_domain)]
    print("更新前のipアドレスを入力してください")
    old_ip_address = input(">>>")
    print("更新後のipアドレスを入力してください")
    new_ip_address = input(">>>")

    dns_records = await cloudflare.get_dns_records(use_zone)
    for dns_record in dns_records:
        if dns_record["content"] == old_ip_address:
            await cloudflare.patch_dns_record(dns_record, new_ip_address)
            print(
                f'{dns_record["name"]}を更新しました: {dns_record["content"]} => {new_ip_address}'
            )
    await cloudflare.close_session()


if __name__ == "__main__":
    asyncio.run(main())
