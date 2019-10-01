from bs4 import BeautifulSoup
import requests
from math import ceil
from time import sleep
import json

def extract_urls(soup):
    results = soup.find_all("a", {'class':'view-complete-item'})
    result_urls = []
    for result in results:
        result_urls.append(result['href'])
    return result_urls

def get_number_of_pages(soup, results_per_page=18):
    num_results = soup.find_all("span", {'class':'matching-count'})[0].contents[0]
    num_results = int(''.join(num_results.split(',')))
    num_pages = ceil(num_results/18)
    return num_pages

cuisines = [
    'scandinavian',
    'italian',
    'french',
    'african',
    'cajun-creole',
    'central-south-american',
    'eastern-european-russian',
    'german',
    'italian-american',
    'korean',
    'middle-eastern',
    'south-american',
    'southern',
    'tex-mex',
    'vietnamese',
    'mexican', 
    'asian',
    'american',  
    'californian',
    'chinese',
    'english',
    'greek',
    'japanese',
    'latin-american',
    'nuevo-latino',
    'south-asian',
    'southwestern',
    'thai',
    'moroccan',
    'indian',
    'british',
    'central-american-caribbean',
    'cuban',
    'european',
    'irish',
    'jewish',
    'mediterranean',
    'southeast-asian',
    'spanish-portuguese',
    'turkish',
]

cuisine_urls = {}

base_url = 'https://www.epicurious.com/search?content=recipe'

for cuisine in cuisines:
    sleep(0.05)

    cuisine_urls[cuisine] = []
    cuisine_url = base_url + '&cuisine={}'.format(cuisine)

    page = requests.get(cuisine_url).content
    soup = BeautifulSoup(page, features="html.parser")
    num_pages = get_number_of_pages(soup)

    cuisine_urls[cuisine] += extract_urls(soup)

    page_count = 2
    
    while page_count <= num_pages:
        sleep(0.05)
        current_url = cuisine_url + '&page={}'.format(page_count)

        page = requests.get(current_url).content
        soup = BeautifulSoup(page, features="html.parser")

        cuisine_urls[cuisine] += extract_urls(soup)

        page_count += 1


with open('cuisine-recipes.json', 'w+') as f:
    json.dump(cuisine_urls, f)







