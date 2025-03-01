import os
import re

input_dir = "output_titles/series_diag"
output_dir = "output_titles/percy_diag"


os.makedirs(output_dir, exist_ok=True)


# dialogue_pattern = r'“(.*?)”'  
dialogue_pattern = r'[“"](.*?)[”"]'



def extract_dialogue(book_text):
    return re.findall(dialogue_pattern, book_text)

for filename in sorted(os.listdir(input_dir)): 
    if filename.endswith(".txt"):
        file_path = os.path.join(input_dir, filename)
        
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            dialogues = extract_dialogue(text) 
        
        
        percy_dialogue_file = os.path.join(output_dir, filename)
        with open(percy_dialogue_file, "w", encoding="utf-8") as output_file:
            output_file.write("\n".join(dialogues))
        
        print(f"Extracted Percy's dialogue from {filename} and saved to {percy_dialogue_file}")
