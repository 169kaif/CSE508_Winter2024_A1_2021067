#make imports
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#MAKE SURE NLTK CORPUS IS DOWNLOADED BEFORE RUNNING

def write_to_sample(file_read_path, file_write_path):

    #init list to store the file content
    file_data = []

    #open file to read and add data to the file_data
    with open(file_read_path, 'r') as f:
        for line in f:
            file_data.append(line)

    #write data to sample file
    with open(file_write_path, 'a') as f:
        f.write("Data: \n")
        for line in file_data:
            f.write(line)
        f.write("\n\n\n")

def write_wordlist2file(word_list, file_path):

    with open(file_path, 'w') as f:
        for word in word_list:
            f.write(word + "\n")


def lowercase_text(file_read_path, file_write_path):

    #init list to store the lowercase lines
    lowercase_data = []

    #open file to read and convert line to lowercase using the lower() function
    with open(file_read_path, 'r') as curr_file:
        for line in curr_file:
            lowercase_data.append(line.lower())

    #write data to new file
    with open(file_write_path, 'w') as new_file:
        for line in lowercase_data:
            new_file.write(line)

#use the nltk tokenize function to tokenize the text
def tokenize_text(file_path):

    #init string to store text data from file
    text_to_tokenize = ""

    with open(file_path, 'r') as temp_file:
        for line in temp_file:
            text_to_tokenize += line

    #use the word tokenize function
    tokenized_text = word_tokenize(text_to_tokenize)

    #write the tokenzied words to the file
    write_wordlist2file(tokenized_text, file_path)

    return tokenized_text

#remove stopwords using the nltk stopwords corpus
def remove_stopwords(word_array, file_path):

    stop_words = set(stopwords.words('english'))

    #store tokenized words except for the stop words
    tokenized_words = []

    for word in word_array:
        if word not in stop_words:
            tokenized_words.append(word)

    write_wordlist2file(tokenized_words, file_path)

    return tokenized_words

def remove_punctuation(word_array, file_path):

    #init array to store words that are not punctuation
    np_words = []

    for word in word_array:
        new_word = ""
        for char in word:
            if (char.isalnum()):
                new_word += char
        if (len(new_word) > 0):
            np_words.append(new_word)

    write_wordlist2file(np_words, file_path)

    return np_words

def remove_blankspace(word_array, file_path):

    #init array to store words without blankspace
    bl_words = []

    for word in word_array:
        new_word = "".join(word.split())
        bl_words.append(new_word)

    write_wordlist2file(bl_words, file_path)

#----------------------main---------------------#            

sample_file_count = 1
        
# loop to apply the above functions to all files
for file in os.listdir("text_files"):

    file_read_path = "text_files" + "/" + file
    file_write_path = "preprocessed_files" + "/" + file
    sample_file_write_path = "sample_files" + "/" + str(sample_file_count) + ".txt"

    #create the sample file to track updates
    if (sample_file_count <= 5):
        with open(sample_file_write_path, 'a') as temp_file:
            temp_file.write(f"Tracking updates for file: {file_read_path} \n\n\n")
        write_to_sample(file_read_path, sample_file_write_path)

    #apply the lowercase function
    lowercase_text(file_read_path, file_write_path)

    #update the sample file to add changes after lowercase function
    if (sample_file_count <= 5):
        write_to_sample(file_write_path, sample_file_write_path)

    #init array to store tokenized text data
    #tokenize text
    tokenized_text_array = tokenize_text(file_write_path)

    #update the sample file to add changes after tokenize function
    if (sample_file_count <= 5):
        write_to_sample(file_write_path, sample_file_write_path)

    #init array to store tokenized words without the stop words
    #get rid of stop words
    sw_tokenized_text_array = remove_stopwords(tokenized_text_array, file_write_path)

    #update the sample file to add changes after removing the stop words
    if (sample_file_count <= 5):
        write_to_sample(file_write_path, sample_file_write_path)

    #init array to store tokenized words without the stop words and punctuation marks
    swp_tokenized_text_array = remove_punctuation(sw_tokenized_text_array, file_write_path)

    #update the sample file to add changes after removing the punctuation marks
    if (sample_file_count <= 5):
        write_to_sample(file_write_path, sample_file_write_path)

    #remove blank space
    remove_blankspace(swp_tokenized_text_array, file_write_path)

    #update the sample file to add changes after removing blankspace
    if (sample_file_count <= 5):
        write_to_sample(file_write_path, sample_file_write_path)

    sample_file_count += 1