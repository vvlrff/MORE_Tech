from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

@app.route('/api/digest')
def digest():
    headers = {
        'Accept': '*/*',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.114 YaBrowser/22.9.1.1079 Yowser/2.5 Safari/537.36'
    }
    hrefs, bigData = [],[]
    for id in range(10):
        url = 'https://www.rbc.ru/v10/ajax/get-news-by-filters/?category=business&offset=' + str(id) + '&limit=12'
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        postHref = soup.find("a").get("href")
        hrefs.append(postHref)

    for href in hrefs:
        data =[]
        url = href[2:-2]
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')  
        title = soup.find(class_="article__header__title-in js-slide-title")
        title_text = title.text
        data = {
            "url": url,
            "title": title_text
        }
        bigData.append(data)
    return jsonify(bigData)


if __name__ == '__main__':
    app.run(port=8000, debug=True)