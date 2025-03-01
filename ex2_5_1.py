from nrclex import NRCLex
import os
import pandas as pd
import matplotlib.pyplot as plt

directory = 'output_titles/pc_diag'

def get_emotions(text):
    emotion = NRCLex(text)
    return emotion.affect_frequencies 

emotion_results = {}

for filename in sorted(os.listdir(directory)):  
    if filename.endswith(".txt"):
        file_path = os.path.join(directory, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            emotions = get_emotions(text)
            emotion_results[filename] = emotions  

df = pd.DataFrame(emotion_results).T 

df.fillna(0, inplace=True)

csv_filename = "series_analysis.csv"
df.to_csv(csv_filename, encoding="utf-8")
print(f"Emotion results saved to {csv_filename}")

plt.figure(figsize=(12, 6))
for emotion in df.columns:
    plt.plot(df.index, df[emotion], marker='o', label=emotion)

plt.title("Emotion Trends Thoughout the Series's Dialogue")
plt.xlabel("Dialogue Files")
plt.ylabel("Emotion Score")
plt.xticks(rotation=45, ha='right')
plt.legend(title="Emotions", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.7)

graph_filename = "series_trends.png"
plt.savefig(graph_filename, bbox_inches="tight")
plt.show()

print(f"Emotion trends graph saved as {graph_filename}")
