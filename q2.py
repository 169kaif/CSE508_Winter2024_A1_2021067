import os
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def extract_file_id(file_name):
    return int(file_name[4:-4])

def and_query(postings_list, t1, t2):

    answer_set = set()

    #handle error to check if either key is not present
    if (t1 not in postings_list.keys()):
        return answer_set
    
    if (t2 not in postings_list.keys()):
        return answer_set

    #if file_id is present in both sets -> add to answer set
    for file_id in postings_list[t1]:
        if file_id in postings_list[t2]:
            answer_set.add(file_id)

    return answer_set

def or_query(postings_list, t1, t2):

    answer_set = set()

    #iterate through postings list of both t1 and t2 and add file_id to answer set
    if (t1 in postings_list.keys()):
        for file_id in postings_list[t1]:
            answer_set.add(file_id)

    if (t2 in postings_list.keys()):
        for file_id in postings_list[t2]:
            answer_set.add(file_id)

    return answer_set

def and_not_query(postings_list, t1, t2):

    answer_set = set()

    #check if t1 is a valid key
    if (t1 in postings_list.keys()):

        #get rid of the common terms
        if (t2 in postings_list.keys()):
            answer_set = postings_list[t1].difference(postings_list[t2])
        else:
            answer_set = postings_list[t1]

    return answer_set

def and_or_query(postings_list, t1, t2):

    answer_set = set()

    #iterate through posting list of t1 and add it to the set
    if (t1 in postings_list.keys()):

        for file_id in postings_list[t1]:
            answer_set.add(file_id)

    #iterate through all file_ids and check if not present in postings list of t2
    if (t2 in postings_list.keys()):

        for i in range(1,1000):
            if i not in postings_list[t2]:
                answer_set.add(i)

    return answer_set

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

#----------------------main---------------------#

#init postings list
postings_list = {}

for file in os.listdir("preprocessed_files"):

    #handling hidden files
    if (file[0] == '.'):
        continue

    file_read_path = "preprocessed_files" + "/" + file
    file_id = extract_file_id(file)

    with open(file_read_path, 'r') as curr_file:
        for line in curr_file:
            curr_word = line.strip()
            if curr_word not in postings_list:
                postings_list[curr_word] = set()
                postings_list[curr_word].add(file_id)
            else:
                postings_list[curr_word].add(file_id)

#specifying dump file path
dump_file_path = "./unigram_inverted_index.pk1"

#saving the unigram inverted index in a dump file
with open(dump_file_path, 'wb') as f:
    pickle.dump(postings_list, f)


#---------query processing-----------#
    
#collect number of queries as input
number_queries = int(input())

for i in range(1, number_queries+1):

    #input query
    input_sequence = input()
    operations = [operation.strip() for operation in input().split(',')]

    #preprocess input_sequence
    processed_sequence = preprocess_text(input_sequence)

    #print the received query
    print("")
    print(f"Query {i}: ", end="")
    for curr_ind in range(len(operations)):
        print(processed_sequence[curr_ind], end=" ")
        print(operations[curr_ind], end = " ")
        if (curr_ind == len(operations)-1):
            print(processed_sequence[curr_ind+1], end=" ")
    print("")

    #process the query
    queried_files = set()
    for curr_index, operation in enumerate(operations):


        #NEED TO ADD FUNCTIONALITY FOR WHEN INSTEAD OF TWO WORDS, WE PROCESS ONE FILE SET AND QUERIED WORD FILE SET