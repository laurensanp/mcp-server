import requests

test_resp = requests.get("https://graphql.anilist.co")
if test_resp.status_code not in (200, 400, 405):
    print("AniList API ist derzeit nicht erreichbar.")