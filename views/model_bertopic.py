import streamlit as st
from bertopic import BERTopic

class ModelBertopic:
    class Model:
        title = "### Visualisasi Setelah Topic Reduction"

    def view(self, model):

        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("#### Tanpa Topic Reduction")
                topic_model_before = BERTopic.load("model/model_bertopic_hmns_before_reduce")
                
                # Visualize Topics
                fig = topic_model_before.visualize_topics()

                # Show the plot in Streamlit
                st.plotly_chart(fig)
            
            with col2:
                st.write("#### Setelah Topic Reduction")
                topic_model_after = BERTopic.load("model/model_bertopic_hmns_reduce_topic_auto_final")

                # Visualize Topics
                fig = topic_model_after.visualize_topics()

                # Show the plot in Streamlit
                st.plotly_chart(fig)
          
            st.markdown("---")
        
       
