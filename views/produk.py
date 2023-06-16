import streamlit as st
from conn import Database


class Produk:
    class Model:
        title = "### Data Produk"

    def view(self, model):

        with st.container():
            st.write("#### Data Produk")
            db = Database()
            query2 = "SELECT nama AS Nama, bintang5 AS 'Bintang 5', bintang4 AS 'Bintang 4', bintang3 AS 'Bintang 3', bintang2 AS 'Bintang 2', bintang1 AS 'Bintang 1' FROM produk"
            df = db.query(query2)
            st.dataframe(df, width=3000, hide_index = True)
