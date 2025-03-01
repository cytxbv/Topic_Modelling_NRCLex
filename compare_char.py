from nrclex import NRCLex
import os
import pandas as pd
import matplotlib.pyplot as plt


character_name = "Sally"  

dialogue_dir = f"output_titles/sally_diag"


def get_emotions(text):
    emotion = NRCLex(text).affect_frequencies 

    if "anticipation" in emotion and "anticip" in emotion:
        del emotion["anticip"]

    return emotion


emotion_results = {}

for filename in sorted(os.listdir(dialogue_dir)):  
    if filename.endswith(".txt"):
        book_name = filename.replace(".txt", "").replace(character_name.lower(), "").replace("_", " ").strip()
        file_path = os.path.join(dialogue_dir, filename)
        
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            emotions = get_emotions(text)


        emotion_results[book_name] = emotions


emotion_df = pd.DataFrame.from_dict(emotion_results, orient='index')

csv_filename = f"{character_name.lower()}_emotions_series.csv"
emotion_df.to_csv(csv_filename, encoding="utf-8")
print(f"{character_name}'s emotion results saved to {csv_filename}")

plt.figure(figsize=(12, 6))

for emotion in emotion_df.columns:
    plt.plot(emotion_df.index, emotion_df[emotion], marker='o', label=emotion)

plt.title(f"{character_name}'s Emotion Trends Across the Series")
plt.xlabel("Books")
plt.ylabel("Emotion Score")
plt.xticks(rotation=45)
plt.legend(title="Emotions", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.7)

graph_filename = f"{character_name.lower()}_emotion_series.png"
plt.savefig(graph_filename, bbox_inches="tight")
plt.show()

print(f"Emotion trends graph saved as {graph_filename}")
