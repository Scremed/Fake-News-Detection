import pandas as pd
from os import path
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Fungsi untuk melakukan web scraping
def scrap(url):
    page = urlopen(url)
    return BeautifulSoup(page, 'lxml');

def get_dataset(web):
    judul = [x for x in web.find_all('h2', class_="h5")]
    hrefs = [x.find('a') for x in judul]
    judul = [x.text for x in judul]
    hrefs = [x.get('href') for x in hrefs]
    tanggal = [x.text for x in web.find_all('span', class_="text-dark text-capitalize")]
    isi_berita = [x.text for x in web.find_all('p')]

    for i in range(len(judul)):
        if hrefs[i] not in hrefs_recent:
            result.append([judul[i], isi_berita[i], tanggal[i], hrefs[i]])

# Mengecek jika sudah terdapat dataset sebelumnya
if path.isfile('dataset/dataset-antaranews.csv'):
    df_recent = pd.read_csv('dataset-antaranews.csv')
    hrefs_recent = df_recent['link'].sort_values(ascending=False).tolist()
else:
    df_recent = pd.DataFrame([],columns=['tanggal','judul','isi', 'link'])
    hrefs_recent = []

result = []
url = "https://antaranews.com/tag/verifikasi-faktual/"
first_page = 1 # page pertama
last_page = 60 # page terakhir

for page in range(first_page, last_page + 1):
    web = scrap(url + str(page))
    get_dataset(web)
    
    print(f'page {page} done')


df = pd.DataFrame(result, columns=['judul','isi','tanggal', 'link'])
print(f'new data shape: {df.shape}')

df = pd.concat([df, df_recent])
print(f'dataset shape: {df.shape}')

df.sort_values(['link'], ascending = False).to_csv('dataset/dataset-antaranews.csv', index=False)

