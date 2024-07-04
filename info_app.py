import util.db_util as du
import streamlit as st


def load_db_data(query):
    tmsdb = du.tmsDB()
    return tmsdb.select_query(query=query)


def run_info_app():
    id_site = st.text_input("Input TMS Site ID", "EX) 0010001834")

    sql = f"SELECT ID_Site, Site_Name, Address, Latitude, Longitude FROM Site_Info Where id_site = '{id_site}'"
    df_site = load_db_data(sql)
    df_site['Latitude'] = df_site['Latitude'].astype(float)
    df_site['Longitude'] = df_site['Longitude'].astype(float)

    st.data_editor(
        df_site.loc[:, ['ID_Site', 'Site_Name', 'Address']],
        column_config={
            "ID_Site" : st.column_config.TextColumn(
                "TMS ID",
                width=200,
                max_chars=12
            ),
            "Site_Name" : st.column_config.TextColumn(
                "Site Name",
                width=300,
                max_chars=50
            ),
            "Address" : st.column_config.TextColumn(
                "Site Address",
                width=500,
                max_chars=300
            )
        },
        hide_index=True
    )

    st.map(df_site.loc[:, ['Latitude', 'Longitude']], latitude='Latitude', longitude='Longitude', size=200)

    # col1, col2 = st.columns(2)
    
    # with col1:
    #     st.dataframe(df_site.loc[:, ['ID_Site', 'Site_Name', 'Address']])


if __name__ == '__main__':
    run_info_app()
