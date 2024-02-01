#make imports
import os
from nltk.tokenize import word_tokenize

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
    with open(file_path, 'w') as temp_file:
        for word in tokenized_text:
            temp_file.write(word + "\n")

    return tokenized_text


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

    sample_file_count += 1