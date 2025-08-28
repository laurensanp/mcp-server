from server import mcp
import requests
from datetime import datetime, timedelta
import pytz

@mcp.tool()
def get_weekly_anime_releases() -> str:
    """
    Gibt eine Liste zurück mit Anime-Erscheinungen der letzten 3 vergangenen Tage und 3 kommenden Tage.
    Returns:
        Eine Liste mit Animes, Datum, Uhrzeit, Anbieter. Kann aber mögliche Errors beinhalten.
    """

    local_timezone_str = "Europe/Berlin"
    try:
        local_tz = pytz.timezone(local_timezone_str)
    except Exception as e:
        return f"Ungültige Zeitzone: {local_timezone_str}. Fehler: {e}"

    now_local = datetime.now(local_tz)

    # Zeitfenster berechnen (UTC)
    try:
        start_utc = (now_local - timedelta(days=3)).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(pytz.utc)
        end_utc = (now_local + timedelta(days=3)).replace(hour=23, minute=59, second=59, microsecond=999999).astimezone(pytz.utc)
        start_ts = int(start_utc.timestamp())
        end_ts = int(end_utc.timestamp())
    except Exception as e:
        return f"Fehler beim Berechnen des Zeitfensters: {e}"

    query = '''
    query ($page: Int, $perPage: Int, $airingAt_greater: Int, $airingAt_lesser: Int) {
      Page(page: $page, perPage: $perPage) {
        pageInfo { hasNextPage }
        airingSchedules(sort: TIME, airingAt_greater: $airingAt_greater, airingAt_lesser: $airingAt_lesser) {
          airingAt
          episode
          media {
            title { romaji english }
            externalLinks { site url }
          }
        }
      }
    }
    '''

    variables = {
        'airingAt_greater': start_ts,
        'airingAt_lesser': end_ts,
        'page': 1,
        'perPage': 50
    }

    url = 'https://graphql.anilist.co'
    releases = []
    output = []

    try:
        test_resp = requests.get("https://graphql.anilist.co")
        if test_resp.status_code not in (200, 400, 405):
            return "AniList API ist derzeit nicht erreichbar."
    except Exception as e:
        return f"Netzwerkfehler beim Testen der AniList API: {e}"

    # Daten von AniList API abrufen (mit Pagination)
    while True:
        try:
            resp = requests.post(url, json={'query': query, 'variables': variables})
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            return f"Error fetching data from AniList API: {e}"

        if 'errors' in data:
            return f"AniList API errors: {data['errors']}"

        page = data['data']['Page']
        releases.extend(page['airingSchedules'])
        if not page['pageInfo']['hasNextPage']:
            break
        variables['page'] += 1

    if not releases:
        return "Keine Anime-Veröffentlichungen im angegebenen Zeitraum gefunden."

    # Favoritenliste
    preferred_titles = [
        "Tensei Shitara Dai Nana Ouji Dattanode, Kimamani Majutsu wo Kiwamemasu 2nd Season",
        "The Water Magician",
        "Call of the Night Season 2",
        "The Fragrant Flower Blooms with Dignity",
        "Gachiakuta",
        "Dr. STONE: SCIENCE FUTURE Part 2",
        "Dandadan 2nd Season",
        "Dealing with Mikadono Sisters Is a Breeze"
    ]
    preferred_titles_lower = [t.lower() for t in preferred_titles]

    # Filtere und bereite Ausgaben vor
    filtered = []
    for r in releases:
        try:
            airing_utc = datetime.fromtimestamp(r['airingAt'], pytz.utc)
            airing_local = airing_utc.astimezone(local_tz)
            romaji = r['media']['title']['romaji']
            english = r['media']['title']['english']
        except Exception as e:
            continue

        # Nur bevorzugte Titel
        display_title = None
        if romaji and romaji.lower() in preferred_titles_lower:
            display_title = romaji
        elif english and english.lower() in preferred_titles_lower:
            display_title = english
        if not display_title:
            continue

        # Anbieter
        links = r['media'].get('externalLinks') or []
        providers = [l['site'] for l in links if l.get('site') and l.get('url')]
        provider_str = "Crunchyroll" if "Crunchyroll" in providers else (", ".join(providers) if providers else "Nicht verfügbar")

        filtered.append({
            'date': airing_local.strftime('%A, %d.%m.%Y'),
            'time': airing_local.strftime('%H:%M'),
            'title': display_title,
            'episode': r['episode'],
            'providers': provider_str
        })

    if not filtered:
        return "Keine Veröffentlichungen für die letzten 3 Tage und die nächsten 3 Tage gefunden, die in Ihrer Liste sind."

    # Sortieren nach Datum und Uhrzeit
    try:
        filtered.sort(key=lambda x: (datetime.strptime(x['date'], '%A, %d.%m.%Y'), datetime.strptime(x['time'], '%H:%M')))
    except Exception as e:
        return f"Fehler beim Sortieren der Ergebnisse: {e}"

    # Ausgabe formatieren
    output.append(
        f"Anime-Veröffentlichungen für die letzten 3 Tage und die nächsten 3 Tage, beginnend am {(now_local - timedelta(days=3)).strftime('%d.%m.%Y')} (Ihre Zeitzone: {local_timezone_str}):"
    )
    last_date = None
    for entry in filtered:
        if entry['date'] != last_date:
            output.append(f"\n--- {entry['date']} ---")
            last_date = entry['date']
        output.append(f"{entry['time']} - {entry['title']} Episode {entry['episode']} (Anbieter: {entry['providers']})")
    return "\n".join(output)