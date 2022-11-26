#!/usr/bin/python3
import os
import sys
import subprocess
import re
import pandas as pd

os.chdir(os.environ['HOME']) #Change directory to homespace
os.getcwd() #Make sure the current directory is your homespace
path_1 = os.environ['HOME'] 
os.system('rm -fr ~/ICA2/protein_data_output') #Remove the sub-directory protein_data 
os.mkdir(path_1 + "/ICA2/protein_data_output/") #Make a new directory called protein_data
os.chdir(path_1 + "/ICA2/protein_data_output/")

def get_protein_content():  #Define a function
    os.system('rm -fr ~/ICA2/protein_data_output/error.txt')
    protein_name = input ("Enter the protein name: ") #Ask the user to input the name of the protein of interest 
    protein_name_file = protein_name.replace(' ', '_') #replace the name of protein 
    Taxon_ID = input ("Enter the Taxon ID: ") #Ask the user to input the taxon ID
    output_file =path_1+ f'/ICA2/protein_data_output/{protein_name_file}_{Taxon_ID}.fasta'
#esearch is used to pull up the protein data  using the variables protein_name and Taxon_ID, and output the protein data into a fasta file, this is assigned to a variable called esearch_var 
#If any error is found,  2>error.txt is used to redirect the error message shown on the screen to the textfile error.txt
    esearch_var = f"esearch -db protein -query '{protein_name}[PROTEIN]' 2>error.txt | efilter -query txid'{Taxon_ID}'[ORGANISM] 2>error.txt | efetch -format fasta 2>error.txt > ~/ICA2/protein_data_output/{protein_name_file}_{Taxon_ID}.fasta"
    os.system(esearch_var) # os.system commamd is used to run the variable esearch_var
    print("protein sequences successfully downloaded")
    return protein_name, Taxon_ID, output_file, protein_name_file

protein_name, Taxon_ID, output_file, protein_name_file = get_protein_content()  #calling out the function get_protein_content and assigning the function to three variables protein_name, Taxon_ID and output_file.
#print a statement to let the user know the name, taxon id and the location of the chosen protein of interest.
print("The protein of interest is" , protein_name, "with taxon id" , Taxon_ID, "located in" , output_file)


with open("error.txt", "r") as file:   #Create a with loop to read the entire file error.txt 
    try :   #try except for error trapping is used 
        if os.stat("error.txt").st_size > 0 : #This command is used to check the content of the file, if the file contains anything,it means that there is an error in the input the used have choson  
            print("invalid protein, please try again using a valid protein name and Taxon ID") #If an error is found, this statement will be printed on the screen to warn the user that the the protein they have chosen is invalid.
    except :
        print("The protein is valid")

os.chdir(os.environ['HOME']) #change directory to the homespace
path = os.environ['HOME'] 
path1 = (path + "/ICA2/protein_data_output")
os.chdir = (path1)
os.listdir()
my_fasta_file = open(output_file) #open a connection (output_file) and assign it to a variable called my_fasta_file which refers to the file that contains the protein information  
protein_id = [] #Make an empty list and assign it to a variable called  protein_id
protein_name = [] #Make an empty list and assign it to a variable called protein_name
species = [] #Make an empty list and assign it to a variable called species
protein_sequence = [] #Make an empty list and assign it to a variable called protein_sequence

for eachline in my_fasta_file : 
    if eachline.startswith(">") :
        protein_id_search = eachline.split()[0]
        print(protein_id_search)
        protein_id.append(protein_id_search)
        protein_headerline =  re.search('(^>)''(.+)''(\[.+\])', eachline)
        species_search = re.search('(\[.+\])', eachline).group(0)
        print(species_search)
        if species_search :
            species.append(species_search)
            id_removed = eachline.replace(protein_id_search, '')
            protein_name_search = id_removed.replace(species_search, '')
            print(protein_name_search)
        if protein_name_search :
            protein_name.append(protein_name_search)
    else :
        protein_sequence_search = protein_sequence.append(eachline)
       # print(protein_sequence)

#Make a dataframe
s1 = pd.Series(protein_id_search)
s2 = pd.Series(protein_name_search)
s3 = pd.Series(species_search)
s4 = pd.Series(protein_sequence_search,dtype=pd.StringDtype())
df = pd.DataFrame ( { 'protein_id' : s1, 'protein_name' : s2, 'species' : s3, 'protein_sequence' : s4 } )
print(df)

#Running Clustalo 
path = os.environ['HOME'] #The homespace is stored into a variable called path

my_fasta_file_original = path + f"/ICA2/protein_data_output/{protein_name_file}_{Taxon_ID}.fasta" #The path variable and the string is assigned to a variable my_fasta_file_original, which contains the fasta file {protein_name_file}_{Taxon_ID}.fasta
my_fasta_file_aligned = path + f"/ICA2/protein_data_output_aligned" #The paih variable and the string 
clustalo_cmd = f'clustalo -i {my_fasta_file_original} -o {my_fasta_file_aligned} -v --outfmt msf --force'
os.system(clustalo_cmd)

#Running Plotcon
my_fasta_file_aligned = path + f"/ICA2/protein_data_output_aligned" 
plotcon_cmd = f'plotcon -sformat -msf {my_fasta_file_aligned} -winsize 4 -graph x11' 

def plotcon_user_input(question= 'Do you want to view the plot now using plotcon?'):
    while "The answer to view the plot is invalid" :
        plotcon_reply = str(input(question+ '[y/n]:')).lower().strip()
        if plotcon_reply[:1] == 'y':
            os.system(plotcon_cmd)
            print("plotcon is currently running, please wait")
            return True
        if plotcon_reply[:1] == 'n':
            print("Exiting plotcon.....")
            return False
plotcon_user_input(question= 'Do you want to view the plot now using plotcon')
