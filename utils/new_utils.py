from category.models import Category
from topic.models import Topic
from news.models import News

from django.db import transaction

from bs4 import BeautifulSoup

import json
import urllib.request
import re
import konlpy
import pandas as pd
import nltk
import tensorflow as tf
import numpy as np
import os

tf.random.set_seed(777)


# ** 각 함수 생성 **
# 카테고리 가져오기
def get_category():

    category_queryset = Category.objects.filter()
    categories = category_queryset.filter()

    category_list = []
    for category in categories:
        category_list.append(category['name'])

    return category_list


# 뉴스 1개씩 검색
# 카테고리 사용하여 검색 상단 뉴스를 가져온다 (쿼리로 해결)
def news_search():
    client_id = os.environ.get('API_ID')
    client_secret = os.environ.get('API_SECRET')
    category_list = get_category()
    url_links = []
    descriptions = []
    for word in category_list:
        encText = urllib.parse.quote(word)
        url = "https://openapi.naver.com/v1/search/news.json?sort=date&display=1&query=" + encText
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            decode_body = response_body.decode('utf-8')
            json_body = json.loads(decode_body)
            items = json_body['items'][0]
            url_link = items['link']
            description = items['description']
            url_links.append(url_link)
            descriptions.append(description)
        else:
            print("Error Code:" + rescode)
        return url_links, descriptions


def clean_korean_documents(documents):
    for i, document in enumerate(documents):
        document = BeautifulSoup(document, 'html.parser').text
        documents[i] = document

    for i, document in enumerate(documents):
        document = re.sub(r'[^ ㄱ-ㅣ가-힣]', '', document)
        documents[i] = document

    for i, document in enumerate(documents):
        okt = konlpy.tag.Okt()
        clean_words = []
        for word in okt.pos(document, stem=True):
            if word[1] in ['Noun', 'Verb', 'Adjective']:
                clean_words.append(word[0])
        document = ' '.join(clean_words)
        documents[i] = document

    df = pd.read_csv('https://raw.githubusercontent.com/cranberryai/todak_todak_python/master/machine_learning_text/clean_korean_documents/korean_stopwords.txt', header=None)
    df[0] = df[0].apply(lambda x: x.strip())
    stopwords = df[0].to_numpy()
    nltk.download('punkt')
    for i, document in enumerate(documents):
        clean_words = []
        for word in nltk.tokenize.word_tokenize(document):
            if word not in stopwords:
                clean_words.append(word)
        documents[i] = ' '.join(clean_words)

    return documents


# 뉴스에서 토픽을 추출한다.
def extract_topic():
    extract_list = []
    labels = ['정치', '경제', '사회', '생활/문화', '세계', '기술/IT', '연예', '스포츠']
    tokenizer = tf.keras.preprocessing.text.Tokenizer()
    model = tf.keras.models.load_model('utils/model.h5')
    urls, descriptions = news_search()
    for url, des in zip(urls, descriptions):
        x_test = np.array([des])
        x_test = clean_korean_documents(x_test)
        x_test = tokenizer.texts_to_sequences(x_test)
        word_index = tokenizer.word_index
        list_x_test = sum(x_test, [])

        max_val = -1
        max_key = ''
        for i in list_x_test:
            for key, value in word_index.items():
                if value == i:
                    print(value, key)
                    if value > max_val:
                        max_key = key
                        max_val = value

        x_test = tf.keras.preprocessing.sequence.pad_sequences([[max_val]], maxlen=300)
        y_predict = model.predict(x_test)

        label = labels[y_predict[0].argmax()]
        extract_list.append({'category': label, 'topic': max_key, 'link': url, 'des': des})

    return extract_list


# 토픽에 해당하는 뉴스를 db에 삽입
@transaction.atomic
def insert_db():
    # insert news
    # insert topic
    # 한 카테고리에서 토픽 여러개 추출하는 로직 짜는 데에 시간이 오래 걸려서 하나로 넣었습니다

    extract_list = extract_topic()
    for li in extract_list:
        topic = Topic.objects.filter(category=li['category'], name=li['topic'])
        if not topic:
            Topic.objects.create(category=li['category'], name=li['topic'])
        News.objects.create(topic1=li['topic'], topic2=li['topic'], topic3=li['topic'], link=li['url'])

    print('end')
