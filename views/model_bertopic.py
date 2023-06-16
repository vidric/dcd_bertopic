import streamlit as st
from bertopic import BERTopic

class ModelBertopic:
    class Model:
        title = "### BERTopic"

    def view(self, model):

        with st.container():
            st.markdown("<h1 style='text-align: center; color: black; font-weight: bold;'>Topic Modelling Customer Review Parfum HMNS Menggunakan BERTopic</h1>", unsafe_allow_html=True)

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
            topic_model = BERTopic(language="id", embedding_model="distiluse-base-multilingual-cased", calculate_probabilities=True)
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
            st.code(code3, language="python")
            st.info('Model ini menghasilkan sekitar 280 topik. Dan topik- topik tersebut tidak tercluster dengan baik.')
        
        with st.container():
            st.write("## Langkah 4 : Topic Reduction")
            st.info('Kita melakukan Topic Reduction dengan code sebagai berikut :')
            code4 = """
            topic_model = BERTopic(language="id", embedding_model="distiluse-base-multilingual-cased", calculate_probabilities=True, nr_topics="auto")
            """
            st.code(code4, language="python")
            st.info('Menghasilkan 38 topik. Dan terlihat topik- topik tersebut tercluster dengan baik.')
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("#### Model BERTopic")
                #topic_model_before = BERTopic.load("model/model_bertopic_hmns_before_reduce")
                topic_model_before = BERTopic.load("vidric/bertopic_dcd")

                
                # Visualize Topics
                fig = topic_model_before.visualize_topics()

                # Show the plot in Streamlit
                st.plotly_chart(fig)
            
            with col2:
                st.write("#### BERTopic Dengan Topic Reduction")
                #topic_model_after = BERTopic.load("model/model_bertopic_hmns_reduce_topic_auto_final")
                topic_model_after = BERTopic.load("vidric/bertopic_dcd_auto_final")

                # Visualize Topics
                fig = topic_model_after.visualize_topics()

                # Show the plot in Streamlit
                st.plotly_chart(fig)
          
            st.markdown("---")
