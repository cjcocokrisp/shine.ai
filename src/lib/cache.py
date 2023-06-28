import pokebase as pb
from pathlib import Path
import urllib
import os

def clear_cache():
    path = Path('cache')
    for file in path.iterdir():
        os.remove(file)

def cache_names():
    full_list = pb.pokemon('?limit=2000&offset=0')
    to_write = []
    for mon in full_list.results:
        to_write.append(str(mon.name).capitalize() + '\n')
        file = open('cache/pkmn-names-full.txt', 'w')
        file.writelines(to_write)
        file.close()

def cache_img(request):
    try:
        mon_api_data = pb.APIResource('pokemon', request.lower())

        sprite = pb.SpriteResource('pokemon', str(mon_api_data.id))
        urllib.request.urlretrieve(str(sprite.url), f'cache/N{request.lower()}.png') 

        sprite = pb.SpriteResource('pokemon', str(mon_api_data.id), shiny=True)
        urllib.request.urlretrieve(str(sprite.url), f'cache/S{request.lower()}.png') 
    except:
        pass # Catch the exception if there is no sprite for the pokemon.





