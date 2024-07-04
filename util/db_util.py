import streamlit as st
import pandas as pd
import pyodbc


class tmsDB : 
    # @st.cache_resource
    def __init__(self) :
        self.host = st.secrets.db_credentials.url
        self.user = st.secrets.db_credentials.id
        self.password = st.secrets.db_credentials.pw
        self.database = st.secrets.db_credentials.db
        self.conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.host+';DATABASE='+self.database+';UID='+self.user+';PWD='+ self.password
        self.db_conn = pyodbc.connect(self.conn_str, timeout=90)

    def __del__(self) :
        self.close()
    
    def re_open(self) : 
        self.db_conn = pyodbc.connect(self.conn_str)

    def close(self) :
        if self.db_conn is not None:
            self.db_conn.close()

    # @st.cache_data(ttl=600)
    def select_query(self, query) :
        for retry in range(3) :
            try :
                result = pd.read_sql(sql = query, con =self.db_conn)
                break
            except :
                if retry < 2 :
                    self.re_open()
                    continue
                st.error( 'DB Error' + ' => '  + 'query select error!!')
                st.error( 'query' + ' => '  + query)

        return result

    def insert_query(self, query) :
        with self.db_conn.cursor() as cursor :
            try :
                cursor.execute(query)
                self.db_conn.commit()
            except Exception as e: 
                st.error(e)

        return True

    def execute_procedure(self, query, params) :
        with self.db_conn.cursor() as cursor :
            try :
                cursor.execute(query, params)
                self.db_conn.commit()
            except Exception as e : 
                st.error(e)

        return True
    
    def get_execute_procedure(self, query, params) :
        for retry in range(3) :
            try :
                result = pd.read_sql(sql = query, con =self.db_conn, params=params)
                break
            except :
                if retry < 2 :
                    self.re_open()
                    continue
                st.error( 'DB Error' + ' => '  + 'query select error!!')
                st.error( 'query' + ' => '  + query)

        return result
    