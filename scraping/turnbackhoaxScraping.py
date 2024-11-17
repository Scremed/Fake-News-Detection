import pandas as pd
from os import path
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Fungsi untuk melakukan web scraping
def scrap(url):
    page = urlopen(url)
    return BeautifulSoup(page, 'lxml');

def get_dataset(web):
    judul = [h3.find('a') for h3 in web.find_all('h3')]
    hrefs = [h3.get('href') for h3 in judul]
    label = [judul.text.split(']',1)[0] for judul in judul]
    judul = [x.text for x in judul]
    judul = [judul.replace(label+"] ",'') for label,judul in zip(label,judul)]
    tanggal = [x.text for x in web.find_all('span', class_="mh-meta-date updated")]
    isi_berita = [x.find('p') for x in web.find_all('div', class_="mh-excerpt")]
    isi_berita = [x.text for x in isi_berita]

    for i in range(len(judul)):
        if hrefs[i] not in hrefs_recent:
            result.append([judul[i], isi_berita[i], tanggal[i], hrefs[i]])


# Mengecek jika sudah terdapat dataset sebelumnya
if path.isfile('dataset/dataset-turnbackhoax.csv'):
    df_recent = pd.read_csv('dataset/dataset-turnbackhoax.csv')
    hrefs_recent = df_recent['link'].sort_values(ascending=False).tolist()
else:
    df_recent = pd.DataFrame([],columns=['judul','isi','tanggal','link'])
    hrefs_recent = []

result = []
url = "https://turnbackhoax.id/page/"
first_page = 1 # page pertama
last_page = 153 # menyesuaikan jumlah dataset fakta

for page in range(first_page, last_page + 1):
    web = scrap(url + str(page))
    get_dataset(web)
    
    print(f'page {page} done')


df = pd.DataFrame(result, columns=['judul','isi','tanggal', 'link'])
print(f'new data shape: {df.shape}')

df = pd.concat([df, df_recent])
print(f'dataset shape: {df.shape}')

df.sort_values(['link'], ascending = False).to_csv('dataset/dataset-turnbackhoax.csv', index=False)

