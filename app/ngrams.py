import collections
import re
import sys
import time
import pymorphy2
from nltk.corpus import stopwords

def tokenize(string):
    """Convert string to lowercase and split into words (ignoring
    punctuation), returning list of words.
    """
    return re.findall(r'\w+', string.lower())


def count_ngrams(lines, min_length=2, max_length=4):
    """Iterate through given lines iterator (file object or list of
    lines) and return n-gram frequencies. The return value is a dict
    mapping the length of the n-gram to a collections.Counter
    object of n-gram tuple and number of times that n-gram occurred.
    Returned dict includes n-grams of length min_length to max_length.
    """
    lengths = range(min_length, max_length + 1)
    ngrams = {length: collections.Counter() for length in lengths}
    queue = collections.deque(maxlen=max_length)

    # Helper function to add n-grams at start of current queue to dict
    def add_queue():
        current = tuple(queue)
        for length in lengths:
            if len(current) >= length:
                ngrams[length][current[:length]] += 1

    # Loop through all lines and words and add n-grams to dict
    for line in lines:
        for word in tokenize(line):
            queue.append(word)
            if len(queue) >= max_length:
                add_queue()

    # Make sure we get the n-grams at the tail end of the queue
    while len(queue) > min_length:
        queue.popleft()
        add_queue()

    return ngrams


def print_most_frequent(ngrams, num=10):
    """Print num most common n-grams of each length in n-grams dict."""
    for n in sorted(ngrams):
        print('----- {} most common {}-grams -----'.format(num, n))
        for gram, count in ngrams[n].most_common(num):
            print('{0}: {1}'.format(' '.join(gram), count))
        print('')


def get_ngrams_dict(text, num):
    token = tokenize(text)

    stop_words = set(stopwords.words("russian"))
    stop_words.add('т.е.')
    #stop_words

    morph = pymorphy2.MorphAnalyzer()

    res = [morph.parse(word)[0].normal_form for word in token]    
    #print(res)

    without_stop_words = [word for word in res if (not word in stop_words) and (len(word) > 1)]
    #print(without_stop_words)
   

    ngrams = count_ngrams(without_stop_words)
    #print(ngrams)

    res2 = dict(ngrams[num])
    #print(res2)

    ngram_sorted = sorted(res2.items(), key=lambda kv: kv[1], reverse=True)
    print(ngram_sorted)

    return ngram_sorted

#Ввод текста
text = 'Что такое NLP? Это широкий круг задач по обработке текстов на естественном языке (т. е. на языке, на котором говорят и пишут люди). Существует набор классических задач NLP, решение которых несет практическую пользу. Первая и самая исторически важная задача – это машинный перевод. Ей занимаются очень давно, и есть огромный прогресс. Но задача получения полностью автоматического перевода высокого качества (FAHQMT) так и остается нерешенной. Это в каком-то смысле мотор NLP, одна из самых больших задач, которой можно заниматься. Вторая задача — классификация текстов. Дан набор текстов, и задача – классифицировать эти тексты по категориям. Каким? Это вопрос к корпусу. Первый и один из самых важных с практической точки зрения способов применения — классификация писем на спам и хам (не спам). Другой классический вариант — многоклассовая классификация новостей по категориям (рубрикация) — внешняя политика, спорт, шапито и т. п. Или, допустим, вам приходят письма, и вы хотите отделить заказы из интернет-магазина от авиабилетов и броней отелей. Третий классический вариант применения задачи текстовой классификации — сентиментный анализ. Например, классификация отзывов на положительные, отрицательные и нейтральные. Поскольку возможных категорий, на которые можно делить тексты, можно придумать очень много, текстовая классификация является одной из самых популярных практических задач NLP. Третья задача – извлечение именованных сущностей, NER. Мы выделяем в тексте участки, которые соответствуют заранее выбранному набору сущностей, например, надо найти в тексте все локации, персоны и организации. В тексте «Остап Бендер — директор конторы “Рога и Копыта”» вы должны понять, что Остап Бендер – это персона, а “Рога и Копыта”– это организация. Зачем эта задача нужна на практике и как ее решать, мы поговорим во второй части нашей статьи.'
get_ngrams_dict(text, 4)