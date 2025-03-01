import csv
import spacy
from collections import defaultdict

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Define the input CSV file name
input_file = 'tribune_14_18.csv'

# Define the output directory where .txt files will be saved
output_directory = 'output_titles/'

# Create a dictionary to store titles for each year
titles_by_year = defaultdict(list)

# Read the CSV file and extract titles for each year
with open(input_file, 'r', encoding = "utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        date_parts = row['date'].split('-')
        year = date_parts[2]  # Extract the year part from the date
        titles_by_year[year].append(row['title'])

# Process and extract titles using spaCy
for year, titles in titles_by_year.items():
    output_file_path = output_directory + f'titles_{year}.txt'
    with open(output_file_path, 'w', encoding = "utf-8") as txtfile:
        for title in titles: 
            txtfile.write(f"{title}\n")
    print(f"Titles for the year {year} have been written to {output_file_path}")

