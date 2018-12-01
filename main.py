import collections

import re

import time

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
s_t = 0


def create_db():
    """
    .txt dosyasinda bulunan bilgileri indexleyerek veri tabani olusturur
    """

    # dosyada bulunan her satir icin
    for line in f:

        # satir basinda ve sonunda bulunan bosluklari, yeni satir karakterlerini temizler
        line = line.strip()

        # - sembolunun solunda bulunan url degerlerini alir
        url = line.split('-')[0].strip()

        # - sembolunun saginda bulunan kelimeleri virgule gore ayirarak diziye ekler
        words = line.split('-')[-1].split(',')

        # - kelimelerin basinda ve sonunda bulunan bosluklari atar
        words = [w.strip() for w in words]

        # her kelime icin bulundugu indis agirlik olarak atanir
        # 0 - en buyuk agirliktir
        for i, w in enumerate(words):
            if my_db.get(w) is None:
                my_db[w] = {}

            my_db[w][url] = i

            # print(my_db)


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
    global s_t

    user_input = input("Please enter sentence: ").strip()
    s_t = time.time()
    user_input = clear(user_input)

    return user_input


def get_serch_results(user_input):
    """
    Kullanici girdisine gore sonuc doner
    :param user_input: temizlenmis kullanici girdisi
    :return: sirali arama sonucu
    """

    found = {}

    # veri tabaninda bulunan her kelime icin
    for user_w in user_input.split():
        if my_db.get(user_w):
            for k, v in my_db[user_w].items():
                if found.get(k) is None:
                    found[k] = v

    sorted_results = sorted(found.items(), key=lambda kv: kv[1])
    # print(results)
    return sorted_results


if __name__ == "__main__":
    create_db()

    while True:

        user_input = get_user_input()
        results = get_serch_results(user_input)
        work_time = (time.time() - s_t)

        if len(results) == 0:
            print("\nSorry, we couldn't find anything :(")

        else:
            print("\n{} results found in {} secs.".format(len(results), work_time))
            for k, v in results:
                print(k)
            print()
