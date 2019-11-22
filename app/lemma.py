from nltk import sent_tokenize, word_tokenize
import pymorphy2
from nltk.corpus import wordnet, stopwords
import nltk
import re

def _create_frequency_matrix(sentences):
    frequency_matrix = {}
    stopWords = set(stopwords.words("russian"))

    morph = pymorphy2.MorphAnalyzer()
    
    pattern = r"[^\w]"

    for sent in sentences:
        freq_table = {}
        words_without_sign = re.sub(pattern, " ", sent)
        words = word_tokenize(words_without_sign)       
        
        for word in words:
            word = word.lower()
            morph_analyze = morph.parse(word)
            word = morph_analyze[0].normal_form
            
            if word in stopWords:
                continue
                
            if len(word) < 2:
                continue

            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

        frequency_matrix[sent[:15]] = freq_table
    
    #print(frequency_matrix)
    
    return frequency_matrix

def _create_documents_per_words(freq_matrix):
    word_per_doc_table = {}

    for sent, f_table in freq_matrix.items():
        for word, count in f_table.items():
            if word in word_per_doc_table:
                word_per_doc_table[word] += 1
            else:
                word_per_doc_table[word] = 1
    #print(word_per_doc_table)
    words_count_cores = len(word_per_doc_table)
    print('Слова в ядре: ' + str(words_count_cores))
    return word_per_doc_table, words_count_cores

def text_length(text):
    pattern ='[ \n\r]'
    
    return len(re.sub(pattern, "", text))

#nltk.download('wordnet')
#nltk.download('punkt')
#nltk.download('stopwords')
def get_lemma_dict(text):
    sentences = nltk.sent_tokenize(text)

    words_count_text = len(text.split(' '))
    print('Общее количество слов:' + str(words_count_text))
    freq_matrix = _create_frequency_matrix(sentences)

    tf = _create_documents_per_words(freq_matrix)[0]
    words_count_cores = _create_documents_per_words(freq_matrix)[1]

    tf_sorted = sorted(tf.items(), key=lambda kv: kv[1], reverse=True)

    return tf_sorted, words_count_text, words_count_cores

#text = 'Что такое NLP? Это широкий круг задач по обработке текстов на естественном языке (т. е. на языке, на котором говорят и пишут люди). Существует набор классических задач NLP, решение которых несет практическую пользу. Первая и самая исторически важная задача – это машинный перевод. Ей занимаются очень давно, и есть огромный прогресс. Но задача получения полностью автоматического перевода высокого качества (FAHQMT) так и остается нерешенной. Это в каком-то смысле мотор NLP, одна из самых больших задач, которой можно заниматься. Вторая задача — классификация текстов. Дан набор текстов, и задача – классифицировать эти тексты по категориям. Каким? Это вопрос к корпусу. Первый и один из самых важных с практической точки зрения способов применения — классификация писем на спам и хам (не спам). Другой классический вариант — многоклассовая классификация новостей по категориям (рубрикация) — внешняя политика, спорт, шапито и т. п. Или, допустим, вам приходят письма, и вы хотите отделить заказы из интернет-магазина от авиабилетов и броней отелей. Третий классический вариант применения задачи текстовой классификации — сентиментный анализ. Например, классификация отзывов на положительные, отрицательные и нейтральные. Поскольку возможных категорий, на которые можно делить тексты, можно придумать очень много, текстовая классификация является одной из самых популярных практических задач NLP. Третья задача – извлечение именованных сущностей, NER. Мы выделяем в тексте участки, которые соответствуют заранее выбранному набору сущностей, например, надо найти в тексте все локации, персоны и организации. В тексте «Остап Бендер — директор конторы “Рога и Копыта”» вы должны понять, что Остап Бендер – это персона, а “Рога и Копыта”– это организация. Зачем эта задача нужна на практике и как ее решать, мы поговорим во второй части нашей статьи.'
#print(get_lemma_dict(text))