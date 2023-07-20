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

            df = db.query('SELECT * FROM v_cluster_rating')
            df.set_index('nama_cluster', inplace=True)

            # Buat stacked bar plot
            ax = df.plot(kind='bar', stacked=True, figsize=(10, 7))
            
            plt.title("Jumlah Rating untuk setiap Cluster")
            plt.xlabel("Nama Cluster")
            plt.ylabel("Jumlah Rating")
            
            # Tampilkan plot di Streamlit
            st.pyplot(plt)
          
            st.markdown("---")
