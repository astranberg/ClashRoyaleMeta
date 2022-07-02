import clashroyale
import asyncio

# Define Tokens
officialAPIToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9" \
                   ".eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImYyZjUzYmI2LWIyMDQtNGRkYi1" \
                   "iMGZjLTk0ZTE4ZWU3YzQ2ZSIsImlhdCI6MTU3NDYxNDgzMywic3ViIjoiZGV2ZWxvcGVyLzZlYmYzNzdmLWVkNjQtMmFlZC0" \
                   "2MjRhLWE3Nzg5YmM4OGZiNCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZl" \
                   "ciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI5OC4xOTUuMTU5LjgyIl0sInR5cGUiOiJjbGllbnQifV19.H13g" \
                   "VRs6fkSDyKEAAqPJKscx2AtN9sDbHaWNm2GSpgVZTTAe_sJM_yKkibMTCyOLu8kvOw7xcCOxycIydqqeUw"
unofficialAPIToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTQ0MywiaWRlbiI6IjIyNzk4NjE5NzM3MTE1ODUyOCIsIm1k" \
                     "Ijp7InVzZXJuYW1lIjoiS2luZ0tvbmciLCJkaXNjcmltaW5hdG9yIjoiOTcxOSIsImtleVZlcnNpb24iOjN9LCJ0cyI6MTU" \
                     "3NjgwMjAxMTk1Mn0.tUBrvk38lBSrg9ilpshqBD9PbzFoOqImLVrM8hUucLg"

clan_groups = [
    ['PPCLCJG9', '2LRU2J', 'PGLQ0VQ', 'YU2RQG9', '2LVRQ29'],
    ['PYP8UPJV', 'P9L0CYY0', 'Y2RGQPJ', '8P2GYJ8', '9VQJPL2L'],
    ['RYPRGCJ', '809R8PG8', 'PJY9PP98', '2GCQLC', '2GL2QPPL']
]
clan_group = ['PULJG98R', '2PLPJ9CL', '8PRVJC', '9RQP2G9Y', 'CQGRYV']


async def get_clans(cr, clan_groups):
    return await asyncio.gather(*[
        cr.get_clan(group)
        for group in clan_groups
    ])


async def main():
    cr = clashroyale.official_api.Client(officialAPIToken, is_async=True, timeout=30)
    try:
        print(clan_group)
        clan = await get_clans(cr, clan_group)
        print(clan[1].tag)
    finally:
        await cr.close()
        await asyncio.sleep(2)
        print('end')

asyncio.run(main())
