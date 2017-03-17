from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# create sample documents
doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
doc_e = "Health professionals say that brocolli is good for your health."

rev1 = "I pre-ordered this for my wife mostly to use as a Kindle E-reader as I figured the tablet would be slow and the display would be less than impressive. I was wrong. What a bargain this little beauty is! This model cost $49.00 but it comes with ad's displayed on the lock screen when your tablet is dormant. Once your screen times out, they disappear. You can pay $15.00 up front to get an ad free version so I assumed to unlock the tablet I'd have to spend 15 to 30 seconds looking at an ad for Amazon Prime, or a product from the daily specials section of Amazon.com I abstained from paying for Ad removal and was pleasantly surprised to find that the ads are only on the lock screen and that as soon as I unlock the tablet they disappear immediately. Here are my pros and cons thus far. PRO: Perfect size for Ebooks, and web surfing to alleviate strain on the eyes from my 5 phone display nice sturdy casing that gives it a nice heft but still weighs in as one of the lighter tablets on the market Child Accounts- Amazon allows you to set up this tablet with age restricted access for kids making this a low cost piece of tech that is perfect for school kids and allows mom and dad to ration the amount of time lil Johnny can play Clash of Clans and how much he can hit the ol' Visa card for. Battery life thus far; wife was on it for about 5 hours last night and battery was at about 46% Kindle Integration -this goes without saying but having my ebooks and audible books synced to the tablet is awesome and my Kindle books look great"
rev2 = "UPDATED - After spending quite a bit more time with the device, I would give it a 4.5 due to a few specific gaps that are a bit annoying. However, you are still getting an amazing 7” tablet, with front and rear facing cameras, a gorgeous interface, fairly snappy performance and durability, all for under 50 bucks! I can’t imagine not buying these for myself and my whole family, but not a primary tablet for a techie adult by any means. For background, I have every Kindle, a couple Fires, and multiple tablets from Apple, Microsoft and Samsung. Note that my review with 5 stars considers the value equation, not just performance and how that may or may not compare to other tablets - if you are expecting this to compare to a tablet costing several times more, don't bother. But if you are looking for a great entry level tablet that does most of the things people want, this little tablet definitely delivers the value! PRICING/CONFIG: I prefer this tablet with ads and no accessories to keep the costs down. You have the option to spend more money, but I recommend against it. You can easily see the specs online, so I won’t do you the discourtesy of simply cutting and pasting those here. Here is the price breakdown: 9.99 base price – what an incredible price point! Or buy 5 and get a sixth one free! This puts it into reach of schools and non-profits."
rev3 ="The short/summed up version: it's the new budget king in the 6-8 size. It's screen is a little lower in resolution but still pleasant to look at, it has enough power for most of the typical tablet tasks, and it shares many of the same features as its higher priced brothers such as front and back cameras, b/g/n wifi, and good overall battery life (minus an hour) My favorite size tablet is 8, so if you're looking at the amazon fire lineup, i would take this over the 6 for sure, and would have a hard time picking the 8 fire at 3x the price. If you re not a prime member, it s still a good tablet, if you are a prime member: it s a great tablet. Possible quality control issue: Mine had two dead pixels (not very noticeable, but still will exchange) You can load APKs(enable unknown sources), i loaded antutu and panasonic image app, both work properly."

# compile sample documents into a list
#doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]
doc_set = [rev1,rev2,rev3]
# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:
    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]

    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

    # add tokens to list
    texts.append(stemmed_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=4, id2word=dictionary, passes=20)
print("LDA............")
topics = ldamodel.print_topics(num_topics=3, num_words=5)
for topic in topics:
    print(type(topic))
    print(topic)

print("LSA.................")
#id2word = gensim.corpora.Dictionary.load_from_text("c:\lda_test.txt")
lsi = gensim.models.lsimodel.LsiModel(corpus, id2word=dictionary)

from nltk.corpus import sentiwordnet as swn

topics = lsi.print_topics(5)
for topic in topics:
    print(topic[1])
    print(swn.senti_synsets(topic[1]))
    print("----------------------------------------")



#print(list(swn.senti_synsets('slow')))

happy = swn.senti_synsets('happy')

print(happy.neg_score())

all = swn.all_senti_synsets()
#print(all)