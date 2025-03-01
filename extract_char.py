import os
import spacy
from collections import defaultdict

nlp = spacy.load("en_core_web_sm")

directory = 'output_titles/series_diag'

character_dialogues = defaultdict(list)

character_names = [
    "Sally"
]

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            text = file.read()

            doc = nlp(text)
            
            current_character = None
            
            for sent in doc.sents:

                for ent in sent.ents:
                    if ent.label_ == "PERSON":
                        character = ent.text.strip()
                       
                        if character in character_names:
                            current_character = character

                if current_character:
                    dialogue = sent.text.strip()  
                    character_dialogues[current_character].append(dialogue)


for character, dialogues in character_dialogues.items():

    output_file_path = f"output_titles/{character.replace(' ', '_')}_dialogues.txt"  
    with open(output_file_path, 'w', encoding='utf-8') as txtfile:
        for dialogue in dialogues:
            txtfile.write(f"{dialogue}\n")  
    print(f"Dialogues for {character} have been written to {output_file_path}")
