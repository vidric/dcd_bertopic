import streamlit as st
from bertopic import BERTopic

class HasilModel:
    class Model:
        title = "### BERTopic"

    def view(self, model):

        with st.container():
            st.markdown("<h1 style='text-align: center; color: black; font-weight: bold;'>Topic Modelling Customer Review Parfum HMNS Menggunakan BERTopic</h1>", unsafe_allow_html=True)

        with st.container():
            df = db.query('SELECT review_asli AS Review, rating AS Rating from reviews WHERE LENGTH(review_asli) > 0 ORDER BY tanggal_convert DESC LIMIT 10')
            st.dataframe(df, width=1000, hide_index = True)
          
            st.markdown("---")


