import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
import numpy as np
import pandas as pd                                 
import plotly.express as px                         
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from deta import Deta
import json
from collections import Counter
from PIL import Image
image = Image.open('logo.jpg')

st.set_page_config('PKR PRU15', ':inbox_tray:', layout='wide')         # https://www.webfx.com/tools/emoji-cheat-sheet/
st.image(image, caption='')
st.title('Pilihan Raya Umum 15')
st.header('PKR - Perak Darul Ridzuan')

# Setting for utility database
parlimens = ['parlimen']
aduns = ['adun']
parti_parlimens = ['parti_parlimen']
parti_aduns = ['parti_adun']
kawasans = ['kawasan']
undi_parlimens = ['undi_parlimen']
undi_aduns = ['undi_adun']

# Utility Database Interface

DETA_KEY = st.secrets["deta_key"]              
deta = Deta(DETA_KEY)
db = deta.Base('pkr_db')

def insert_db(parlimen,adun,parti_parlimen,parti_adun,kawasan,undi_parlimen,undi_adun):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.put({'parlimen': parlimens, 'adun': aduns, 'kawasan': kawasans, 'parti_parlimen': parti_parlimens,
    'parti_adun': parti_aduns, 'undi_parlimen': undi_parlimens, 'undi_adun': undi_aduns})

def fetch_all_db():
    """Returns a dict of all date"""
    res = db.fetch()
    return res.items

with st.form('entry_form', clear_on_submit = True):

    col1, col2, col3 = st.columns(3)
    with col1:
        for parlimen in parlimens:
            parlimen = st.selectbox('Parlimen',('054 - Gerik','055 - Lenggong', '056 - Larut', '057 - Parit Buntar',
            '058 - Bagan Serai'),key = parlimen)
        for parti_parlimen in parti_parlimens:
            parti_parlimen = st.selectbox('Parti',('BN','PH','PN'), key = parti_parlimen)
        for undi_parlimen in undi_parlimens:
            st.number_input("Bil. undi", min_value=0.0,max_value = 1000000.0,step = 1e-3,format = "%.0f",key = undi_parlimen)
        
    with col2:
        for adun in aduns:
            adun = st.selectbox('Adun',
            ('N01 - Pengkalan Hulu','N02 - Temengor', 'N03 - Keniring','N04 - Kota Tampan', 'N05 - Selama'), key = adun)
        for parti_adun in parti_aduns:
            parti_adun = st.selectbox('Parti',('BN','PH','PN'), key = parti_adun)
        for undi_adun in undi_aduns:
            st.number_input("Bil. undi", min_value=0.0,max_value = 1000000.0,step = 1e-3,format = "%.0f",key = undi_adun)

    with col3:
        for kawasan in kawasans:
            kawasan = st.selectbox('Kawasan',('01','02','03'),key = kawasan)

    submit_undi = st.form_submit_button('Submit')
    if submit_undi:
        parlimens = {parlimen: st.session_state[parlimen] for parlimen in parlimens}
        aduns = {adun: st.session_state[adun] for adun in aduns}
        kawasans = {kawasan: st.session_state[kawasan] for kawasan in kawasans}
        parti_parlimens = {parti_parlimen: st.session_state[parti_parlimen] for parti_parlimen in parti_parlimens}
        parti_aduns = {parti_adun: st.session_state[parti_adun] for parti_adun in parti_aduns}
        undi_parlimens = {undi_parlimen: st.session_state[undi_parlimen] for undi_parlimen in undi_parlimens}
        undi_aduns = {undi_adun: st.session_state[undi_adun] for undi_adun in undi_aduns}
        insert_db(parlimens,aduns,kawasans,parti_parlimens,parti_aduns,undi_parlimens,undi_aduns)
        st.success('Data saved')

df = fetch_all_db()
df = json.dumps(df)
df = pd.read_json(df)

parlimen_1 = df['parlimen'].map(Counter).groupby(df['key']).sum()
parlimen_1 = df['parlimen'].apply(lambda x: x.get('parlimen')).dropna()
adun_1 = df['adun'].map(Counter).groupby(df['key']).sum()
adun_1 = df['adun'].apply(lambda x: x.get('adun')).dropna()
kawasan_1 = df['kawasan'].map(Counter).groupby(df['key']).sum()
kawasan_1 = df['kawasan'].apply(lambda x: x.get('kawasan')).dropna()
parti_parlimen1 = df['parti_parlimen'].map(Counter).groupby(df['key']).sum()
parti_parlimen1 = df['parti_parlimen'].apply(lambda x: x.get('parti_parlimen')).dropna()
parti_adun1 = df['parti_adun'].map(Counter).groupby(df['key']).sum()
parti_adun1 = df['parti_adun'].apply(lambda x: x.get('parti_adun')).dropna()
undi_parlimen1 = df['undi_parlimen'].map(Counter).groupby(df['key']).sum()
undi_parlimen1 = df['undi_parlimen'].apply(lambda x: x.get('undi_parlimen')).dropna()
undi_adun1 = df['undi_adun'].map(Counter).groupby(df['key']).sum()
undi_adun1 = df['undi_adun'].apply(lambda x: x.get('undi_adun')).dropna()

df1 = pd.merge(parlimen_1,adun_1,left_index=True,right_index=True)
df1 = pd.merge(df1,kawasan_1,left_index=True,right_index=True)
df1 = pd.merge(df1,parti_parlimen1,left_index=True,right_index=True)
df1 = pd.merge(df1,parti_adun1,left_index=True,right_index=True)
df1 = pd.merge(df1,undi_parlimen1, left_index=True,right_index=True)
df1 = pd.merge(df1,undi_adun1, left_index=True,right_index=True)
#Parlimen
bn_parlimen = df1[(df1['parti_parlimen']=='BN')]
pn_parlimen = df1[(df1['parti_parlimen']=='PN')]
ph_parlimen = df1[(df1['parti_parlimen']=='PH')]
bn_parlimen_total = bn_parlimen['undi_parlimen'].sum()
pn_parlimen_total = pn_parlimen['undi_parlimen'].sum()
ph_parlimen_total = ph_parlimen['undi_parlimen'].sum()
total = bn_parlimen_total+pn_parlimen_total+ph_parlimen_total
#Adun
bn_adun = df1[(df1['parti_adun']=='BN')]
pn_adun = df1[(df1['parti_adun']=='PN')]
ph_adun = df1[(df1['parti_adun']=='PH')]
bn_adun_total = bn_adun['undi_adun'].sum()
pn_adun_total = pn_adun['undi_adun'].sum()
ph_adun_total = ph_adun['undi_adun'].sum()


st.header('Parlimen')
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label='BN',value=f'{bn_parlimen_total:,.0f}',delta=(bn_parlimen_total/total))
with col2:
    st.metric('PN',f'{pn_parlimen_total:,.0f}')
with col3:
    st.metric('PH',f'{ph_parlimen_total:,.0f}')
#st.dataframe(df1)

fig_bar = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
fig_bar.add_trace(go.Bar(x = ['BN','PN','PH'], y = [bn_parlimen_total,pn_parlimen_total,ph_parlimen_total],name='', 
    text=[bn_parlimen_total,pn_parlimen_total,ph_parlimen_total]))
fig_bar.update_traces(texttemplate='%{text:.2f}', textposition='auto')
fig_bar.update_layout(title_text='Jumlah Undi',title_x=0.5, height=350, font=dict(family="Helvetica", size=10),
                    xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
fig_bar.update_annotations(font=dict(family="Helvetica", size=10))
fig_bar.update_xaxes(title_text='Parti', showgrid=False, zeroline=False, showline=True, linewidth=1, linecolor='black')
fig_bar.update_yaxes(showgrid=False, zeroline=False, showline=False, linewidth=1, linecolor='black')
# PIE CHART Cost
fig_pie = make_subplots(specs=[[{"type": "domain"}]])
fig_pie.add_trace(go.Pie(values=[bn_parlimen_total,pn_parlimen_total,ph_parlimen_total],labels=['BN','PN','PH'],textposition='inside',
                textinfo='label+percent'),row=1, col=1)
fig_pie.update_annotations(font=dict(family="Helvetica", size=10))
fig_pie.update_layout(height=350,showlegend=False,title_text='Peratusan Undi',title_x=0.5,font=dict(family="Helvetica", size=10))            
# Chart Presentation
col1, col2 = st.columns(2)
col1.plotly_chart(fig_bar, use_container_width=True)
col2.plotly_chart(fig_pie, use_container_width=True)

st.header('Adun')
col1, col2, col3 = st.columns(3)
with col1:
    st.metric('BN',f'{bn_adun_total:,.0f}')
with col2:
    st.metric('PN',f'{pn_adun_total:,.0f}')
with col3:
    st.metric('PH',f'{ph_adun_total:,.0f}')
#st.dataframe(df1)

fig_bar = make_subplots(shared_xaxes=True, specs=[[{'secondary_y': True}]])
fig_bar.add_trace(go.Bar(x = ['BN','PN','PH'], y = [bn_adun_total,pn_adun_total,ph_adun_total],name='', 
    text=[bn_adun_total,pn_adun_total,ph_adun_total]))
fig_bar.update_traces(texttemplate='%{text:.2f}', textposition='auto')
fig_bar.update_layout(title_text='Jumlah Undi',title_x=0.5, height=350, font=dict(family="Helvetica", size=10),
                    xaxis=dict(tickmode="array"),plot_bgcolor="rgba(0,0,0,0)",yaxis=(dict(showgrid=False)),yaxis_title=None,showlegend=False)
fig_bar.update_annotations(font=dict(family="Helvetica", size=10))
fig_bar.update_xaxes(title_text='Parti', showgrid=False, zeroline=False, showline=True, linewidth=1, linecolor='black')
fig_bar.update_yaxes(showgrid=False, zeroline=False, showline=False, linewidth=1, linecolor='black')
# PIE CHART Cost
fig_pie = make_subplots(specs=[[{"type": "domain"}]])
fig_pie.add_trace(go.Pie(values=[bn_adun_total,pn_adun_total,ph_adun_total],labels=['BN','PN','PH'],textposition='inside',
                textinfo='label+percent'),row=1, col=1)
fig_pie.update_annotations(font=dict(family="Helvetica", size=10))
fig_pie.update_layout(height=350,showlegend=False,title_text='Peratusan Undi',title_x=0.5,font=dict(family="Helvetica", size=10))            
# Chart Presentation
col1, col2 = st.columns(2)
col1.plotly_chart(fig_bar, use_container_width=True)
col2.plotly_chart(fig_pie, use_container_width=True)



# --- HIDE STREAMLIT STYLE ---

hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)