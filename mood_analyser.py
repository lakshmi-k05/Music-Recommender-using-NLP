import nltk
import sys
import os
import re
import yaml
import training_mod
import play_choose
from mood_to_song import choose_song

class Wordify(object):
    #Creates list of sentence tokens
    def __init__(self):
        self.get_sentences = nltk.data.load('tokenizers/punkt/english.pickle')
        self.get_words = nltk.tokenize.TreebankWordTokenizer()

    def split_words(self, text):
        sentences = self.get_sentences.tokenize(text)
        words = [self.get_words.tokenize(sentence) for sentence in sentences]
        return words
class POStagger(object):
    #tags output from wordify
    def __init__(self):
        pass
    def tagger(self, sent_tokens):
        #nltk.pos_tag() takes a list of tokens and returns a list of words-tags tuples
        pos_all = [nltk.pos_tag(sentence) for sentence in sent_tokens]
        tagged_sent = [[(word, word, [tags]) for (word, tags) in pos_sent] for pos_sent in pos_all]
        return tagged_sent

class DictionaryTagger(object):
    #creates dictionary of mood lexicons
    def __init__(self, dictionary_Paths):
        training_mod.train_data()
        files = [open(path, 'r') for path in dictionary_Paths]
        dictionaries = [yaml.load(dictionary_file) for dictionary_file in files]
        map(lambda x: x.close(), files)
        self.dictionary = {}
        self.max_key_length = 0
        for dict in dictionaries:
            for key in dict:
                if key in self.dictionary:
                    self.dictionary[key].extend(dict[key])
                else:
                    self.dictionary[key] = dict[key]
                    self.max_key_length = max(len(key), self.max_key_length)

    def tag(self, tagged_sent):
        return [self.tag_sentences(sent) for sent in tagged_sent]

    def tag_sentences(self, sentence, tag_with_lemma=False):
        final_tagged_sent = []
        N = len(sentence)
        if self.max_key_length==0:
            self.max_key_length=N
        i = 0
        while(i<N):
            tag_done = False
            j = min(i + self.max_key_length, N)
            while(i<j):
                form = ' '.join([word[0] for word in sentence[i:j]]).lower()
                lemma = ' '.join([word[1] for word in sentence[i:j]]).lower()
                if tag_with_lemma:
                    match_token = lemma
                else:
                    match_token = form
                if match_token in self.dictionary:
                    single_token = j-i ==1
                    initial_pos = i
                    i = j
                    new_tag = [new_tag for new_tag in self.dictionary[match_token]]
                    new_tagged_token = (form, lemma, new_tag)
                    if single_token:
                        initial_tag = sentence[initial_pos][2]
                        new_tagged_token[2].extend(initial_tag)
                        final_tagged_sent.append(new_tagged_token)
                        tag_done = True
                else:
                        j-=1
            if not tag_done:
                final_tagged_sent.append(sentence[i])
                i+=1
        return  final_tagged_sent
def value_of(mood):
    if mood == 'happy': return [1,0]
    if mood == 'sad': return [-1,0]
    if mood == 'excited': return [0,1]
    if mood == 'calm' : return [0,-1]
    return [0,0]

def sentence_score(sentence_tokens, previous_token, acum_score):
    if not sentence_tokens:
        return acum_score
    else:
        current_token = sentence_tokens[0]
        tags = current_token[2]
        token_score = [0,0]
        val = 0.0
        for tag in tags:
            val = value_of(tag);
            token_score[0] += val[0]        #happiness score
            token_score[1] += val[1]        #excitement score

        if token_score[0]!=0:
            type = 0                    #type 0 for happiness scale
        else:
            type = 1
        if previous_token is not None:
            previous_tags = previous_token[2]
            if 'hyper' in previous_tags:
                token_score[type] *= 2.0
            elif 'less' in previous_tags:
                token_score[type] /= 2.0
            elif 'opp' in previous_tags:
                token_score[type] *= -1.0
        acum_score[0] += token_score[0]
        acum_score[1] += token_score[1]
        return sentence_score(sentence_tokens[1:], current_token, acum_score)
def mood_score(content):
    #scores for whole content
    sent_scores = [sentence_score(sent, None, [0.0, 0.0]) for sent in content]
    content_score = [0,0]
    n = len(sent_scores)
    for sent_moods in sent_scores:
        content_score[0] += sent_moods[0]
        content_score[1] += sent_moods[1]
    #print (content_score)
    content_score[0] = content_score[0]/(n*2)
    content_score[1] = content_score[1]/(n*2)
    return content_score
def direct_play(content):
    lines = content.split('.')
    flag = False
    for line in lines:
        words = line.split()
        if 'play' in words[0].lower():
            flag = True
            break
    if flag is True:
        play_choose.initialise(line)
    else:
        return

if __name__ == "__main__":
    mood = (0,0)
    wordify = Wordify()
    postagger = POStagger()
    text = input("Enter your text")
    direct_play(text)
    sentence_tokens = wordify.split_words(text)
    sentence_tags = postagger.tagger(sentence_tokens)
    dictTagger = DictionaryTagger(['dict/happy.yml', 'dict/sad.yml', 'dict/opp.yml', 'dict/hyper.yml', 'dict/excited.yml', 'dict/less.yml', 'dict/calm.yml'])
    final_dict_tagging = dictTagger.tag(sentence_tags)
    score = mood_score(final_dict_tagging)
    print (final_dict_tagging)
    print ('The final score is ', score)
    choose_song(score)

