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
            st.markdown("<h1 style='text-align: center; color: black; font-weight: bold;'>Topic Modelling Customer Review Parfum HMNS Menggunakan BERTopic</h1>", unsafe_allow_html=True)

            df = db.query('SELECT * FROM v_cluster_rating ORDER BY jumlah_total_rating DESC')
            df.set_index('nama_cluster', inplace=True)

            # Buat stacked bar plot
            kolom_dipilih = ['jumlah_rating_1', 'jumlah_rating_2', 'jumlah_rating_3', 'jumlah_rating_4', 'jumlah_rating_5']
            df_sorted = df.sort_values(by='jumlah_total_rating', ascending=False)
            ax = df[kolom_dipilih].plot(kind='bar', stacked=True, figsize=(10, 7))
            
            plt.title("Jumlah Rating untuk setiap Cluster")
            plt.xlabel("Nama Cluster")
            plt.ylabel("Jumlah Rating")
            plt.yscale('log')
            
            # Tampilkan plot di Streamlit
            st.pyplot(plt)
          
            st.markdown("---")
