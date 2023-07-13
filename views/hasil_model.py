import streamlit as st
from bertopic import BERTopic

class HasilModel:
    class Model:
        title = "### BERTopic"

    def view(self, model):

        with st.container():
            st.markdown("<h1 style='text-align: center; color: black; font-weight: bold;'>Topic Modelling Customer Review Parfum HMNS Menggunakan BERTopic</h1>", unsafe_allow_html=True)

        with st.container():
            st.info('BERTopic adalah topic modelling yang menggabungkan model transformer dengan algoritma clustering untuk menentukan topik-topik dari sebuah dokumen.')
            st.markdown(
                """
                <div style="background-color:#ADD8E6; padding:10px; border-radius:5px;">
                Beberapa model dan algoritma yang digunakan dalam BERTopic antara lain :
                <br> - <b>Model Transformer:</b> Ini merupakan bagian utama dari BERTopic. Model ini digunakan untuk menghasilkan representasi vektor dari teks, yang kemudian digunakan dalam proses clustering. BERTopic mendukung berbagai jenis model transformer seperti BERT, RoBERTa, DistilBERT, dan banyak lagi.
                <br> - <b>UMAP (Uniform Manifold Approximation and Projection):</b> UMAP adalah algoritma pengurangan dimensi yang digunakan untuk mengurangi dimensi dari representasi vektor yang dihasilkan oleh model transformer. Tujuannya adalah untuk mempertahankan struktur topologis data sembari mengurangi kompleksitasnya.
                <br> - <b>HDBSCAN (Hierarchical Density-Based Spatial Clustering of Applications with Noise):</b> Setelah UMAP digunakan untuk pengurangan dimensi, HDBSCAN digunakan untuk mengelompokkan vektor dalam ruang berdimensi lebih rendah. HDBSCAN adalah algoritma clustering berbasis kerapatan yang mampu mendeteksi cluster dengan berbagai bentuk dan ukuran.
                <br> - <b>Class-based TF-IDF:</b> Setelah proses clustering, BERTopic menggunakan teknik Class-based TF-IDF untuk mengekstraksi kata-kata yang paling mewakili setiap topik. Dengan ini, kita dapat menginterpretasikan topik-topik yang ditemukan oleh model.
                <br>
                </div>
                """, 
                unsafe_allow_html=True
                )
            st.markdown("")


