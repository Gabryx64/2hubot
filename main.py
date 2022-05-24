import asyncio
import mimetypes
import os
import json
import requests
import random
from datetime import date
from dotenv import load_dotenv
from mastodon import Mastodon
from booru import Danbooru

queries = [
    [("Marisa", "kirisame_marisa"), ("Mokou", "fujiwara_no_mokou"), ("Mima", "mima_(touhou)"), ("Meiling", "hong_meiling")],
    [("Tewi", "inaba_tewi"), ("Tenshi", "hinanawi_tenshi"), ("Takane", "yamashiro_takane")],
    [("Whiterock", "letty_whiterock"), ("White", "lily_white")],
    [("Tewi", "inaba_tewi"), ("Tenshi", "hinanawi_tenshi"), ("Takane", "yamashiro_takane")],
    [("Flan", "flandre_scarlet"), ("Fumo", "fumo_(doll)")],
    [("Sakuya", "izayoi_sakuya"), ("Sanae", "kochiya_sanae"), ("Suwako", "moriya_suwako"), ("Satori", "komeiji_satori"),
     ("Seika", "kaku_seiga"), ("Suika", "ibuki_suika")],
    [("Sakuya", "izayoi_sakuya"), ("Sanae", "kochiya_sanae"), ("Suwako", "moriya_suwako"), ("Satori", "komeiji_satori"),
     ("Seika", "kaku_seiga"), ("Suika", "ibuki_suika")],
]


async def main():
    load_dotenv()
    mastodon = Mastodon(
        access_token=os.environ["TKN"],
        api_base_url=os.environ["INST_URL"])
    while True:
        day = random.choice(queries[date.today().weekday()])
        img = json.JSONDecoder().decode(await Danbooru().search(query=day[1], gacha=True))["file_url"]
        data = []
        for chunk in requests.get(img, stream=True):
            for byte in chunk:
                data.append(byte)
        media = mastodon.media_post(bytes(data), mime_type=mimetypes.guess_type(img)[0])
        mastodon.status_post(f"Happy {day[0]} day!\n\n#2hubot", sensitive=True, media_ids=media)
        await asyncio.sleep(86400)


if __name__ == "__main__":
    asyncio.run(main());
