from category.models import Category
from topic.models import Topic
from news.models import News

from django.db import transaction

from bs4 import BeautifulSoup

import urllib
import json
import urllib.request
import re
import konlpy
import nltk
import tensorflow as tf
import numpy as np
import environ

tf.random.set_seed(777)
env = environ.Env(
    DEBUG=(bool, False)
)


# ** 각 함수 생성 **
# 카테고리 가져오기
def get_category():
    category_list = Category.objects.values_list('name', flat=True)
    return category_list


def search_news(category):
    client_id = env('API_ID')
    client_secret = env('API_SECRET')

    word = urllib.parse.quote(category)
    url = "https://openapi.naver.com/v1/search/news.json?sort=date&display=1&query=" + word
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    code = response.getcode()
    if code == 200:
        response_body = response.read()
        decode_body = response_body.decode('utf-8')
        json_body = json.loads(decode_body)
        items = json_body['items'][0]
        return items
    else:
        print("Error Code:" + code)
        return


# 뉴스 1개씩 검색
# 카테고리 사용하여 검색 상단 뉴스를 가져온다 (쿼리로 해결)
def get_category_info():
    category_list = get_category()
    url_links = []
    descriptions = []
    for category in category_list:
        items = search_news(category)
        url_links.append(items['link'])
        descriptions = items['description']

    return url_links, descriptions


def make_readable_documents(documents):
    for i, document in enumerate(documents):
        document = BeautifulSoup(document, 'html.parser').text
        documents[i] = document

    for i, document in enumerate(documents):
        document = re.sub(r'[^ ㄱ-ㅣ가-힣]', '', document)
        documents[i] = document

    for i, document in enumerate(documents):
        open_korean_text = konlpy.tag.Okt()
        clean_words = []
        for word in open_korean_text.pos(document, stem=True):
            if word[1] in ['Noun', 'Verb', 'Adjective']:
                clean_words.append(word[0])
        document = ' '.join(clean_words)
        documents[i] = document

    return documents


def words_filter():
    link = 'https://raw.githubusercontent.com/cranberryai/todak_todak_python/master/machine_learning_text/clean_korean_documents/korean_stopwords.txt'
    data = urllib.request.urlopen(link)
    words = []
    for word in data:
        words.append(word.decode('utf-8'))
    words = np.array(words)
    return words


def clean_korean_documents(documents):
    nltk.download('punkt')
    for i, document in enumerate(make_readable_documents(documents)):
        clean_words = []
        for word in nltk.tokenize.word_tokenize(document):
            if word not in words_filter():
                clean_words.append(word)
        documents[i] = ' '.join(clean_words)
    return documents


def get_embedding_topic(word_index, embedding_description_list):
    embedding_value = -1
    result_topic = ''
    for i in embedding_description_list:
        for key, value in word_index.items():
            if value == i:
                if value > embedding_value:
                    result_topic = key
                    embedding_value = value
    return embedding_value, result_topic


# 뉴스에서 토픽을 추출한다.
def extract_topic():
    extract_list = []
    labels = env('CATEGORY_LABEL')
    tokenizer = tf.keras.preprocessing.text.Tokenizer()
    model = tf.keras.models.load_model('utils/model.h5')
    urls, descriptions = get_category_info()
    for url, des in zip(urls, descriptions):
        description = np.array([des])
        clean_description = clean_korean_documents(description)
        embedding_description = tokenizer.texts_to_sequences(clean_description)

        embedding_value, result_topic = get_embedding_topic(tokenizer.word_index, sum(embedding_description, []))

        padding_words = tf.keras.preprocessing.sequence.pad_sequences([[embedding_value]], maxlen=300)
        predict = model.predict(padding_words)

        result_label = labels[predict[0].argmax()]
        extract_list.append({'category': result_label, 'topic': result_topic, 'link': url, 'des': des})

    return extract_list


# 토픽에 해당하는 뉴스를 db에 삽입
@transaction.atomic
def insert_db():

    extract_list = extract_topic()
    news_list = []
    topic_list = []
    for li in extract_list:
        topic = Topic.objects.filter(category=li['category'], name=li['topic'])
        if not topic:
            topic_list.append(Topic(category=li['category'], name=li['topic']))
        news_list.append(News(topic1=li['topic'], topic2=li['topic'], topic3=li['topic'], link=li['url']))

    Topic.objects.bulk_create(topic_list)
    News.objects.bulk_create(news_list)

    print('end')
