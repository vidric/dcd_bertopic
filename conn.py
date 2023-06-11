import streamlit as st

class Database:
    def __init__(self):
        self.conn = st.experimental_connection('mysql', type='sql')

    def query(self, sql):
        return self.conn.query(sql, ttl=600)
