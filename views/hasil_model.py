import matplotlib.pyplot as plt
import streamlit as st
from bertopic import BERTopic
from conn import Database

class HasilModel:
    class Model:
        title = "### BERTopic"

    def view(self, model):

        with st.container():
            db = Database()
            st.markdown("<h1 style='text-align: center; color: black; font-weight: bold;'>Hasil Model BERTopic</h1>", unsafe_allow_html=True)

            df = db.query('SELECT * FROM v_cluster_rating WHERE jumlah_rating_5 < 30000 ORDER BY jumlah_total_rating DESC')
            df.set_index('nama_cluster', inplace=True)

            # Buat stacked bar plot
            kolom_dipilih = ['jumlah_rating_1', 'jumlah_rating_2', 'jumlah_rating_3', 'jumlah_rating_4', 'jumlah_rating_5']
            df_sorted = df.sort_values(by='jumlah_total_rating', ascending=False)
            ax = df[kolom_dipilih].plot(kind='bar', stacked=True, figsize=(10, 7))
            
            plt.title("Jumlah Rating untuk setiap Topik")
            plt.xlabel("Nama Topik")
            plt.ylabel("Jumlah Rating")
            
            # Tampilkan plot di Streamlit
            st.pyplot(plt)
          
            st.markdown("---")
            
        with st.form(key='my_form'):
            default_option = ["kemasan", "kebanggaan", "hadiah", "edisi hmns", "pengiriman", "respon pasangan", "admin", "starterpack", "repeat order", "bonus", "daya tahan", "eos", "kartu ucapan", "tester"]
            selected_ratings = st.multiselect("Pilih Topik", ["kemasan", "kebanggaan", "hadiah", "edisi hmns", "pengiriman", "respon pasangan", "admin", "starterpack", "repeat order", "bonus", "daya tahan", "eos", "kartu ucapan", "tester"], default=default_option)
            
            submit_button = st.form_submit_button(label='Submit')
