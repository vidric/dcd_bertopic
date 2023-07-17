import streamlit as st
import numpy as np
import pandas as pd
import json
import altair as alt
from pathlib import Path
import requests
from conn import Database
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

class Dashboard:
    class Model:
        pageTitle = "Dashboard"

        wordsTitle = "Jumlah Review"

        inferenceTimeTitle = "Jumlah Rating"

        documentsTitle = "Jumlah Produk"

        dailyInferenceTitle = "Jumlah Topik"

        accuracyTitle = "Akumulasi Rating"

        titleModelEval = "## Evaluation Accuracy"
        titleInferencePerformance = "#### Word Cloud Semua Review"
        titleDatasetInfo = "## Dataset Info"
        titleDataAnnotation = "## Data Annotation"
        titleTrainingPerformance = "## Training Performance"
        titleEvaluationPerformance = "## Evaluation Performance"

    def view(self, model):
        # st.title(model.pageTitle)

        with st.container():
            col1, col2, col3, col4, col5 = st.columns(5)

            db = Database()

            with col1:
                df = db.query('SELECT COUNT(id) from reviews')
                jumlah_review = df.iloc[0,0]
                jumlah_review = "{:,.0f}".format(jumlah_review).replace(",", " ").replace(".", ",").replace(" ", ".")
                st.metric(label=model.wordsTitle, value=jumlah_review)

            with col2:
                df = db.query('SELECT COUNT(id) from produk')
                jumlah_produk = df.iloc[0,0]
                jumlah_produk = "{:,.0f}".format(jumlah_produk).replace(",", " ").replace(".", ",").replace(" ", ".")
                st.metric(label=model.documentsTitle, value=jumlah_produk)

            with col3:
                df = db.query('SELECT COUNT(id) from cluster')
                jumlah_topik = df.iloc[0,0]
                jumlah_topik = "{:,.0f}".format(jumlah_topik).replace(",", " ").replace(".", ",").replace(" ", ".")
                st.metric(label=model.dailyInferenceTitle, value=jumlah_topik)

            with col4:
                df = db.query('SELECT SUM(bintang5 + bintang4 + bintang3 + bintang2 + bintang1) as total_bintang FROM produk')
                jumlah_rating = df.iloc[0,0]
                jumlah_rating = "{:,.0f}".format(jumlah_rating).replace(",", " ").replace(".", ",").replace(" ", ".")
                st.metric(label=model.inferenceTimeTitle, value=jumlah_rating)

            with col5:
                df = db.query('SELECT (SUM(bintang5) * 5 + SUM(bintang4) * 4 + SUM(bintang3) * 3 + SUM(bintang2) * 2 + SUM(bintang1)) / (SUM(bintang5 + bintang4 + bintang3 + bintang2 + bintang1)) AS rata_rata_rating FROM produk')
                akumulasi_rating = df.iloc[0,0]
                akumulasi_rating = "{:,.2f}".format(akumulasi_rating).replace(".", " ").replace(".", ",").replace(" ", ",")
                st.metric(label=model.accuracyTitle, value=str(akumulasi_rating) + ' / 5')

            st.markdown("---")


        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(model.titleInferencePerformance)

                df = db.query('SELECT review_cleansing from reviews')
                review_cleansing = ' '.join(clean_text(review) for review in df['review_cleansing'])

                df = db.query('SELECT kata from stopwords')
                kata_stopwords = set(kata.lower() for kata in df['kata'])
                kata_stopwords.add('tidak')

                wc = WordCloud(background_color="white", collocations=False, max_words=100, stopwords=kata_stopwords, max_font_size=256, random_state=42, width=800, height=300)
                word_frequencies = wc.process_text(review_cleansing)

                filtered_word_frequencies = {word: freq for word, freq in word_frequencies.items() if freq > 10}

                wc.generate_from_frequencies(filtered_word_frequencies)
                plt.imshow(wc, interpolation="bilinear")
                plt.axis('off')
                st.pyplot(plt)
            
            with col2:

                df = db.query("SELECT review_cleansing from reviews WHERE rating IN ('bintang 1', 'bintang 2')")
                total_rows = len(df)
                review_cleansing = ' '.join(clean_text(review) for review in df['review_cleansing'])

                st.write("### Word Cloud Semua Review Rating 1 & 2" + "( " + str(total_rows) + " Review )")

                df = db.query('SELECT kata from stopwords')
                kata_stopwords = set(kata.lower() for kata in df['kata'])
                kata_stopwords.add('tidak')
                kata_stopwords.add('saya')
                kata_stopwords.add('parfum')
                kata_stopwords.add('wangi')
                kata_stopwords.add('sudah')
                kata_stopwords.add('aku')
                kata_stopwords.add('ada')
                kata_stopwords.add('saja')
                kata_stopwords.add('tapi')
                kata_stopwords.add('dengan')

                wc = WordCloud(background_color="white", colormap='Paired', collocations=False, max_words=100, stopwords=kata_stopwords, max_font_size=256, random_state=42, width=800, height=300)
                word_frequencies = wc.process_text(review_cleansing)

                filtered_word_frequencies = {word: freq for word, freq in word_frequencies.items() if freq > 5}

                wc.generate_from_frequencies(filtered_word_frequencies)
                plt.imshow(wc, interpolation="bilinear")
                plt.axis('off')
                st.pyplot(plt)
          
            st.markdown("---")
        
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("#### 10 Review Terakhir")

                df = db.query('SELECT review_asli AS Review, rating AS Rating from reviews WHERE LENGTH(review_asli) > 0 ORDER BY tanggal_convert DESC LIMIT 10')
                st.dataframe(df, width=1000, hide_index = True)
                
            
            with col2:
                st.write("#### 10 Review Terakhir Rating 1 & 2")

                df = db.query("SELECT review_asli AS Review, rating AS Rating from reviews WHERE rating IN ('bintang 1', 'bintang 2') AND LENGTH(review_asli) > 0 ORDER BY tanggal_convert DESC LIMIT 10")
                st.dataframe(df, width=1000, hide_index = True)
          
            st.markdown("---")
            
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("#### List Product")

                df = db.query('SELECT * from produk')
                df['nama'] = df.apply(lambda x: f'<a href="https://bertopic.streamlit.app/product/{x.id}">{x.nama}</a>', axis=1)
                df = df.drop(columns=['id'])
                df.set_index('nama', inplace=True)  # Ubah kolom 'nama' menjadi indeks
                st.write(df.to_html(escape=False, index=True), unsafe_allow_html=True)
            
            with col2:
                st.write("#### List Topik")

                df = db.query("SELECT nama from cluster")
                st.dataframe(df, width=1000, hide_index = True)
          
            st.markdown("---")
