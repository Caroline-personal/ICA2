#!/usr/bin/python3
import os
import sys
import subprocess

os.chdir(os.environ['HOME']) #Change directory to homespace
os.getcwd() #Make sure the current directory is your homespace
path_1 = os.environ['HOME'] 
os.system('rm -fr ~/ICA2/protein_data_output') #Remove the sub-directory protein_data 
os.mkdir(path_1 + "/ICA2/protein_data_output/") #Make a new directory called protein_data
os.chdir(path_1 + "/ICA2/protein_data_output/")

def get_protein_content():  #Define a function 
    protein_name = input ("Enter the protein name: ") #Ask the user to input the name of the protein of interest 
    protein_name_file = protein_name.replace(' ', '_') #replace the name of protein 
    Taxon_ID = input ("Enter the Taxon ID: ") #Ask the user to input the taxon ID
#esearch is used to pull up the protein data  using the variables protein_name and Taxon_ID, and output the protein data into a fasta file, this is assigned to a variable called esearch_var 
#If any error is found,  2>error.txt is used to redirect the error message shown on the screen to the textfile error.txt
    esearch_var = f'esearch -db protein -query "{protein_name}[PROTEIN]" 2>error.txt | efilter -query txid"{Taxon_ID}"[ORGANISM] 2>error.txt | efetch -format fasta 2>error.txt > ~/ICA2/protein_data_output/{protein_name_file}_{Taxon_ID}.fasta'
    os.system(esearch_var) # os.system commamd is used to run the variable esearch_var
    print("protein sequences successfully downloaded")
    return

get_protein_content()  #calling out the function get_protein_content

with open("error.txt", "r") as file:   #Create a with loop to read the entire file error.txt 
    try :   #try except for error trapping is used 
        if os.stat("error.txt").st_size > 0 : #This command is used to check the content of the file, if the file contains anything,it means that there is an error in the input the used have choson  
            print("invalid protein, please try again using a valid protein name and Taxon ID") #If an error is found, this statement will be printed on the screen to warn the user that the the protein they have chosen is invalid.
    except :
        print("The protein is valid")
