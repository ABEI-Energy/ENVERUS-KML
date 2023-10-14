import datetime as dt
import io
import locale as lc
import pandas as pd
import streamlit as st
import streamlit_toggle as tog
from docx.shared import Cm
import mapper as mp
import coordinates as cd
import functions as fn
import kml
from zipfile import ZipFile


#Set the language for datetime
lc.setlocale(lc.LC_ALL,'es_ES.UTF-8')
month = dt.datetime.now().strftime("%B %Y")
def normalize(string):
    return str(round(float(string.replace(",", ".")),2))

def normalize2(string):
    return str(string.replace(",", "."))

st.set_page_config(layout="wide")

rootShp = "USA Shapefile/USA_SHAPEFILE.shp"

"""
# ENVERUS kml maker
"""


# Time to read the documents

st.divider()

coly, colx = st.columns(2)
with colx:
    uploadedFile = st.file_uploader("Drag here the csv from Enverus. Make sure the file is not filtered.", accept_multiple_files = False)

with coly:
    st.caption("Csv example of unaltered file")
    with open("SAMPLEFILES/ENV_CSV_FILE_EXAMPLE.csv", "rb") as fp:
        btn = st.download_button(
            label="Download csv file type",
            data=fp,
            file_name="ENV_CSV_FILE_EXAMPLE.csv",
            mime='text/csv',
        )

colz, cola = st.columns(2)

if uploadedFile:

    # st.cache_data
    if uploadedFile.name.endswith('csv'):

        df_stateless, df_statefull, df_stateless_countiless, df_full = fn.df_adequacy(uploadedFile)
        #@todo hay algunos que tienen county pero no state, hay que pensar cómo llenarlos.
        df, flag_adequacy = mp.locator_json(df_stateless, df_statefull, df_stateless_countiless, df_full, rootShp)

        df.reset_index(inplace = True, drop = True)

        if flag_adequacy:

            col1, col2, col3, col4 = st.columns(4)
            state = periods = ISO = priceType = str()

            with col1:
                state = st.multiselect('Select state:', sorted(df['State'].unique()))

            with col2:
                if state:
                    ISO = st.multiselect('Select ISO:', df.loc[df['State'].isin(state), 'ISO'].unique())

            with col3:
                if state:
                    periods = st.multiselect('Select period:', df.loc[df['State'].isin(state), 'Period From'].unique())

            with col4:
                if state:
                    priceType = st.multiselect('Select price type:', df.loc[df['State'].isin(state), 'Price type'].unique())


        #@todo que cree el kml en base a las etiquetas que se gestionen
        #@todo mirar lo del html io write a ver si es eso lo que necesitamos
        #@todo que permita descargarse, primero el kml y después el html. Igual meterlo todo en el zip a ver si podemos como overpass el bitsIO

        if (len(periods)!=0) and (len(ISO)!=0) and (len(state)!=0) and (len(priceType)!=0):

            filtered_df, df_indexed = fn.filter_df(df,periods,ISO, state, priceType)

            html_to_show_spread = mp.html_display_spread(filtered_df)
            html_to_show_indexed = mp.html_display_indexed(df_indexed)
            colb, colc = st.columns(2)


            st.caption('LMP Hot Spot heatmap')

            html_to_show_indexed = mp.html_display_indexed(df_indexed)
            st.write(html_to_show_indexed)

            obj_html_io_indexed = io.StringIO()
            html_to_show_indexed.write_html(obj_html_io_indexed)
            obj_html_io_indexed.seek(0)


            st.caption('Average Max - Min Daily LMP Spread heatmap')

            html_to_show_spread = mp.html_display_spread(filtered_df)
            st.write(html_to_show_spread)

            obj_html_io_spread = io.StringIO()
            html_to_show_spread.write_html(obj_html_io_spread)
            obj_html_io_spread.seek(0)

            flag_createFile = st.button("Generate zip file")
            flagZip = False


            # st.write(filtered_df)

            if flag_createFile:
                nameZip = 'Enverus ' + str(state) + " " + str(ISO) + " " + str(periods) + " " + str(priceType) + " " + ".zip"
                zip_data = io.BytesIO()

                flagKml, kml_string = kml.kmlMaker(filtered_df)
                obj_kml_io = io.StringIO(kml_string)
                obj_kml_io.seek(0)

                # Create a ZipFile Object
                with ZipFile(zip_data, 'w') as zipf:
                   # Adding files that need to be zipped
                    zipf.writestr("Heatmap spread value.html",obj_html_io_spread.getvalue())
                    zipf.writestr("Heatmap indexed.html",obj_html_io_indexed.getvalue())
                    zipf.writestr("Node spread.kml",obj_kml_io.getvalue())

                    flagZip = True
            
            if flagZip and flagKml:
                st.info('Download the report file')
                btn = st.download_button(
                    label="Download",
                    data=zip_data.getvalue(),
                    file_name=nameZip,
                    mime="application/zip"
                )                


        pass
