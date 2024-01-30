#making imports
import os

def lowercase_text(file_read_path, file_write_path):

    #open file to read
    curr_file = open(file_read_path, 'r')

    #init list to store the lowercase lines
    lowercase_data = []

    #convert line to lowercase using the lower() function
    for line in curr_file:
        lowercase_data.append(line.lower())

    #write data to new file
    new_file = open(file_write_path, 'a')
    for line in lowercase_data:
        new_file.write(line)
        
# loop to apply the above functions to all files
for file in os.listdir("text_files"):

    file_read_path = "text_files" + "/" + file
    file_write_path = "preprocessed_files" + "/" + file

    #apply the lowercase function
    lowercase_text(file_read_path, file_write_path)