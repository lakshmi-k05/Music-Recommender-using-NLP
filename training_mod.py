import yaml

def train_data():

    positivedata = {}
    reader = open('dict/positive-words.txt', 'r')
    word = reader.readlines()
    for w in word:
        w = w.split('\n');
        positivedata[w[0]] = ['happy']
    with open('dict/happy.yml','w') as outfile:
        yaml.dump(positivedata, outfile, default_flow_style = False)

    negativedata = {}
    reader = open('dict/sad-words.txt', 'r')
    word = reader.readlines()
    for w in word:
        w = w.split('\n');
        negativedata[w[0]] = ['sad']
    with open('dict/sad.yml', 'w') as outfile:
        yaml.dump(negativedata, outfile, default_flow_style=False)

    calmdata = {}
    reader = open('dict/calming-words.txt', 'r')
    word = reader.readlines()
    for w in word:
        w = w.split('\n');
        calmdata[w[0]] = ['calm']
    with open('dict/calm.yml', 'w') as outfile:
        yaml.dump(calmdata, outfile, default_flow_style=False)

    exciteddata = {}
    reader = open('dict/excited-words.txt', 'r')
    word = reader.readlines()
    for w in word:
        w = w.split('\n');
        exciteddata[w[0]] = ['excited']
    with open('dict/excited.yml', 'w') as outfile:
        yaml.dump(exciteddata, outfile, default_flow_style=False)
