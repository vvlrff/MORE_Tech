from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import pickle
import string
import nltk
import pymorphy2
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')
stop_words = stopwords.words('russian')
stop_words.extend(['который', 'https', 'также', 'другой', 'которые', 'которым', 'которых', 'которая', 'которому', 'каждый'])
morph = pymorphy2.MorphAnalyzer()
spec_chars = string.punctuation + '\n\xa0«»\t—…'

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

@app.route('/api/digest/director')
def digest_dir():
    headers = {
        'Accept':
        '*/*',
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.114 YaBrowser/22.9.1.1079 Yowser/2.5 Safari/537.36'
    }
    hrefs, bigData = [], []
    for id in range(10):
        url = 'https://www.rbc.ru/v10/ajax/get-news-by-filters/?category=business&offset=' + str(
            id) + '&limit=12'
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        postHref = soup.find("a").get("href")
        hrefs.append(postHref)

    for id in range(10):
        url = 'https://www.rbc.ru/v10/ajax/get-news-by-filters/?category=economics&offset=' + str(
            id) + '&limit=12'
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        postHref = soup.find("a").get("href")
        hrefs.append(postHref)


    for href in hrefs:
        data = []
        url = href[2:-2]
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        title = soup.find(class_="article__header__title-in js-slide-title")
        title_text = title.text
        data = {"URL": url, "TITLE": title_text}
        bigData.append(data)

    data_digest = pd.DataFrame(bigData)

    upper_lettres = 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    spec_chars = string.punctuation + '\n\xa0«»\t—…'

    def clean_data_digest(dataset):
        for index in range(dataset.shape[0]):
            text = dataset.TITLE[index]
            if type(text) != float:
                text = "".join([ch for ch in text if ch not in spec_chars])
                text = re.sub('\n', '', text)
                text = text.strip()
                dataset.TITLE[index] = text

    clean_data_digest(data_digest)

    def digest_distribution(dataset):
        list_of_upper_letters = []
        for index in range(dataset.shape[0]):
            number_of_upper_latters = 0
            text = dataset.TITLE[index]
            for ch in text:
                if ch in upper_lettres:
                    number_of_upper_latters += 1
            list_of_upper_letters.append(number_of_upper_latters)
        mean_upper_letters = sum(list_of_upper_letters) / len(list_of_upper_letters)
        digest_for_director = []
        director_links = []
        digest_for_accountant = []
        accountant_links = []
        for index in range(len(list_of_upper_letters)):
            if list_of_upper_letters[index]  > mean_upper_letters:
                digest_for_director.append(dataset.TITLE[index])
                director_links.append(dataset.URL[index])
            else:
                digest_for_accountant.append(dataset.TITLE[index])
                accountant_links.append(dataset.URL[index])
        return digest_for_director, director_links, digest_for_accountant, accountant_links

    digest_for_director, director_links, digest_for_accountant, accountant_links = digest_distribution(data_digest)

    items = []
    for index in range(len(digest_for_director)):
        items.append(
            {
                    "id": index,
                    "fact_for_digest": digest_for_director[index],
                    "url": director_links[index]
            }
        )
    return jsonify(items)

@app.route('/api/digest/accountant')
def digest_accountant():
    headers = {
        'Accept':
        '*/*',
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.114 YaBrowser/22.9.1.1079 Yowser/2.5 Safari/537.36'
    }
    hrefs, bigData = [], []
    for id in range(10):
        url = 'https://www.rbc.ru/v10/ajax/get-news-by-filters/?category=business&offset=' + str(
            id) + '&limit=12'
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        postHref = soup.find("a").get("href")
        hrefs.append(postHref)

    for id in range(10):
        url = 'https://www.rbc.ru/v10/ajax/get-news-by-filters/?category=economics&offset=' + str(
            id) + '&limit=12'
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        postHref = soup.find("a").get("href")
        hrefs.append(postHref)


    for href in hrefs:
        data = []
        url = href[2:-2]
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        title = soup.find(class_="article__header__title-in js-slide-title")
        title_text = title.text
        data = {"URL": url, "TITLE": title_text}
        bigData.append(data)

    data_digest = pd.DataFrame(bigData)
    
    upper_lettres = 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    spec_chars = string.punctuation + '\n\xa0«»\t—…'

    def clean_data_digest(dataset):
        for index in range(dataset.shape[0]):
            text = dataset.TITLE[index]
            if type(text) != float:
                text = "".join([ch for ch in text if ch not in spec_chars])
                text = re.sub('\n', '', text)
                text = text.strip()
                dataset.TITLE[index] = text

    clean_data_digest(data_digest)

    def digest_distribution(dataset):
        list_of_upper_letters = []
        for index in range(dataset.shape[0]):
            number_of_upper_latters = 0
            text = dataset.TITLE[index]
            for ch in text:
                if ch in upper_lettres:
                    number_of_upper_latters += 1
            list_of_upper_letters.append(number_of_upper_latters)
        mean_upper_letters = sum(list_of_upper_letters) / len(list_of_upper_letters)
        digest_for_director = []
        director_links = []
        digest_for_accountant = []
        accountant_links = []
        for index in range(len(list_of_upper_letters)):
            if list_of_upper_letters[index]  > mean_upper_letters:
                digest_for_director.append(dataset.TITLE[index])
                director_links.append(dataset.URL[index])
            else:
                digest_for_accountant.append(dataset.TITLE[index])
                accountant_links.append(dataset.URL[index])
        return digest_for_director, director_links, digest_for_accountant, accountant_links

    digest_for_director, director_links, digest_for_accountant, accountant_links = digest_distribution(data_digest)

    items = []
    for index in range(len(digest_for_accountant)):
        items.append(
            {
                    "id": index,
                    "fact_for_digest": digest_for_accountant[index],
                    "url": accountant_links[index]
            }
        )
    return jsonify(items)


@app.route('/api/trendsandinside')
def trends():
    total_last_week = pd.read_csv("/Users/vvlrff/Desktop/my_projects/MORE_Tech/api/total_last_week.csv", sep = '\t', error_bad_lines=False)
    with open('/Users/vvlrff/Desktop/my_projects/MORE_Tech/api/frequency_dict_half_of_the_year.pkl', 'rb') as f:
        frequency_dict_half_of_the_year = pickle.load(f)

    with open('/Users/vvlrff/Desktop/my_projects/MORE_Tech/api/frequency_dict_last_week.pkl', 'rb') as f:
        frequency_dict_last_week = pickle.load(f)

    general_dict = dict()
    for key, value in frequency_dict_last_week.items():
        if key in frequency_dict_half_of_the_year:
            general_dict[key] = value / frequency_dict_half_of_the_year[key]
    sorted_general_dict = sorted(general_dict.items(), key=lambda x: x[1], reverse = True)[:3]

    final_search = []
    for elem in sorted_general_dict:
        final_search.append(elem[0])

    def find_and_return_article():
        trend_result = []
        for trend_word in final_search:
            trend_word_dictionary = dict()
            for counter in range(total_last_week.shape[0]):
                text = total_last_week.MESSAGE[counter]
                if type(text) != float:
                    tokens = nltk.word_tokenize(text)   
                    filtered_text = [word.lower() for word in tokens if word.lower() not in stop_words] 
                    final_text = []
                    for word in filtered_text:
                        if word.isalpha() and len(word) > 4:
                            p = morph.parse(word)[0]
                            final_text.append(p.normal_form)
                        else:
                            continue
                    if trend_word in final_text:
                        trend_word_dictionary[counter] = final_text.count(trend_word)
            trend_result.append(sorted(trend_word_dictionary.items(), key=lambda x: x[1], reverse = True)[0])
        return trend_result
    
    trend_result = find_and_return_article()

    general_trend_collection = []
    for trend_index in trend_result:
        text = re.sub(' - РИА Новости', '', total_last_week.MESSAGE[trend_index[0]])
        text = re.sub(' – РИА Новости', '', text)
        general_trend_collection.append(text)

    items = []
    for index in range(len(general_trend_collection)):
        items.append(
            {
                "id": index,
                "text_of_the_article": general_trend_collection[index]
            }
        )
    return jsonify(items)


if __name__ == '__main__':
    app.run(port=8000, debug=True)