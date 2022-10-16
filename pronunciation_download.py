from bs4 import BeautifulSoup
from playsound import playsound
import requests
import argparse
import urllib.request
import webbrowser


parser = argparse.ArgumentParser(description='Download pronunciation of an English word.')
parser.add_argument('word', type=str, help='an English word')
parser.add_argument('--web', dest='web', action='store_true', help='to open the webpage on the browser')
parser.set_defaults(web=False)
args = parser.parse_args()

# set some headers
agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
headers = requests.utils.default_headers()
headers.update({'User-Agent': agent})
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', agent)]
urllib.request.install_opener(opener)


def get_soup(url):
  r  = requests.get(url, headers=headers)
  data = r.text
  return BeautifulSoup(data, features="html.parser")


def get_near_urls(primary_soup, word):
  result_links = list()
  near_list = primary_soup.select_one('div#relatedentries')

  if near_list is not None:
    for item in near_list.select('li'):
      new_word = item.select_one('span').find(text=True).strip()
      if new_word == word:
        link = item.select_one('a').get('href')
        result_links.append(link)
  return result_links


def download_single(soup):
  headword = soup.select_one('h1.headword').text
  position = soup.select_one('span.pos')
  if position is not None: position = position.text
  pronounce_div = soup.select_one('div.phons_n_am')
  phonetics = pronounce_div.select_one('span').text
  link =  pronounce_div.select_one('div.sound.pron-us').get('data-src-mp3')
  return headword, position, phonetics, link


word = args.word.lower().strip().replace(' ', '-')
primary_url  = 'https://www.oxfordlearnersdictionaries.com/definition/english/' + word
if args.web: webbrowser.open(primary_url, new=2)

primary_soup = get_soup(primary_url)

soup_list = [primary_soup]
for other_url in get_near_urls(primary_soup, word):
  soup_list.append(get_soup(other_url))

all_results = [download_single(soup) for soup in soup_list]
all_results = [res for res in all_results if res[0] == word]
unique_phonetics = set([res[2] for res in all_results])

for phonetic in unique_phonetics:
  matching_results = [res for res in all_results if res[2] == phonetic]
  position_list = [res[1] for res in matching_results if res[1] is not None]

  headword, _, phon, link = matching_results[0]
  pos = ' (' + '|'.join(position_list) + ')' if len(position_list) > 0 else ''
  mp3_file_name = '{}{}.mp3'.format(headword, pos)
  urllib.request.urlretrieve(link, mp3_file_name)
  print(word, pos, phon)
  playsound(mp3_file_name)
