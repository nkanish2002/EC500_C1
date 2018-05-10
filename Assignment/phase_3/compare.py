from pytrends.request import TrendReq
import matplotlib.pyplot as plt
from wordcloud import WordCloud  # https://github.com/amueller/word_cloud
import unicodedata


def plot_wordcloud(name, wordlist):
    # Creates Wordcloud
    text = ' '.join([w.replace(' ', '') for w in wordlist])
    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(name + '.png')


def showcompare(name, list):
    # Compares trends
    pytrends = TrendReq(hl='en-US')
    word = unicodedata.normalize('NFKD', next(
        iter(list))).encode('ascii', 'ignore')
    pytrends.build_payload(
        kw_list=[word], timeframe='today 1-m', geo='US', gprop='news')
    related_topics_df = pytrends.related_topics()[word]
    plot_wordcloud(name + "Google", related_topics_df['title'].tolist())
    plot_wordcloud(name, list)
