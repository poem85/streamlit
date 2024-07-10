import util.db_util as du
import streamlit as st


def load_db_data(query):
    tmsdb = du.tmsDB()
    return tmsdb.select_query(query=query)


def run_info_app():
    id_site = st.text_input("Input TMS Site ID", "EX) 0010001834")

    tab1, tab2 = st.tabs(["Site Info.", "Product Info."])

    # Site Info
    with tab1:
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

    with tab2:
        sql = f"SELECT ID_GW, ID_ODU, ID_AWHP FROM AWHP_Info Where id_site = '{id_site}'"
        df_awhp_list = load_db_data(sql)

        col1, col2, col3 = st.columns(3)
        with col1:
            id_gw = st.selectbox(
                label=' ',
                options=df_awhp_list['ID_GW'].unique(),
                index=None,
                placeholder="Select Gateway ID...",
                label_visibility="hidden"
            )
        with col2:
            id_odu = st.selectbox(
                label=' ',
                options=df_awhp_list[df_awhp_list.ID_GW == id_gw]['ID_ODU'].unique(),
                index=None,
                placeholder="Select ODU ID...",
                label_visibility="hidden"
            )
        with col3:
            id_awhp = st.selectbox(
                label=' ',
                options=df_awhp_list[(df_awhp_list.ID_GW == id_gw) & (df_awhp_list.ID_ODU == id_odu)]['ID_AWHP'],
                index=None,
                placeholder="Select AWHP ID...",
                label_visibility="hidden"
            )

        sql = f"SELECT ID_Site, ID_GW, ID_ODU, ID_AWHP, oper, Mode, hotwater, watertanktemp, watertanksettemp, roomtemp, awsettemp \
            FROM AWHP_Info ai WHERE ID_Site = '{id_site}' and ID_GW = '{id_gw}' and ID_ODU = '{id_odu}' and ID_AWHP = '{id_awhp}'"
        df_oper = load_db_data(sql)

        st.data_editor(
            df_oper.loc[:, ['ID_Site', 'ID_GW', 'ID_ODU', 'ID_AWHP', 'oper', 'Mode', 'hotwater']],
            column_config={
                "ID_Site" : st.column_config.TextColumn(
                    "TMS ID",
                    width="medium",
                    max_chars=10
                ),
                "ID_GW" : st.column_config.TextColumn(
                    "GW ID",
                    width="medium",
                    max_chars=10
                ),
                "ID_ODU" : st.column_config.TextColumn(
                    "ODU ID",
                    width="medium",
                    max_chars=10
                ),
                "ID_AWHP" : st.column_config.TextColumn(
                    "AWHP ID",
                    width="medium",
                    max_chars=10
                ),
                "oper" : st.column_config.TextColumn(
                    "Operation",
                    width="medium",
                    max_chars=100
                ),
                "Mode" : st.column_config.TextColumn(
                    "Mode",
                    width="medium",
                    max_chars=100
                ),
                "hotwater" : st.column_config.TextColumn(
                    "Hotwater",
                    width="medium",
                    max_chars=100
                ),
            }, hide_index=True
        )

        if len(df_oper) > 0:
            row_container = st.container(border=True)
            sub_col1, sub_col2, sub_col3, sub_col4 = row_container.columns(4)
            sub_col1.metric("Watertank Current", value=f"{df_oper.loc[0, 'watertanktemp']} ℃")
            sub_col2.metric("Watertank Set", value=f"{df_oper.loc[0, 'watertanksettemp']} ℃")
            sub_col3.metric("Room Current", value=f"{df_oper.loc[0, 'roomtemp']} ℃")
            sub_col4.metric("Room Set", value=f"{df_oper.loc[0, 'awsettemp']} ℃")



if __name__ == '__main__':
    run_info_app()
