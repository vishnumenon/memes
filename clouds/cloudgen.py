from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import json

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# Loop through memes
for meme in ["rickroll"]: #["aesthetic", "emoji", "nessie", "obama", "ratings", "rickroll", "switcharoo", "wot"]:
    allText = ""

    # Aggregate all bodies for the meme into one string
    for line in open(meme+".json"):
        # Add body to variable
        allText += json.loads(line)["body"] + " "

    # Print status update
    print("Done reading")
    # Load mask image
    mask = np.array(Image.open(meme+".png"))
    # Create stopword set and add new stopwords for specific meme
    stopwords = set(STOPWORDS)
    stopwords.update(["youtube", "dQw4w9WgXcQ"])

    # Load colormap for WC
    image_colors = ImageColorGenerator(mask)

    # Generate word cloud for allText with specified color and shape masks
    wc = WordCloud(background_color=None, mode="RGBA", color_func=image_colors, max_words=1000, mask=mask, stopwords=stopwords)
    wc.generate(allText)
    # Write to file
    wc.to_file(meme+"-cloud.png")
