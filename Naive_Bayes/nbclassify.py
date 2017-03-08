import json
import collections,copy
import math
import sys

input_file = open(sys.argv[1],'r')
test_set = input_file.read()
input_file.close()

test_set = test_set.split('\n')
del test_set[-1]

print(len(test_set))
global punctuations,prepositions,articles,conjunctions,auxillary_verbs,pronouns,specifics

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

f=open('model.json','r')
prob_model=json.load(f)
f.close()
print(prob_model['prior_probability'])

dict1 = collections.OrderedDict()
for i in range(len(test_set)):
    current_review=copy.deepcopy(test_set[i][20:])
    dict1[test_set[i][:20]]= evaluate_text(current_review)
file=open("nboutput.txt",'w')
for sample,word_list in dict1.items():
    answer=[1,1,1,1]
    for word in word_list:
        if word in prob_model['dec_pos']:
            answer[0]=answer[0]+ math.log((prob_model['dec_pos'][word]))
            answer[1] = answer[1] + math.log((prob_model['dec_neg'][word]))
            answer[2] = answer[2] + math.log((prob_model['tru_pos'][word]))
            answer[3] = answer[3] + math.log((prob_model['tru_neg'][word]))

    answer[0] = answer[0] + math.log(prob_model['prior_probability']['dec_pos_prior'])
    answer[1] = answer[1] + math.log(prob_model['prior_probability']['dec_neg_prior'])
    answer[2] = answer[2] + math.log(prob_model['prior_probability']['tru_pos_prior'])
    answer[3] = answer[3] + math.log(prob_model['prior_probability']['tru_neg_prior'])

    if (answer[0]>answer[1]):
        file.write(sample + " " + "deceptive")
    else:
        file.write(sample + " " + "truthful")
    if (answer[2]>answer[3]):
        file.write(" positive" + "\n")
    else:
        file.write(" negative" + "\n")

