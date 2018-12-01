import collections

import re

stopWords = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out',
             'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into',
             'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the',
             'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were',
             'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to',
             'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have',
             'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can',
             'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself',
             'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by',
             'doing', 'it', 'how', 'further', 'was', 'here', 'than', 'll', 're', 've']

f = open('keywords.txt')

my_db = {}

from textblob import TextBlob


def create_db():
    """
    .txt dosyasinda bulunan bilgileri indexleyerek veri tabani olusturur
    """

    # dosyada bulunan her satir icin
    for line in f:

        # satir basinda ve sonunda bulunan bosluklari, yeni satir karakterlerini temizler
        line = line.strip()

        # - sembolunun solunda bulunan url degerlerini alir
        url = line.split('-')[0]

        # - sembolunun saginda bulunan kelimeleri virgule gore ayirarak diziye ekler
        words = line.split('-')[-1].split(',')

        # - kelimelerin basinda ve sonunda bulunan bosluklari atar
        words = [w.strip() for w in words]

        indexed_words = {}

        # her kelime icin bulundugu indis agirlik olarak atanir
        # 0 - en buyuk agirliktir
        for i, w in enumerate(words):
            indexed_words[w] = i

        # url key degeri, agirliklandirilmis kelimeler value`dur
        my_db[url] = indexed_words


def clear(sentence):
    # removing punctuations
    txt = re.sub("\W", ' ', sentence)

    # removing stop words
    res = ""
    for word in txt.split(" "):
        if word.lower() not in stopWords:
            res += word.lower() + " "

    return res


def get_user_input():
    """
    Kullanicidan girdi alir
    :return: punctation and stop word free user input
    """

    user_input = input("Please enter sentence: ").strip()
    clear(user_input)

    return user_input


def get_serch_results(user_input):
    """
    Kullanici girdisine gore sonuc doner
    :param user_input: temizlenmis kullanici girdisi
    :return: sirali arama sonucu
    """

    found = {}

    # veri tabaninda bulunan her kelime icin
    for url, w in my_db.items():

        for user_w in user_input.split():
            if user_w in w.keys():
                found[url] = w[user_w]

    print(found)
    od = collections.OrderedDict(sorted(found.items()))

    return od


if __name__ == "__main__":
    create_db()
    while True:
        user_input = get_user_input()
        res = get_serch_results(user_input)

        for k, v in res.items():
            print(k, v)
