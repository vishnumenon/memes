from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import json

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

for meme in ["rickroll"]: #["aesthetic", "emoji", "nessie", "obama", "ratings", "rickroll", "switcharoo", "wot"]:
    allText = ""
    lines = 0
    for line in open(meme+".json"):
        allText += json.loads(line)["body"] + " "
        lines += 1
        if lines > 10000:
            break
    print("Done reading")
    mask = np.array(Image.open(meme+".png"))
    stopwords = set(STOPWORDS)
    stopwords.update(["youtube", "dQw4w9WgXcQ"])

    image_colors = ImageColorGenerator(mask)

    wc = WordCloud(background_color=None, mode="RGBA", color_func=image_colors, max_words=1000, mask=mask, stopwords=stopwords)
    wc.generate(allText)
    wc.to_file(meme+"-cloud.png")
