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

        with st.container():
            st.write("## Langkah 1 : Sumber Data")
            st.info('Data review berasal dari E-Commerce Tokopedia. Diperoleh dengan cara metode web scraping. Disimpan ke dalam database MySQL.')

        with st.container():
            st.write("## Langkah 2 : Data Cleansing")
            st.markdown(
                """
                <div style="background-color:#ADD8E6; padding:10px; border-radius:5px;">
                Sebelum masuk ke tahap model, data review dicleansing dengan cara : 
                <br> - Cek bahasa. Apabila bahasa inggris, terjemahkan ke bahasa Indonesia.
                <br> - Hapus huruf berulang. Seperti maaaniisss menjadi manis.
                <br> - Ubah typo atau kata tertentu dengan cara konversi kata. Dimana telah tersedia kata yang perlu dikonversi di dalam database.
                <br> - Gabungkan 2 kata tertentu seperti: terima kasih menjadi terimakasih, starter pack menjadi starterpack.
                <br>
                </div>
                """, 
                unsafe_allow_html=True
                )
            st.markdown("")
            st.write("Code:")
            code = """
            #ubah ke huruf kecil
            review_asli = review_asli.lower()

            # terjemahkan ke indonesia 
            if detect(review_asli) == 'en':
                translation = Translator.translate(review_asli, src='en', dest='id')
                review_indonesia = translation.text
            else:
                review_indonesia = review_asli
            
            # hapus huruf berulang
            review = re.sub(r'(.)\1{1,}', r'\1', review_indonesia)

            # cek typo dan ubah ke kata dasar
            review_split = review.split()
            words = [conversion_dict[word] if word in conversion_dict else word for word in review_split]
            review_cleansing = ' '.join(words)

            review_cleansing = review_cleansing.replace("terima kasih", "terimakasih")
            review_cleansing = review_cleansing.replace("starter pack", "starterpack")
            """
            st.code(code, language='python')

        
        with st.container():
            st.write("## Langkah 3 : Model BERTopic")
        
            code3 = """
            topic_model = BERTopic(language="indonesian",calculate_probabilities=True)
            """
            st.code(code3, language="python")
            st.info('Model ini menghasilkan sekitar 280 topik. Dan topik- topik tersebut tidak tercluster dengan baik.')
        
        with st.container():
            st.write("## Langkah 4 : Topic Reduction")
            st.info('Kita melakukan Topic Reduction dengan code sebagai berikut :')
            code4 = """
            # Initiate UMAP
            umap_model = UMAP(n_neighbors=15, 
                  n_components=5, 
                  min_dist=0.0, 
                  metric='cosine', 
                  random_state=109)
                  
            topic_model = BERTopic(umap_model=umap_model, language="indonesian", calculate_probabilities=True, nr_topics="auto")

            topics, probs = topic_model.fit_transform(reviews_fit)
            # simpan model
            topic_model.save("model_bertopic_hmns_reduce_topic_auto_final")
            
            doc_topic_tuples = []
            
            # mapping setiap review akan masuk ke topic apa saja
            for doc_id, doc_prob in zip(id_to_review_mapping.keys(), probs):
                
                topic_prob_tuples = [(int(topic), float(prob)) for topic, prob in enumerate(doc_prob) if prob > 0.001]
                sorted_topic_prob_tuples = sorted(topic_prob_tuples, key=lambda x: x[1], reverse=True)
                sorted_topics = [topic for topic, _ in sorted_topic_prob_tuples]
                
                doc_topic_tuples.append((int(doc_id), id_to_review_mapping[doc_id], sorted_topics))

            topic_info = topic_model.get_topic_info()
            nama_file_json = 'topic_info_reduce_auto_final.json'
            topic_info.to_json(nama_file_json, orient='records')
            
            filename = "doc_topic_tuples_fix_reduce_topic_auto_final.csv"
            
            #disimpan ke dalam file csv
            with open(filename, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['id_dokumen', 'dokumen', 'topic_ids'])
            
            for row in doc_topic_tuples:
                csvwriter.writerow([row[0], row[1], ','.join(map(str, row[2]))])
            """
            st.code(code4, language="python")
            st.info('Menghasilkan 67 topik. Dan terlihat topik- topik tersebut tercluster dengan baik.')
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("#### Model BERTopic")
                topic_model_before = BERTopic.load("vidric/bertopic_before_tuning")

                
                # Visualize Topics
                fig = topic_model_before.visualize_topics()

                # Show the plot in Streamlit
                st.plotly_chart(fig)
            
            with col2:
                st.write("#### BERTopic Dengan Topic Reduction")
                topic_model_after = BERTopic.load("vidric/bertopic_after_tuning")

                # Visualize Topics
                fig = topic_model_after.visualize_topics()

                # Show the plot in Streamlit
                st.plotly_chart(fig)
          
            st.markdown("---")
            
        with st.container():
            st.write("## Langkah 5 : Clustering")
        
            st.info('Kita melakukan clustering atas 67 model yang dihasilkan, ke dalam 15 cluster. Yakni Kualitas, Kemasan, Admin, Kebanggaan, Respon Pasangan, Repeat Order, dan seterusnya. Proses ini dilakukan secara manual.')
