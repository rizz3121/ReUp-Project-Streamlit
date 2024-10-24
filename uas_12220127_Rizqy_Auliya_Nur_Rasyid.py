#Rizqy Auliya Nur Rasyid
#12220127
#Program Visualisasi Data Perolehan Minyak Mentah Berbagai Negara dalam Rentang Tahun 1971-2015

from urllib.request import urlopen
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm, colors
import streamlit as st
import json
import requests
from io import BytesIO

fhand=pd.read_csv("https://raw.githubusercontent.com/Rizqya3121/Tubes/main/produksi_minyak_mentah.csv")


#title main page
st.set_page_config(layout="wide")
st.title("Statistik Produksi Minyak Berbagai Negara di Dunia")
st.markdown("Berikut adalah visualisasi dan rangkuman data produksi minyak dari berbagai negara di dunia dalam rentang tahun 1971-2015")


#sidebar
gambar= requests.get("https://raw.githubusercontent.com/Rizqya3121/Tubes/main/offshore-drilling-rigs.png")
st.sidebar.image(BytesIO(gambar.content))

st.sidebar.title("Customization")
left_col, mid_col, right_col = st.columns(3)

#Inputan yang dapat dikustomisasi oleh user
st.sidebar.subheader("Silakan pilih konfigurasi")
fhand2=urlopen("https://raw.githubusercontent.com/Rizqya3121/Tubes/main/kode_negara_lengkap.json")
info=json.load(fhand2)
daftar_negara=[]
daftar_kode=[]
wow={} #Dictionary yang berisi nama lengkap negara sebagai key dan alpha 3 sebagai value
wow2={} #Dictionary yang berisi alpha 3 sbg key dan nama negara sebagai value
for i in range(len(info)):
    daftar_negara.append(info[i]['name'])
for i in range(len(info)):
    daftar_kode.append(info[i]['alpha-3'])
for i in range(len(daftar_negara)):
    wow[daftar_negara[i]]=daftar_kode[i]
for i in range(len(daftar_negara)):
    wow2[daftar_kode[i]]=daftar_negara[i]

bersih=fhand[fhand['kode_negara'].isin(daftar_kode)] #membersihkan dataframe dari negara yg tidak ada di json
inputannegara=list(bersih['kode_negara'].unique())
listnegara=[]
for i in inputannegara:
    listnegara.append(wow2[i])
inputantahun=list(bersih['tahun'].unique())
wow3={} #Dictionary yang menyimpan key berupa nama negara lengkap dan value alpha-3 negara tanpa organisasi (bersih)
negarabersih=[]
for i in inputannegara:
    if i in wow2:
        wow3[wow2[i]]=i
        negarabersih.append(wow2[i])

daftar_benua=[]
daftar_srg=[]
for i in range(len(info)):
    daftar_benua.append(info[i]['region'])
    daftar_srg.append(info[i]['sub-region'])

#Inputan User
aktif= st.sidebar.checkbox('Aktifkan advanced searching')
if aktif:
        dfkotor=pd.DataFrame(list(zip(daftar_benua,daftar_srg,daftar_negara)),columns=['benua','srg','negara']) #DF berisi benua, subregion, dan nama negara
        dfcomb=dfkotor[dfkotor['negara'].isin(negarabersih)] #Pembersihan DF, dicari yang hanya berupa negara
        benua= list(set(list(dfcomb['benua']))) #Membuat list berisi benua unik
        inputbenua= st.sidebar.selectbox('Pilih region', benua)
        masked1=dfcomb.loc[dfcomb['benua'] == inputbenua]
        inputsubregion= list(set(list(masked1['srg'])))
        inputusersrg= st.sidebar.selectbox("Pilih sub-region", inputsubregion)
        masked2=masked1.loc[masked1['srg'] == inputusersrg]
        cntry = st.sidebar.selectbox("Pilih negara", list(set(list(masked2['negara']))))
else:
    cntry = st.sidebar.selectbox("Pilih negara", wow3)

tahun = st.sidebar.selectbox("Pilih tahun", inputantahun)
topn=   st.sidebar.number_input("Berapa besar?", min_value=1, max_value=len(bersih), value=5)

subreg={}
region={}
for i in range(len(info)):
    subreg[info[i]['alpha-3']]=info[i]['sub-region']
    region[info[i]['alpha-3']]=info[i]['region']

#Nomor 1 (Kolom Bagian Kiri Atas)
left_col.subheader("Grafik Produksi Minyak Mentah")
p=bersih.loc[bersih['kode_negara'] == wow3[cntry]] #p adalah dataframe berisi data dari negara inputan user
fig, ax = plt.subplots()
colors=range(len(p))
ax.plot(p['tahun'], p['produksi'])
ax.scatter(p['tahun'], p['produksi'])
plt.title("Negara: {}".format(cntry))
plt.xticks(np.arange(1971,2016,5), rotation=90)
ax.set_xlabel("Tahun", fontsize=12)
ax.set_ylabel("Jumlah Produksi Minyak", fontsize=12)
plt.tight_layout()
left_col.pyplot(fig)

#Nomor 2 (Kolom Bagian Tengah Atas)
mid_col.subheader("Top {} Produsen Minyak Mentah {}".format(topn,tahun))

chosenyear=bersih.loc[bersih['tahun'] == tahun]
final_df = chosenyear.sort_values(by=['produksi'], ascending=False).head(topn) 
finaldf=final_df.sort_values(by=['produksi'], ascending=True) #DF agar horizontal bar tidak terbalik urutannya
fig,ax = plt.subplots()
yaxis=[] #List untuk menyimpan nama negara sbg sumbu y nantinya

for a in finaldf['kode_negara']:
    yaxis.append(wow2[a])

cmap_name = 'tab20'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(yaxis)]
plt.barh(yaxis,finaldf['produksi'],color=colors)
plt.xlabel("Jumlah Produksi Minyak")
plt.xticks(rotation=50)
plt.tight_layout()
mid_col.pyplot(fig)

#Nomor 3 (Bagian Kolom Kanan Atas)
right_col.subheader("Top {} Produsen of All Time".format(topn))

dftop=bersih.groupby(bersih['kode_negara']).agg("sum") #Membuat DF dengan menghilangkan data ganda, dan dijumlah value per kolom
dftop2=dftop.sort_values(by=['produksi'], ascending=False).head(topn).reset_index() #Membuat DF top n produsen
fig,ax = plt.subplots()
xaxis=[] #List berisi daftar nama negara pada sumbu x nantinya
fig,ax =plt.subplots()
for a in dftop2['kode_negara']:
    xaxis.append(wow2[a])
plt.bar(xaxis,dftop2['produksi'],color=colors)
plt.ylabel('Jumlah Produksi Minyak')
plt.xticks(rotation=90)
plt.ticklabel_format(style='plain', axis='y')
right_col.pyplot(fig)

#Nomor 4 bagian 1
left_col.subheader("Summary: Top Producer")
goat=bersih.sort_values(by=['produksi'], ascending=False).head(1).reset_index()
yeargoat= chosenyear.sort_values(by=['produksi'], ascending=False).head(1).reset_index()
left_col.markdown('_Penghasil Minyak Terbesar pada Tahun {}:_'.format(tahun))
left_col.markdown('{} ({}), di sub-region {}, region {}, sebanyak {}'.format(wow2[yeargoat['kode_negara'][0]],yeargoat['kode_negara'][0],subreg[yeargoat['kode_negara'][0]],region[yeargoat['kode_negara'][0]],yeargoat['produksi'][0]))

left_col.markdown('_Penghasil Minyak Terbesar of All Time (NON KUMULATIF):_')
left_col.markdown('{} ({}), di sub-region {}, region {}, sebanyak {} pada tahun {}'.format(wow2[goat['kode_negara'][0]],goat['kode_negara'][0],subreg[goat['kode_negara'][0]],region[goat['kode_negara'][0]],goat['produksi'][0],goat['tahun'][0]))

left_col.markdown('_Penghasil Minyak Terbesar of All Time (KUMULATIF):_')
left_col.markdown('{} ({}), di sub-region {}, region {}, sebanyak {}'.format(wow2[dftop2['kode_negara'][0]],dftop2['kode_negara'][0],subreg[dftop2['kode_negara'][0]],region[dftop2['kode_negara'][0]],dftop2['produksi'][0]))

#Nomor 4 bagian 2
mid_col.subheader("Summary: Lowest Producer")
nozero= bersih[bersih.produksi != 0]
nozero2= chosenyear[chosenyear.produksi != 0]
nogoat=nozero.sort_values(by=['produksi'], ascending=True).head(1).reset_index()
noyeargoat= nozero2.sort_values(by=['produksi'], ascending=True).head(1).reset_index()
mid_col.markdown('_Penghasil Minyak Terkecil pada Tahun {}:_'.format(tahun))
mid_col.markdown('{} ({}), di sub-region {}, region {}, sebanyak {}'.format(wow2[noyeargoat['kode_negara'][0]],noyeargoat['kode_negara'][0],subreg[noyeargoat['kode_negara'][0]],region[noyeargoat['kode_negara'][0]],noyeargoat['produksi'][0]))

mid_col.markdown('_Penghasil Minyak Terkecil of All Time (NON KUMULATIF):_')
mid_col.markdown('{} ({}), di sub-region {}, region {}, sebanyak {} pada tahun {}'.format(wow2[nogoat['kode_negara'][0]],nogoat['kode_negara'][0],subreg[nogoat['kode_negara'][0]],region[nogoat['kode_negara'][0]],nogoat['produksi'][0],nogoat['tahun'][0]))

dflow=dftop[dftop.produksi != 0]
dflowfinal=dflow.sort_values(by=['produksi'], ascending=True).head(1).reset_index()
mid_col.markdown('_Penghasil Minyak Terkecil of All Time (KUMULATIF):_')
mid_col.markdown('{} ({}), di sub-region {}, region {}, sebanyak {}'.format(wow2[dflowfinal['kode_negara'][0]],dflowfinal['kode_negara'][0], subreg[dflowfinal['kode_negara'][0]],region[dflowfinal['kode_negara'][0]],dflowfinal['produksi'][0]))

#Nomor 4 bagian 3
left_col.subheader("Summary: is Not Producer")
chosen=chosenyear.reset_index()
left_col.markdown('_Bukan Penghasil Minyak tahun {} :_'.format(tahun))
count=1
for i in range(len(chosen)):
    if chosen['produksi'][i]==0:
        left_col.markdown('{}) {} ({}), di sub-region {}, region {}'.format(count,wow2[chosen['kode_negara'][i]],chosen['kode_negara'][i],subreg[chosen['kode_negara'][i]],region[chosen['kode_negara'][i]]))
        count+=1
left_col.markdown("Banyak negara bukan produsen minyak pada tahun {}: {} Negara".format(tahun,count-1))

count2=1
mid_col.subheader("Summary: is Not Producer of All Time")
mid_col.markdown("_Negara-negara yang bukan merupakan produsen:_")
dfnewidx=dftop.reset_index()
for i in range(len(dftop)):
    if dftop['produksi'][i]==0:
        mid_col.markdown('{}) {} ({}), di sub-region {}, region {}'.format(count2,wow2[dfnewidx['kode_negara'][i]],dfnewidx['kode_negara'][i],subreg[dfnewidx['kode_negara'][i]],region[dfnewidx['kode_negara'][i]]))
        count2+=1
mid_col.markdown("Banyak negara bukan produsen minyak : {} Negara".format(count2-1))

#Bonus Point
#Top-B Negara dengan rata-rata tertinggi
right_col.subheader('Top {} Rataan Produksi'.format(topn))
avg=bersih.groupby(bersih['kode_negara']).agg('mean')
avg2=avg.sort_values(by=['produksi'], ascending=False).head(topn).reset_index() 
avgtop=avg2.sort_values(by=['produksi'], ascending=True)
yax=[] #List untuk menyimpan nama negara sbg sumbu y nantinya

for a in avgtop['kode_negara']:
    yax.append(wow2[a])

fig,ax=plt.subplots()
plt.barh(yax, avgtop['produksi'],color=colors)
plt.xlabel("Rataan Produksi Minyak")
plt.tight_layout()
right_col.pyplot(fig)
