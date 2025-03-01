from nrclex import NRCLex
import os
import pandas as pd
import matplotlib.pyplot as plt


annabeth_dir = "output_titles/annabeth_diag"
percy_dir = "output_titles/percy_diag"


def get_emotions(text):
    emotion = NRCLex(text)
    return emotion.affect_frequencies  


def process_character(directory, prefix):
    emotion_results = {}

    for filename in sorted(os.listdir(directory)):  
            
            book_name = filename.replace(".txt", "").replace("annabeth", "").replace("percyjackson", "").strip()
            file_path = os.path.join(directory, filename)
            
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                emotions = get_emotions(text)
                if "anticipation" in emotions and "anticip" in emotions:
                    del emotions["anticip"]
            
            
            emotion_results[book_name] = emotions

    df = pd.DataFrame.from_dict(emotion_results, orient='index')

    print(f"Processed books in {directory}: {list(df.index)}")
    
    return df.add_prefix(prefix) 


annabeth_df = process_character(annabeth_dir, "")
percy_df = process_character(percy_dir, "")

common_books = set(annabeth_df.index).intersection(set(percy_df.index))
annabeth_df = annabeth_df.loc[list(common_books)]
percy_df = percy_df.loc[list(common_books)]

emotion_comparison = pd.concat([annabeth_df, percy_df], axis=1)


csv_filename = "percy_annabeth_emotions.csv"
emotion_comparison.to_csv(csv_filename, encoding="utf-8")
print(f"Emotion comparison saved to {csv_filename}")


for book in common_books:
    plt.figure(figsize=(12, 6))


    annabeth_emotions = annabeth_df.loc[book]
    percy_emotions = percy_df.loc[book]


    bar_width = 0.4
    x_labels = annabeth_emotions.index
    x = range(len(x_labels))


    plt.bar(x, annabeth_emotions, width=bar_width, label="Annabeth", align='center')
    plt.bar([i + bar_width for i in x], percy_emotions, width=bar_width, label="Percy", align='center')

    plt.title(f"Emotion Comparison in {book.title()}")
    plt.xlabel("Emotions")
    plt.ylabel("Emotion Score")
    plt.xticks([i + bar_width / 2 for i in x], x_labels, rotation=45)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)


    graph_filename = f"{book}_emotion_comparison.png"
    plt.savefig(graph_filename, bbox_inches="tight")
    plt.show()

    print(f"Emotion comparison graph saved as {graph_filename}")