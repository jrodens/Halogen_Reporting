from nltk import ngrams
from collections import Counter

result = []
sentence = open(r"O:/desc.txt","r")
# Since you are not considering periods and treats words with - as phrases
sentence = sentence.replace('.', '').replace('-', ' ')

for n in range(len(sentence.split(' ')), 1, -1):
    phrases = []

    for token in ngrams(sentence.split(), n):
        phrases.append(' '.join(token))

    phrase, freq = Counter(phrases).most_common(1)[0]
    if freq > 1:
        result.append((phrase, n))
        sentence = sentence.replace(phrase, '')

for phrase, freq in result:
    print('%s: %d' % (phrase, freq))
