from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from bs4 import BeautifulSoup
import pandas as pd
import re

class Utils:
    def scrape_lyrics_to_dataframe(self,links):

        driver = webdriver.Chrome()
        all_data = []

        for url in links:
            try:
                driver.get(url)
                time.sleep(3)  # Espera por si la página tarda en cargar

                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                # Obtener nombre de la canción
                song_tag = soup.find('h1', class_='textStyle-primary')
                song_name = song_tag.text.strip() if song_tag else 'No encontrado'

                # Obtener nombre del autor
                author_tag = soup.find('h2', class_='textStyle-secondary')
                author_name = author_tag.text.strip() if author_tag else 'No encontrado'

                # Obtener las estrofas únicas
                lyric_container = soup.find('div', class_='lyric-original')
                estrofas_unicas = []
                if lyric_container:
                    p_tags = lyric_container.find_all('p')
                    for p in p_tags:
                        texto = p.get_text(separator="\n").strip()
                        if texto not in estrofas_unicas:
                            estrofas_unicas.append(texto)

                # Crear diccionario de la fila
                song_data = {
                    'song_name': song_name,
                    'author_name': author_name
                }

                for i, estrofa in enumerate(estrofas_unicas, 1):
                    song_data[f'estrofa{i}'] = estrofa

                all_data.append(song_data)

                print(f'Scrapeado: {song_name} - {author_name}')

            except Exception as e:
                print(f'Error con URL: {url} | Error: {e}')

        driver.quit()

        # Crear DataFrame final
        df = pd.DataFrame(all_data)
        return df


        
