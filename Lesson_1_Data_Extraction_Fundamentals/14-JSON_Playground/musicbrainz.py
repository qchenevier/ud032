# To experiment with this code freely you will have to run this code locally.
# We have provided an example json output here for you to look at,
# but you will not be able to run any queries through our UI.
import json
import requests
import os

PROXY_CONFIG_FILE = 'proxy_config.py'
if os.path.exists(PROXY_CONFIG_FILE):
    exec(open(PROXY_CONFIG_FILE).read())

BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print("requesting", r.url)

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    if type(data) == dict:
        print(json.dumps(data, indent=indent, sort_keys=True))
    else:
        print(data)


def main():
    results = query_by_name(ARTIST_URL, query_type["simple"], "Lucero")
    # pretty_print(results)

    artist_id = results["artists"][0]["id"]
    print("ARTIST:")
    pretty_print(results["artists"][0])

    artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
    releases = artist_data["releases"]
    print("ONE RELEASE:")
    pretty_print(releases[0], indent=2)
    release_titles = [r["title"] for r in releases]

    print("ALL TITLES:")
    for t in release_titles:
        print(t)


main()

query_name = 'First Aid Kit'
res = query_by_name(ARTIST_URL, query_type['simple'], query_name)
artist_with_exact_name = [a for a in res['artists'] if query_name == a['name']]
print(len(artist_with_exact_name))

query_name = 'Queen'
res = query_by_name(ARTIST_URL, query_type['simple'], query_name)
artist_with_exact_name = [a for a in res['artists'] if query_name == a['name']]
print(artist_with_exact_name[2]['begin-area']['name'])

query_name = 'The Beatles'
res = query_by_name(ARTIST_URL, query_type['simple'], query_name)
artist_with_exact_name = [a for a in res['artists'] if query_name == a['name']]
the_beatles = artist_with_exact_name[0]
spanish_alias = [a for a in the_beatles['aliases'] if a['locale'] == 'es'][0]
print(spanish_alias['name'])

query_name = 'Nirvana'
res = query_by_name(ARTIST_URL, query_type['simple'], query_name)
artist_with_exact_name = [a for a in res['artists'] if query_name == a['name']]
nirvana = artist_with_exact_name[4]
print(a['disambiguation'])

query_name = 'One Direction'
res = query_by_name(ARTIST_URL, query_type['simple'], query_name)
artist_with_exact_name = [a for a in res['artists'] if query_name == a['name']]
one_direction = artist_with_exact_name[0]
print(one_direction['life-span']['begin'])
