import os
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def extract_file_id(file_name):
    return int(file_name[4:-4])

#lowercase the text
def lowercase_text(input_text):
    return input_text.lower()

#tokenize the text
def tokenize_text(input_text):
    return word_tokenize(input_text)

#remove stop words from the text
def remove_stopwords(input_text):

    stop_words = set(stopwords.words('english'))

    #store words except for the stop words
    cleaned_words = []

    for word in input_text:
        if word not in stop_words:
            cleaned_words.append(word)

    return cleaned_words

#remove punctuation marks
def remove_punctuation(input_text):

    #init array to store words that are not punctuation
    np_words = []

    for word in input_text:
        new_word = ""
        for char in word:
            if (char.isalnum()):
                new_word += char
        if (len(new_word) > 0):
            np_words.append(new_word)

    return np_words

#remove blank space tokens
def remove_blankspace(input_text):

    #init array to store words without blankspace
    bl_words = []

    for word in input_text:
        new_word = "".join(word.split())
        bl_words.append(new_word)

    return bl_words

#apply preprocessing functions to the text
def preprocess_text(input_text):

    #lowercase the text
    input_text = lowercase_text(input_text)

    #tokenize the text
    input_text = tokenize_text(input_text)

    #remove stopwords
    input_text = remove_stopwords(input_text)

    #remove punctuations
    input_text = remove_punctuation(input_text)

    #remove blank space tokens
    input_text = remove_blankspace(input_text)

    return input_text

def phrase_check(file_ind, word_ind, seq_ind, processed_sequence, postings_list):

    if (seq_ind == len(processed_sequence)):
        return True

    curr_word = processed_sequence[seq_ind]

    if file_ind not in postings_list[curr_word]:
        return False
    else:
        if word_ind not in postings_list[curr_word][file_ind]:
            return False
        else:
            return phrase_check(file_ind, word_ind+1, seq_ind+1, processed_sequence, postings_list)


#----------------------main---------------------#

#init postings list
postings_list = {}

for file in os.listdir("preprocessed_files"):

    #handling hidden files
    if (file[0] == '.'):
        continue

    file_read_path = "preprocessed_files" + "/" + file
    file_id = extract_file_id(file)

    curr_word_ind = 0

    with open(file_read_path, 'r') as curr_file:
        for line in curr_file:
            curr_word = line.strip()
            if curr_word not in postings_list:
                postings_list[curr_word] = {file_id: [curr_word_ind]}
            else:
                if file_id in postings_list[curr_word]:
                    postings_list[curr_word][file_id].append(curr_word_ind)
                else:
                    postings_list[curr_word][file_id] = [curr_word_ind]

            curr_word_ind += 1

#specifying dump file path
dump_file_path = "./positional_index.pk1"

#saving the unigram inverted index in a dump file
with open(dump_file_path, 'wb') as f:
    pickle.dump(postings_list, f)

#---------query processing-----------#
    
#collect number of queries as input
number_queries = int(input())

for i in range(1, number_queries+1):

    #input query
    input_sequence = input()

    #preprocess input_sequence
    processed_sequence = preprocess_text(input_sequence)

    #set to store the queried files
    queried_files = set()

    #store first word to identify the start of phrase and recursively check for other 
    #words of the phrase
    first_word = processed_sequence[0]

    if first_word in postings_list.keys():
        for file in postings_list[first_word]:
            for word_ind in postings_list[first_word][file]:
                if (phrase_check(file, word_ind+1, 1, processed_sequence, postings_list)):
                    queried_files.add(file)

    print(f"Number of documents retrieved for query {i}: " + str(len(queried_files)))
    print(f"Names of the documents retrieved for query {i}: ", end="")
    for file_id in queried_files:
        print("file" + str(file_id) + ".txt,", end="")
    print("\n")