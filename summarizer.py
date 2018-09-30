import bs4 as bs
import heapq
import nltk
import re
import urllib.request

# User input for url of webpage
user_url = str(input('Enter the webpage that you want to summarize:  '))

# Obtaining the webpage
scraped_data = urllib.request.urlopen(user_url)
article = scraped_data.read()

# Parsing article
parsed_article = bs.BeautifulSoup(article, 'lxml')
paragraphs = parsed_article.find_all('p')

article_text = ""

for p in paragraphs:
    article_text += p.text

# Preprocessing
# Normalizing - removing square brackets
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)

# Normalizing - removing special characters and digits
formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

# Tokenizing - split article into sentences
sentence_list = nltk.sent_tokenize(article_text)

# Finding weighted frequency of occurence
stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
# Tokenizing by word to calculate frequency of word
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies:
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

# Calculating weighted frequency
max_frequency = max(word_frequencies.values())
for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/max_frequency)

# Calculating sentence score
sentence_scores = {}
for sentence in sentence_list:
    for word in nltk.word_tokenize(sentence.lower()):
        if word in word_frequencies.keys():
            if len(sentence.split(' ')) < 30:
                if sentence not in sentence_scores.keys():
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]

# Getting summary
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
summary = ' '.join(summary_sentences)

print(summary)