import streamlit as st
from pypdf import PdfReader
from docx import Document
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize

# Download nltk punkt tokenizer if needed
nltk.download('punkt')

st.title("Multi-Visualization Text Analytics App")

uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=['pdf', 'docx'])

def extract_text(file):
    if file.type == "application/pdf":
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    else:
        return None

if uploaded_file:
    text = extract_text(uploaded_file)
    if not text:
        st.error("Could not extract text from the document.")
    else:
        st.subheader("Extracted Text")
        st.text_area("Text", text, height=300)

        words = text.split()
        if words:
            word_freq = Counter(words)
            most_common = word_freq.most_common(10)
            words_top, counts = zip(*most_common)

            # 1. Bar chart
            plt.figure(figsize=(10,5))
            plt.bar(words_top, counts, color='skyblue')
            plt.xticks(rotation=45)
            plt.xlabel("Words")
            plt.ylabel("Frequency")
            plt.title("Top 10 Most Frequent Words")
            st.pyplot(plt)
            plt.clf()

            # 2. Word Cloud
            wc = WordCloud(width=800, height=400, background_color='white').generate(text)
            plt.figure(figsize=(10,5))
            plt.imshow(wc, interpolation='bilinear')
            plt.axis('off')
            plt.title("Word Cloud")
            st.pyplot(plt)
            plt.clf()

            # 3. Pie chart of word length categories
            short_words = sum(1 for w in words if len(w) <= 3)
            medium_words = sum(1 for w in words if 4 <= len(w) <= 7)
            long_words = sum(1 for w in words if len(w) > 7)
            labels = ['Short (<=3 chars)', 'Medium (4-7 chars)', 'Long (>7 chars)']
            sizes = [short_words, medium_words, long_words]
            colors = ['lightcoral', 'gold', 'lightskyblue']
            plt.figure(figsize=(6,6))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
            plt.title("Word Length Distribution")
            st.pyplot(plt)
            plt.clf()


        else:
            st.info("No words found to visualize.")
