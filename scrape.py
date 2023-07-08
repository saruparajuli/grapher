from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import json
from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph/<anime_name>', methods=['GET', 'POST'])
@cache.cached(timeout=60*60)
def graph(anime_name):
    code = anime_name.split('_=')[1]
    name = anime_name.split('_=')[0]
    characters = scrape_characters(f'https://myanimelist.net/anime/{code}/{name}/characters')
    characters = sorted(characters, key=lambda d: d['name'])
    char_names = [char['name'] for char in characters]
    char_favorites = [char['favorites'] for char in characters]

    return render_template('graph.html', anime_name=name, char_names=json.dumps(char_names), char_favorites=json.dumps(char_favorites))

@app.route('/search/<anime_name>', methods=['GET','POST'])
@cache.cached(timeout=60*60)
def get_urls(anime_name):
    url = f'https://myanimelist.net/anime.php?cat=anime&q={anime_name}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    animes = []
    results = soup.find_all(class_='picSurround')
    for result in results:
        result = result.find(class_='hoverinfo_trigger')
        try:
            image = result.find('img')['data-srcset'].strip().split('x, ')[1].replace(' 2x', '')
            name = result.find('img')['alt']
            link = result['href']
            code = link.strip().split('/')[-2]
        except:
            print(result)
        animes.append({
            'name': name,
            'image': image,
            'link': link,
            'code': code
        })
    return render_template('search.html', animes=animes)

def scrape_characters(anime_url):
    url = f'{anime_url}/characters'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    characters = []
    results = soup.find_all(class_='js-anime-character-table')
    for result in results:
        char_name = result.find(class_='h3_character_name').text
        char_favorites = result.find_all(class_='spaceit_pad')
        for char in char_favorites:
            if 'Favorites' in char.text:
                char_favorite = char.text.strip().split(' ')[0].replace(',','')
        characters.append({
            'name': char_name,
            'favorites': int(char_favorite)
        })

    return characters


if __name__ == '__main__':
    app.run(debug=True)
