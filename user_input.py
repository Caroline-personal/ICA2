#!/usr/bin/python3
import os
import sys
import subprocess
import re
import pandas as pd
from pathlib import Path

os.chdir(os.environ['HOME']) #Change directory to homespace
os.getcwd() #Make sure the current directory is your homespace
path_1 = os.environ['HOME'] 
os.system('rm -f -r ~/ICA2/protein_data_output') #Remove the sub-directory protein_data 
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
    esearch_var = f"esearch -db protein -query '{protein_name}[PROTEIN]' 2>error.txt NOT PARTIAL | efilter -query txid'{Taxon_ID}'[ORGANISM] 2>error.txt NOT PARTIAL | efetch -format fasta 2>error.txt NOT PARTIAL > ~/ICA2/protein_data_output/{protein_name_file}_{Taxon_ID}.fasta"
    os.system(esearch_var) # os.system commamd is used to run the variable esearch_var
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
organism = [] #Make an empty list and assign it to a variable called species
protein_sequence = [] #Make an empty list and assign it to a variable called protein_sequence

for eachline in my_fasta_file : 
    if eachline.startswith(">") :
        protein_id_search = eachline.split()[0]
        print(protein_id_search)
        protein_id.append(protein_id_search)
        protein_headerline =  re.search('(^>)''(.+)''(\[.+\])', eachline)
        organism_search = re.search('(\[.+\])', eachline).group(0)
        print(organism_search)
    if organism_search :
        organism.append(organism_search)
        id_removed = eachline.replace(protein_id_search, '')
        protein_name_search = id_removed.replace(organism_search, '')
        print(protein_name_search)
    if protein_name_search :
        protein_name.append(protein_name_search)
    else :
        if protein_sequnece_search :
            protein_sequence_search = protein_sequence.append(eachline)
            print(protein_sequence_search)

#Make a dataframe
s1 = pd.Series(protein_id)
s2 = pd.Series(protein_name)
s3 = pd.Series(organism_search)
s4 = pd.Series(protein_sequence,dtype=pd.StringDtype())
df = pd.DataFrame ({'protein_id' : s1, 'protein_name' : s2, 'organism' : s3, 'protein_sequence' : s4 })
print(df)
csv_convert = path+ '/ICA2'
df.to_csv(path+'/ICA2/'+protein_name_file+'_'+Taxon_ID+'.csv', sep='\t')

organism_count = df['organism'].value_counts()
print(organism_count)



#Running Clustalo
path = os.environ['HOME'] #The homespace is stored into a variable called path

my_fasta_file_original = path + "/ICA2/protein_data_output/"+protein_name_file+"_"+Taxon_ID+".fasta" #The path variable and the string is assigned to a variable my_fasta_file_original, which contains the fasta file {protein_name_file}_{Taxon_ID}.fasta
my_output_file_clustalo = path + f"/ICA2/protein_data_output_aligned" #The path variable and the string containing the file protein_data_output_aligned is assigned to a variable called my_output_file_aligned, which contains the data generated by clustalo in msf form.
#clustalo command is put into a string and run using an input file (my_fasta_file_original) and the output is put into a file called my_output_file_clustalo in msf form, the string is then assigned to the variable clustalo_cmd
clustalo_cmd = f'clustalo -i {my_fasta_file_original} -o {my_output_file_clustalo} -v --outfmt msf --force'

def clustalo_user_input(question= 'Do you want to run Clustalo for sequence alignement?'): #Defining a function
    while "The answer to run clustalo is invalid" : #A while loop is used to prompt the user for input if they give an invalid answer
        clustalo_user_reply = str(input(question+ '[y/n]:')).lower().strip() #Ask the user for input (y/n) for running clustalo analysis
#If loop is used, giving instructions to run clustalo_cmd variable (clustalo analysis) if the user input is y 
        if clustalo_user_reply[:1] == 'y':
            os.system(clustalo_cmd) #os.system command is used to run the variable clustalo_cmd
            print("Clustalo analysis is done, please see the results") #A statement is shown on the screen to update the user that the clustalo analysis is done
            return True #Exiting the function
#If loop is used, giving instructions to exit clustalo idf the user input to the question is n
        if clustalo_user_reply[:1] == 'n':
            print ("Exiting Clustalo .....") #A statement updating the user that clustalo analysis is not done
            return False #Exiting the function 

clustalo_user_input(question= 'Do you want to run Clustalo for sequence alignement?') #Calling the function

#Running infoalign
os.system('rm -fr ~/ICA2/infoalign_output/')
os.mkdir(path + "/ICA2/infoalign_output/") # +protein_name_file+"_"+Taxon_ID+".infpalign")
my_output_file_infoalign = path + "/ICA2/infoalign_output/"  #+protein_name_file+"_"+Taxon_ID+".infoalign"
infoalign_cmd = f'infoalign -sequence {my_output_file_clustalo} -odirectory2 {my_output_file_infoalign} -'

def infoalign_user_input(question= 'Do you want to run infoalign to learn more information about the asligned sequences?'):
    while "The answer to run infoalign is invalid" :
        infoalign_user_reply = str(input(question+ '[y/n]:')).lower().strip()
        if infoalign_user_reply[:1] == 'y':
            os.system(infoalign_cmd)
            print("infoalign analysis is done, please view the results in the output file")
            return True
        if infoalign_user_reply[:1] == 'n':
            print("Exiting infoalign....")
            return False
infoalign_user_input(question= 'Do you want to run infoalign to learn more information about the aligned sequences?')

#Running Plotcon
my_output_file_clustalo = path + f"/ICA2/protein_data_output_aligned" # The variable (path) and the string containing the file protein_data_output_aligned are assigned to the variable my_output_file_clustalo 
plotcon_cmd = f'plotcon -sformat -msf {my_output_file_clustalo} -winsize 4 -graph x11' #plotcon command is put into a string and run using the output file (msf form) generated by clustalo, and this is assigned to the variable plotcon_cmd. The window size is set to 4 and the graph type is set to x11 by default.

def plotcon_user_input(question= 'Do you want to view the plot now using plotcon?'): #Defining a function 
    while "The answer to view the plot is invalid" : # A while loop is used to prompt the user for input if the answer they gave is invalid
        plotcon_reply = str(input(question+ '[y/n]:')).lower().strip() #Ask the user for input (y/n) to your question
#If loop is used, giving instructions to run the plotcon_cmd variable if the user input is y and this shows the plot of the protein selected on the screen. 
        if plotcon_reply[:1] == 'y':
            os.system(plotcon_cmd)
            print("plotcon is currently running and the plot will be shown on the screen, please wait")
            return True #exiting the function
#If loop is used, giving instructions to not run (exit) plotcon if the user input is n 
        if plotcon_reply[:1] == 'n':
            print("Exiting plotcon.....")
            return False #exiting the function
plotcon_user_input(question= 'Do you want to view the plot now using plotcon') #run the function plotcon_user_input

#Running prosite
#The single fasta file will be split into seperate fasta files with  individual protein sequences first by seqretsplit.
#Running seqretsplit
my_fasta_file_original = (os.environ['HOME'] + "/ICA2/protein_data_output/"+protein_name_file+"_"+Taxon_ID+".fasta") #The path variable and the string is assigned to a variable my_fasta_file_original, which contains the fasta file {protein_name_file}_{Taxon_ID}.
seqretsplit_output = (os.environ['HOME'] + "/ICA2/prosite_output/seqretsplit_results/") #variable seqretsplit_output is created to be used when running seqretsplit command line, as all the fasta files containing individual sequences will be assigned to this variable.
os.system(f'rm -f -r {seqretsplit_output}') #remove the variable seqretsplit_output
os.makedirs( seqretsplit_output ) #make a directory with the path assigned to variable seqretsplit_cmd 
#Assign the  seqretsplit command to the variable seqretsplit_cmd, put the command line in a string and split the single fasta file in my_fasta_file_original variable into individual sequences (in seperate fasta files) that can be scanned by patmatmotifs. The fasta files generated will be put into seqretsplit_output 
seqretsplit_cmd = f"seqretsplit -sequence {my_fasta_file_original} -osdirectory2 {seqretsplit_output} -" 
os.system( seqretsplit_cmd) #Run the seqretsplit_cmd

#Scanning protein sequences using patmatmotifs
prosite_results = (os.environ['HOME'] + "/ICA2/prosite_output/patmotifs_output/") #Assign the directory that ends with .patmatmotifs into a variable called prosite_results
os.system(f'rm -f -r {prosite_results}') #remove the variable prosite_results
os.makedirs( prosite_results ) #make a directory using the variable prosite_results
prosite_files = Path(seqretsplit_output).glob('*')
for file in prosite_files:
    prosite_cmd = f"patmatmotifs -sequence {file} -rdirectory2 {prosite_results} -"
    os.system(prosite_cmd)

