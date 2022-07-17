import tkinter as tk
from tkinter import *
import tkinter.messagebox
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from tkinter.ttk import *
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob
import time
from wordcloud import WordCloud, STOPWORDS
from nltk.tokenize import word_tokenize

# Progress Bar
def ProcessBarAni():
    Progress_Bar['value'] = 20
    m.update_idletasks()
    time.sleep(1)
    Progress_Bar['value'] = 50
    m.update_idletasks()
    time.sleep(1)
    Progress_Bar['value'] = 80
    m.update_idletasks()
    time.sleep(1)
    Progress_Bar['value'] = 100

# Donut Chart
def piech(score):
    if score > 0:
        y = np.array([score, (1 - score)])
        explode = (0.05, 0.05)
        mylabels = ["Good", "Bad"]
        plt.pie(y, labels=mylabels, shadow=True, startangle=90, autopct='%1.1f%%', pctdistance=0.85, explode=explode)
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.legend(mylabels, loc="best")
        plt.show()
    elif score < 0:
        y = np.array([1 - (score * (-1)), (score * (-1))])
        mylabels = ["Good", "Bad"]
        plt.pie(y, labels=mylabels, shadow=True, startangle=90)
        plt.legend(mylabels, loc="best")
        plt.show()
    else:
        y = np.array([.5, 0.5])
        mylabels = ["Good", "Bad"]
        plt.pie(y, labels=mylabels, shadow=True, startangle=90)
        plt.legend(mylabels, loc="best")
        plt.show()

# WordCloud
def wordcloudImg(x1):
    try:
        wordcloud = WordCloud(width=800, height=800,
                              background_color='white',
                              stopwords=STOPWORDS,
                              min_font_size=10).generate(x1)
        plt.axis("off")
        plt.imshow(wordcloud)

    except:
        wordcloud = WordCloud(width=800, height=800,
                              background_color='white',
                              stopwords=STOPWORDS,
                              min_font_size=10).generate("Missing string argument")
        plt.axis("off")
        plt.imshow(wordcloud)

#Email sumarizer
def sumarizerfn(x1):
    try:
        text = x1
        stopWords = set(stopwords.words("english"))
        words = word_tokenize(text)
        # Creating a frequency table to keep the
        # score of each word
        freqTable = dict()
        for word in words:
            word = word.lower()
            if word in stopWords:
                continue
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1
        # Creating a dictionary to keep the score
        # of each sentence
        sentences = sent_tokenize(text)
        sentenceValue = dict()
        for sentence in sentences:
            for word, freq in freqTable.items():
                if word in sentence.lower():
                    if sentence in sentenceValue:
                        sentenceValue[sentence] += freq
                    else:
                        sentenceValue[sentence] = freq
        sumValues = 0
        for sentence in sentenceValue:
            sumValues += sentenceValue[sentence]
        # Average value of a sentence from the original text
        average = int(sumValues / len(sentenceValue))
        # Storing sentences into our summary.
        summary = ''
        for sentence in sentences:
            if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
                summary += " " + sentence

        return summary
    except:
        return "No string found"

# String filtering without stopwords
def remove_mystopwords(sentence):
    text_tokens = word_tokenize(sentence)
    tokens_filtered = [word for word in text_tokens if not word in STOPWORDS]
    return (" ").join(tokens_filtered)

#Tkinter main
m = tk.Tk()
m.title('Text Analysis')
canvas1 = tk.Canvas(m, width=400, height=500, bg='black')
canvas1.pack()
Progress_Bar = Progressbar(m, orient=HORIZONTAL, length=350, mode='determinate')
entry1 = Text(m)
canvas1.create_window(202, 240, width=360, height=430, window=entry1)

#Main operational function
def homeInt():
    x1 = entry1.get("1.0", 'end-1c')

    filtered_text = remove_mystopwords(x1)
    # print(filtered_text)
    score = TextBlob(filtered_text).sentiment.polarity
    # print(score)

    # Progress bar animation
    ProcessBarAni()

    # Email summary pop-up
    summary = sumarizerfn(x1)
    tkinter.messagebox.showinfo("Email summary", summary)

    # WordCloud
    plt.figure("Word distribution")
    wordcloudImg(x1)

    # Pie chart
    plt.figure("Sentiment Analysis")
    piech(score)
    plt.show()


Progress_Bar.pack()
button1 = tk.Button(text='Evaluate', command=homeInt, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 480, width=300, window=button1)

m.mainloop()

