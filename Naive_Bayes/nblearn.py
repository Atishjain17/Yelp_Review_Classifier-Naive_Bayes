import json
import random
import collections,copy
import sys

input_file = open(sys.argv[1],'r')
input = input_file.read()
input_file.close()
input = input.split('\n')
del input[-1]
label_file = open(sys.argv[2],'r')
label = label_file.read()
label_file.close()
label = label.split('\n')
del label[-1]
for i in range(len(label)):
    label[i]=label[i].split()

global punctuations,prepositions,articles,conjunctions,auxillary_verbs,pronouns,specifics
global dict2,dict3
global dec_pos_prior,dec_neg_prior,tru_pos_prior,tru_neg_prior
dec_pos_prior=0
dec_neg_prior=0
tru_pos_prior=0
tru_neg_prior=0

dict2 = {'dec_pos':{}, 'dec_neg':{}, 'tru_pos':{}, 'tru_neg':{}}
dict3={}
dict4 = {'dec_pos':{}, 'dec_neg':{}, 'tru_pos':{}, 'tru_neg':{}}


punctuations = [',', '.', '?', ';', '`', ':', '"', '\'', '[', ']', '{', '}', '(', ')', '<', '>', '~', '#', '/','\\', '!']

articles = ['a','an','the']

conjunctions = ['and','or','but','so','for','after','although','as','because','before','even','if','though','once','which'
                'since','that','till','unless','until','what','when','whereever','whenever','whether','while','yet','who']

prepositions = ['with','at','from','into','during','including','until','against','among','throughout','despite','towards',
                'upon','of','to','in','for','on','by','about','like','through','over','between','following','along','across',
                'beyond','behind','under','within','except','near','above','up','down','out','around','off','aboard','about',
                'below','beneath','besides','']

auxillary_verbs = ['be','can','could','do','did','does','has','had','have','being','is','am','was','are','were',
                   'may','might','must','shall','should','will','would']

pronouns=['i','me','myself','we','us','ourselves','you','your','yourself','yourselves','he','him','himself','she','her',
          'herself','it','itself','they','them','themselves','my','mine','yours','our','ours','their','theirs','this',
          'that','these','those']

specifics=['hotel','room','rooms','night','service','staff','bed','business']

def split_data(input1,percent):
    global train_set
    global test_set
    count=int(len(input1)*(percent/100.0))
    test_set=random.sample(input1, count)
    print(test_set)
    f = open("test.txt", "w+")
    for i in range(len(test_set)):
        f.write(test_set[i]+'\n')
    f.close
    train_set = [v for i, v in enumerate(input1) if v not in frozenset(test_set)]
    print(len(train_set))
    test_label_set = [v for i, v in enumerate(label) if v not in frozenset(test_set)]
    f = open("test_label.txt", "w+")
    for i in range(len(test_label_set)):
        f.write(test_label_set[i]+'\n')
    f.close

def delete_punctuations(current_review):
    for i in range(len(punctuations)):
        current_review = current_review.replace(punctuations[i], " ")
    return current_review

def delete_contractions(current_review):
    current_review = current_review.replace("'s", " is")
    current_review = current_review.replace("n't", " not")
    current_review = current_review.replace("'ve", " have")
    current_review = current_review.replace("'m", " am")
    current_review = current_review.replace("'d", " had")
    current_review = current_review.replace("'ll", " will")
    return current_review

def delete_articles(current_review):
    for i in range(len(articles)):
        current_review = current_review.replace(" "+articles[i]+" ", " ")
    return current_review

def delete_prepositions(current_review):
    for i in range(len(prepositions)):
        current_review = current_review.replace(" "+prepositions[i]+" ", " ")
    return current_review

def delete_conjunctions(current_review):
    for i in range(len(conjunctions)):
        current_review = current_review.replace(" "+conjunctions[i]+" ", " ")
    return current_review

def delete_auxillary_verbs(current_review):
    for i in range(len(auxillary_verbs)):
        current_review = current_review.replace(" "+auxillary_verbs[i]+" ", " ")
    return current_review

def delete_pronouns(current_review):
    for i in range(len(pronouns)):
        current_review = current_review.replace(" "+pronouns[i]+" ", " ")
    return current_review

def delete_specifics(current_review):
    for i in range(len(specifics)):
        current_review = current_review.replace(" "+specifics[i]+" ", " ")
    return current_review

def evaluate_text(current_review):
    current_review = delete_contractions(current_review)
    current_review = delete_punctuations(current_review)
    current_review = current_review.lower()
    current_review = delete_articles(current_review)
    current_review = delete_prepositions(current_review)
    current_review = delete_conjunctions(current_review)
    current_review = delete_auxillary_verbs(current_review)
    current_review = delete_pronouns(current_review)
    current_review = delete_specifics(current_review)
    current_review = current_review.split()
    return current_review

def seperate_classes(label,dict1):
    global dec_pos_prior,dec_neg_prior,tru_pos_prior,tru_neg_prior
    for i in range(len(label)):

        if(label[i][1] == 'deceptive' and label[i][2] == 'positive'and dict1.get(label[i][0])!=None):
            current_review =  dict1.get(label[i][0])
            dec_pos_prior += 1
            for j in range(len(current_review)):
                if(current_review[j] in dict2['dec_pos']):
                    dict2['dec_pos'][current_review[j]] += 1
                else:
                    dict2['dec_pos'][current_review[j]] = 1

        elif(label[i][1] == 'deceptive' and label[i][2] == 'negative'and dict1.get(label[i][0])!=None):
            current_review =  dict1.get(label[i][0])
            dec_neg_prior += 1
            for j in range(len(current_review)):
                if(current_review[j] in dict2['dec_neg']):
                    dict2['dec_neg'][current_review[j]] += 1
                else:
                    dict2['dec_neg'][current_review[j]] = 1

        elif(label[i][1] == 'truthful' and label[i][2] == 'positive'and dict1.get(label[i][0])!=None):
            current_review =  dict1.get(label[i][0])
            tru_pos_prior += 1
            for j in range(len(current_review)):
                if(current_review[j] in dict2['tru_pos']):
                    dict2['tru_pos'][current_review[j]] += 1
                else:
                    dict2['tru_pos'][current_review[j]] = 1

        elif(label[i][1] == 'truthful' and label[i][2] == 'negative'and dict1.get(label[i][0])!=None):
            current_review =  dict1.get(label[i][0])
            tru_neg_prior += 1
            for j in range(len(current_review)):
                if(current_review[j] in dict2['tru_neg']):
                    dict2['tru_neg'][current_review[j]] += 1
                else:
                    dict2['tru_neg'][current_review[j]] = 1

        if(dict1.get(label[i][0])!=None):
            current_review = dict1.get(label[i][0])
            for j in range(len(current_review)):
                if(current_review[j] in dict3):
                    dict3[current_review[j]] += 1
                else:
                    dict3[current_review[j]] = 1

def delete_lower_count(dict2,dict3):
    temp_key=[]
    for word, word_count in dict3.items():
        if(word_count <= 4 ):
            if(word in dict2['dec_pos']):
                del dict2['dec_pos'][word]

            if (word in dict2['dec_neg']):
                del dict2['dec_neg'][word]

            if (word in dict2['tru_pos']):
                del dict2['tru_pos'][word]

            if (word in dict2['tru_neg']):
                del dict2['tru_neg'][word]
            temp_key.extend([word])
    for i in range (len(temp_key)):
        del dict3[temp_key[i]]

def smoothing(dict2,dict3):
    for word,v in dict3.items():
        if(word in dict2['dec_pos']):
            dict2['dec_pos'][word] += 1
        else:
            dict2['dec_pos'][word]=1

        if (word in dict2['dec_neg']):
            dict2['dec_neg'][word] += 1
        else:
            dict2['dec_neg'][word]=1

        if (word in dict2['tru_pos']):
            dict2['tru_pos'][word] += 1
        else:
            dict2['tru_pos'][word]=1

        if (word in dict2['tru_neg']):
            dict2['tru_neg'][word] += 1
        else:
            dict2['tru_neg'][word]=1

def calculate_probability(dict2,total_no_of_unique_word):
    no_of_word_in_dec_pos=0
    no_of_word_in_dec_neg=0
    no_of_word_in_tru_pos=0
    no_of_word_in_tru_neg=0
    for word in dict3:
        no_of_word_in_dec_pos += dict2['dec_pos'][word]
        no_of_word_in_dec_neg += dict2['dec_neg'][word]
        no_of_word_in_tru_pos += dict2['tru_pos'][word]
        no_of_word_in_tru_neg += dict2['tru_neg'][word]
    for word in dict3:
        dict4['dec_pos'][word] = (dict2['dec_pos'][word]+dict2['dec_neg'][word])/((no_of_word_in_dec_pos+no_of_word_in_dec_neg)*1.0)
        dict4['dec_neg'][word] = (dict2['tru_pos'][word]+dict2['tru_neg'][word])/((no_of_word_in_tru_pos+no_of_word_in_tru_neg)*1.0)
        dict4['tru_pos'][word] = (dict2['tru_pos'][word]+dict2['dec_pos'][word])/((no_of_word_in_tru_pos+no_of_word_in_dec_pos)*1.0)
        dict4['tru_neg'][word] = (dict2['tru_neg'][word]+dict2['dec_neg'][word])/((no_of_word_in_tru_neg+no_of_word_in_dec_neg)*1.0)

split_data(input,20)
dict1 = collections.OrderedDict()
for i in range(len(train_set)):
    current_review=copy.deepcopy(train_set[i][20:])
    dict1[train_set[i][:20]]= evaluate_text(current_review)

seperate_classes(label,dict1)
#delete_lower_count(dict2,dict3)
smoothing(dict2,dict3)
calculate_probability(dict2,len(dict3))

print(len(dict3))
print(dec_pos_prior)
print(dec_neg_prior)
print(tru_pos_prior)
print(tru_neg_prior)
dict4['prior_probability']={}

total_sample = dec_pos_prior+dec_neg_prior+tru_pos_prior+tru_neg_prior
dict4['prior_probability']['dec_pos_prior'] = (dec_pos_prior+dec_neg_prior) / (total_sample*1.0)
dict4['prior_probability']['dec_neg_prior'] = (tru_pos_prior+tru_neg_prior) / (total_sample*1.0)
dict4['prior_probability']['tru_pos_prior'] = (tru_pos_prior+dec_pos_prior) / (total_sample*1.0)
dict4['prior_probability']['tru_neg_prior'] = (tru_neg_prior+dec_neg_prior) / (total_sample*1.0)
print(dict4['prior_probability'])
f = open("model.json", "w+")
json.dump(dict4,f)
f.close()