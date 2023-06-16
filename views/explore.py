import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from streamlit_echarts import st_pyecharts, st_echarts
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from conn import Database
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

class Explore:
    class Model:
        title = "### Explore Data"

    def view(self, model):

        with st.form(key='my_form'):
            # Default values
            default_start_date = datetime.now() - timedelta(days=30)
            default_end_date = datetime.now()
            default_option = ["bintang 1", "bintang 2", "bintang 3", "bintang 4", "bintang 5"]
            rating_colors = {"bintang 1": "red", "bintang 2": "yellow", "bintang 3": "orange", "bintang 4": "blue", "bintang 5": "green"}

            start_date, end_date = st.date_input("Pilih Rentang Tanggal:", (default_start_date, default_end_date))
            selected_ratings = st.multiselect("Pilih Rating Bintang", ["bintang 1", "bintang 2", "bintang 3", "bintang 4", "bintang 5"], default=default_option)
            
            submit_button = st.form_submit_button(label='Submit')

        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("#### Line Plot")

                if submit_button:
                    db = Database()

                    start_date_str = start_date.strftime('%Y-%m-%d')
                    end_date_str = end_date.strftime('%Y-%m-%d')

                    selected_ratings_str = ', '.join([f"'{rating}'" for rating in selected_ratings])

                    query = f"SELECT tanggal_convert AS tanggal, rating, COUNT(*) as counts FROM reviews WHERE tanggal_convert BETWEEN '{start_date_str}' AND '{end_date_str}' AND rating IN ({selected_ratings_str}) GROUP BY tanggal_convert, rating ORDER BY tanggal_convert ASC"
                    
                    rows = db.query(query)
                    print(query)
                    df = pd.DataFrame(rows, columns=['tanggal', 'rating', 'counts'])

                    # Prepare data for echarts
                    echarts_data = []
                    for rating in df['rating'].unique():
                        df_rating = df[df['rating'] == rating]
                        echarts_data.append({"name": rating, "type": "line", "data": df_rating['counts'].tolist(), "itemStyle": {"color": rating_colors[rating]}})

                    # Create echarts
                    # Create echarts
                    option = {
                        "tooltip": {"trigger": "axis"},
                        "legend": {"data": df['rating'].unique().tolist()},
                        "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
                        "toolbox": {"feature": {"saveAsImage": {}}},
                        "xAxis": {"type": "category", "boundaryGap": False, "data": df['tanggal'].astype(str).unique().tolist()},
                        "yAxis": {"type": "value"},
                        "series": echarts_data
                    }


                    st_echarts(options=option, height="400px")
            
            with col2:
                st.write("#### Word Cloud")

                if submit_button:
                    query2 = f"SELECT review_cleansing FROM reviews WHERE LENGTH(review_asli) > 0 AND tanggal_convert BETWEEN '{start_date_str}' AND '{end_date_str}' AND rating IN ({selected_ratings_str})"
                    df = db.query(query2)
                    review_cleansing = ' '.join(clean_text(review) for review in df['review_cleansing'])

                    df = db.query('SELECT kata from stopwords')
                    kata_stopwords = set(kata.lower() for kata in df['kata'])
                    kata_stopwords.add('tidak')
                    kata_stopwords.add('saya')

                    wc = WordCloud(background_color="white", collocations=False, max_words=100, stopwords=kata_stopwords, max_font_size=256, random_state=42, width=800, height=300)
                    word_frequencies = wc.process_text(review_cleansing)

                    filtered_word_frequencies = {word: freq for word, freq in word_frequencies.items() if freq > 3}

                    wc.generate_from_frequencies(filtered_word_frequencies)
                    plt.imshow(wc, interpolation="bilinear")
                    plt.axis('off')
                    st.pyplot(plt)

          
            st.markdown("---")

        with st.container():
            if submit_button:
                st.write("#### Raw Data")
                query2 = f"SELECT tanggal_convert AS Tanggal, nama_produk AS Produk, review_asli AS Review, rating AS Rating FROM reviews WHERE LENGTH(review_asli) > 0 AND tanggal_convert BETWEEN '{start_date_str}' AND '{end_date_str}' AND rating IN ({selected_ratings_str}) ORDER BY tanggal_convert ASC"
                df = db.query(query2)
                st.dataframe(df, width=3000, hide_index = True)
