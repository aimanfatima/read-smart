from nltk.corpus import wordnet as wn
from textblob import TextBlob
import re

tag_rank = {
    # 0:"CD", Removing Priority temporarily
    1:"NNP",
    2:"NNPS",
    3:"NN",
    4:"NNS",
    5:"VB",
    6:"VBD",
    7:"VBG",
    8:"VBN",
    9:"VBP",
    10:"VBZ",
    11:"JJ",
    12:"JJR",
    13:"JJS",
    14:"RB",
    15:"RBR",
    16:"RBS",
    17:"FW",
    18:"CC",
    # 19:"Change it void",
    19:"CD",
    20:"DT",
    21:"EX",
    22:"IN",
    23:"LS",
    24:"MD",
    25:"PDT",
    26:"POS",
    27:"PRP",
    28:"PRP$",
    29:"SYM",
    30:"TO",
    31:"UH",
    32:"WDT",
    33:"WP",
    34:"WP$",
    35:"WRB",
    36:"RP"    
}

def get_rank(value):
    for rank, tag in tag_rank.items(): 
         if tag == value: 
             return rank 
  
    return "tag doesn't exist"


class Article:
    """Retrieves and analyzes fill in the blanks for any given paragraph"""
    def __init__(self, paragraph):
        self.summary = TextBlob(paragraph)

    def generate_trivia_sentences(self):
        sentences = self.summary.sentences

        # Remove the first sentence - it's never a good one
        # del sentences[0]

        trivia_sentences = []
        for sentence in sentences:
            trivia = self.evaluate_sentence(sentence)
            if trivia:
                trivia_sentences.append(trivia)

        return trivia_sentences

    def get_similar_words(self, word):
        # In the absence of a better method, take the first synset
        synsets = wn.synsets(word, pos='n')

        # If there aren't any synsets, return an empty list
        if len(synsets) == 0:
            return []
        else:
            synset = synsets[0]

        # Get the hypernym for this synset (again, take the first)
        hypernym = synset.hypernyms()[0]

        # Get some hyponyms from this hypernym
        hyponyms = hypernym.hyponyms()

        # Take the name of the first lemma for the first 8 hyponyms
        similar_words = []
        for hyponym in hyponyms:
            similar_word = hyponym.lemmas()[0].name().replace('_', ' ')
            
            if similar_word != word:
                similar_words.append(similar_word)

            if len(similar_words) == 8:
                break

        return similar_words

    def evaluate_sentence(self, sentence):
        if len(sentence.words) < 4:
            return None
        print("\n------------------Sentence-------------------------\n")
        print(sentence)
        print("-------------------------------------------\n")
        tag_map = {word.lower(): tag for word, tag in sentence.tags}
        sorted_tag_map = sorted(tag_map.items(), key=lambda kv:(get_rank(kv[1])))     
        # print(sorted_tag_map) 
        replace_nouns = []
        for word, tag in sorted_tag_map:
            for phrase in sentence.noun_phrases:
                # print(phrase)
                # check for '
                if word.lower() in phrase:
                    # Blank out the last two words in this phrase
                    # print(phrase)
                    [replace_nouns.append(phrase_word) for phrase_word in phrase.split()[-2:]]
                    break

            # If we couldn't find the word in any phrases,
            # replace it on its own
            if len(replace_nouns) == 0:
                replace_nouns.append(word)
            break
        
        if len(replace_nouns) == 0:
            # Return none if we found no words to replace
            return None

        trivia = {
            'answer': ' '.join(replace_nouns)
        }

        if len(replace_nouns) == 1:
            # If we're only replacing one word, use WordNet to find similar words
            # trivia['similar_words'] = self.get_similar_words(replace_nouns[0])
            trivia['similar_words'] = []
        else:
            # If we're replacing a phrase, don't bother - it's too unlikely to make sense
            # TO DO
            trivia['similar_words'] = []

        # Blank out our replace words (only the first occurrence of the word in the sentence)
        replace_phrase = ' '.join(replace_nouns)
        blanks_phrase = ('__________ ' * len(replace_nouns)).strip()

        expression = re.compile(re.escape(replace_phrase), re.IGNORECASE)
        sentence = expression.sub(blanks_phrase, str(sentence), count=1)

        trivia['question'] = sentence
        return trivia
