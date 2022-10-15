# -*- coding: utf-8 -*-
"""MLClassification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GzaIBh6nzR7w17Rd3FxSfgCrrnSolZxS

# **CAPSTONE PROJECT - CLASSIFICATION**

## **IMPORT PACKAGES**
"""

# Import Package
import os
import pandas as pd
import numpy as np

# Package untuk visualisasi
import matplotlib.pyplot as plt
import seaborn as sns

# Package untuk cleaning, modelling, dan evaluation model
import statsmodels.api as sm
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, cross_validate, cross_val_score, KFold, StratifiedKFold, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import confusion_matrix
from sklearn import metrics

"""## **READ DATASET**"""

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv("/content/drive/MyDrive/Data Science - Mechine Learning/Data/Meet 11/reservasi_hotel.csv",sep=";")

df.head()

"""## **PROBLEM STATEMENT**

*   Perusahaan ingin mengetahui bagaimana profiling dari customer hotel mitranya, dari negara mana, bagaimana karakteristik dalam pemesanan hotel dilihat berdasarkan resort hotel dan city hotel
*   Perusahaan ingin fokus pada karakteristik yang melakukan pembatalan sebelumnya. Hal ini ingin mengoptimalkan dengan menerapkan kebijakan baru agar tidak terjadi pembatalan yang berlebih, karena dapat merugikan perusahaan.
*   Membuat mechine learning dengan feature-feature dan berikan kebijakan berdasarkan model mechine learning yang kamu buat untuk mengoptimalkan website pemesanan online hotel

## **EDA**
"""

df.columns

"""Lihat Perbandingan antara jumlah cutomer yang melakukan pembatalan atau melanjutkan pemesanan"""

df["pembatalan"].value_counts().plot.pie(autopct="%1.1f%%",shadow=True)

"""***Dari chart diatas dapat disimpulkan dari data yang ada sebanyak 63% customer melanjutkan pemesanan dan cukup besar yang melakukan pembatalan yaitu 37%***

### 1.0 Cari tau profiling dari customer

#### cari tau dari negara mana saja customer?

Untuk mencari tau profiling customer maka dilakukan filter customer yang benar2 melakukan pemesanan (tidak melakukan pembatalan)
"""

#Negara Dengan Customer Terbanyak
dforder = df[['negara']][df["pembatalan"]=="Tidak"].value_counts().sort_values(ascending=False)
dforder.head()

#Jumlah Negara Dengan Customer paling sedikit
dforder = df[['negara']][df["pembatalan"]=="Tidak"].value_counts().sort_values(ascending=False)
dforder[dforder==1].count()

"""**Berdasarkan data diatas dapat dilihat 5 negara dengan customer terbanyak yaitu Portugal** sebanyak **21071**, disusul dengan 4 negara lain yaitu 
- United Kingdom 9676
- France        8481
- Spain        6391
- Germany        6069 

dan  Jumlah Negara Dengan Customer paling sedikit yaitu sebanyak 31 negara

Lihat kembali negara2 yang memiliki order paling banyak berdasarkan tipe hotelnya
"""

negara = df[['tipe_hotel','negara']][df["negara"].isin(["PRT","GBR","FRA","ESP","DEU"])].value_counts().sort_values(ascending=False)
negara

negara.unstack().plot(kind='bar')
plt.xlabel('Tipe Hotel',fontsize=15)
plt.ylabel('Total',fontsize=15)
plt.legend(bbox_to_anchor=(1,1),shadow=True,ncol=1,title='JUmlah Negara per Tipe Hotel')
plt.ylim(ymin=0)
label,location = plt.yticks()
plt.xticks(rotation=0)
plt.gcf().set_size_inches(10,5)
plt.tight_layout()
plt.show()

"""####karakteristik dalam pemesanan hotel dilihat berdasarkan resort hotel dan city hotel"""

f,ax = plt.subplots(1,1,figsize=(12,4))
presentasecustomer = df[df["pembatalan"]=="Tidak"].groupby(["tipe_hotel"])['tipe_hotel'].count()
colors = sns.color_palette('pastel')
presentasecustomer.plot.pie(explode=[0,0.1],autopct='%1.1f%%',shadow=True,colors=colors).set_title('karakteristik dalam pemesanan hotel')
ax.set_ylabel('')
plt.show()

"""***Dari pie chart dapat dilihat customer lebih banyak memesan City Hotel dibandingkan dengan Resort Hotel, dengan perbandungan 61.6 banding 38.5 persen ***

###2.0 Cari tau karakteristik customer yang melakukan pembatalan
"""

df.columns

cspembatalan = df[df["pembatalan"]=="Ya"]
cspembatalan

"""####Cari tahu berdasarkan tipe hotel"""

f,ax = plt.subplots(1,1,figsize=(12,4))
presentasecustomerbatal = df[df["pembatalan"]=="Ya"].groupby(["tipe_hotel"])['tipe_hotel'].count()
colors = sns.color_palette('pastel')
presentasecustomerbatal.plot.pie(explode=[0,0.1],autopct='%1.1f%%',shadow=True,colors=colors).set_title('karakteristik dalam pemesanan hotel')
ax.set_ylabel('')
plt.show()

"""***City hotel memiliki jumlah pembatalan paling banyak sekitar 74.9%, berbanding lurus dengan jumlah pesanan terbanyak yaitu dari city hotel. Berarti dalam hal ini perusahaan perlu meningkatkan upaya promosi agar customer juga dapat tertarik pada tipe Resort Hotel mengingat angka presentasi pemesanan Resort Hotel yang kecil. selain itu juga perlu dicari tau mengapa customer banyak melakukan pembatalan pesanan pada city hotel***

####Cari tau  lebih lanjut karakteristik cutomer yg melakukan pembatalan
"""

feature = cspembatalan[['dewasa', 'anak_anak',
       'babies', 'meal', 'market_segment', 'tamu_berulang',
       'tipe_ruang', 'tipe_kamar_ditentukan', 'perubahan_pemesanan',
       'tipe_deposit','tipe_customer','required_car_parking_spaces']]

for col in feature:
    plt.figure(figsize=(8,6))
    sns.countplot(x=col, data=feature)
    plt.title = col
    plt.tight_layout()

"""Dari hasil analisa didapat kesimpulan, dari grafik dapat dilihat bahwa :
- Jumlah pemesanan dengan 2 orang dewasa dan tidak memiliki anak-anak dan babies cenderung lebih banyak melakukan pembatalan.
- Tipe meal dengan tipe "BB" juga cenderung banyak melakukan pembatalan.
- Market segment paling banyak yang melakukan pembatalan yaitu dari Online TA dan Group. 
- Customer baru / bukan tamu berulang lebih banyak dalam melakukan pembatalan. 
- Untuk tipe ruang dan kamar yang ditentukan yang paling banyak melakukan pembatalan adalah tipe A.
- Customer yang malakukan pembatalan lebih banyak dari customer yang tidak melakukan perubahan pemesanan
- Jenis Deposit dengan pilihan tanpa deposito dan Non Refund lebih banyak dalam melakuakn pematalan
- Tipe customer transien dan tidak membutuhkan parkir paling banyak melakukan pembatalan


"""

cspembatalan.info()

"""####Karakteristik Customer Yang sebelumnya pernah melakukan pembatalan"""

cspembatalansebelumnya = cspembatalan[['dewasa', 'anak_anak',
       'babies', 'meal', 'market_segment', 'tamu_berulang',
       'tipe_ruang', 'tipe_kamar_ditentukan', 'perubahan_pemesanan',
       'tipe_deposit','tipe_customer','required_car_parking_spaces']][cspembatalan["pembatalan_sebelumnya"]>0]
cspembatalansebelumnya

feature = cspembatalansebelumnya[['dewasa', 'anak_anak',
       'babies', 'meal', 'market_segment', 'tamu_berulang',
       'tipe_ruang', 'tipe_kamar_ditentukan', 'perubahan_pemesanan',
       'tipe_deposit','tipe_customer','required_car_parking_spaces']]

"""**Ada sebenyak 6484 customer yang sudah pernah melakukan pembatalan sebelumnya**"""

for col in feature:
    plt.figure(figsize=(8,6))
    sns.countplot(x=col, data=feature)
    plt.title = col
    plt.tight_layout()

"""Dari hasil analisa didapat kesimpulan dari grafik dapat dilihat bahwa :

- Jumlah pemesanan dengan 2 orang dewasa dan tidak memiliki anak-anak dan babies cenderung lebih banyak melakukan pembatalan sebelumnya.
- Tipe meal dengan tipe "BB" juga cenderung banyak melakukan pembatalan.
- Market segment paling banyak yang melakukan pembatalan sebelumnya yaitu dari Offile TA/TO dan Group.
- Customer baru / bukan tamu berulang lebih banyak dalam melakukan pembatalan sebelumnya.
- Untuk tipe ruang dan kamar yang ditentukan yang paling banyak melakukan pembatalan sebelumnya adalah tipe A.
- Customer yang malakukan pembatalan sebelumnya lebih banyak dari customer yang tidak melakukan perubahan pemesanan
- Jenis Deposit dengan pilihan tanpa deposito dan Non Refund lebih banyak dalam melakukan pematalan
- Tipe customer transien dan tidak membutuhkan parkir paling banyak melakukan pembatalan

## **DATA PRE-PROCESSING**

###Handling Null Value
"""

df.isnull().sum()

df.dropna(subset=['anak_anak'],inplace=True)

df.isnull().sum()

df["company"].fillna("0",inplace=True)
df.dropna(subset=['negara'],inplace=True)

df.isnull().sum()

"""###Change Data Kategori dan Cek Korelasi Data"""

# Ubah kedalam bentuk numerik
#Convertin the predictor variable in a binary numeric variable
df['pembatalan_cat'] = df['pembatalan']
df['pembatalan_cat'].replace(to_replace='Ya', value=1, inplace=True)
df['pembatalan_cat'].replace(to_replace='Tidak',  value=0, inplace=True)

df["pembatalan_cat"].unique()

df.info()

#kategori = df.select_dtypes(include=['object']).copy()
kategori = df[["tipe_hotel","meal","negara","market_segment","tipe_ruang","tipe_kamar_ditentukan","tipe_deposit","tipe_customer"]]

"""adr diubah tipe data
bulan di encode manual
company meski di hapus titiknya
"""

kategori

encoded_data = LabelEncoder()
for feature in kategori:
        if feature in df.columns.values:
            df[feature+"_cat"] = encoded_data.fit_transform(df[feature])

df.head()

df.info()

df['adr'] = df['adr'].str.replace(',','')
df['adr'] = df['adr'].astype(int)

df['company'] = df['company'].astype(float)

df.info()

df['bulan_kedatangan_cat'] = df['bulan_kedatangan']
df['bulan_kedatangan_cat'].replace(to_replace='January', value=1, inplace=True)
df['bulan_kedatangan_cat'].replace(to_replace='February', value=2, inplace=True)
df['bulan_kedatangan_cat'].replace(to_replace='March', value=3, inplace=True)
df['bulan_kedatangan_cat'].replace(to_replace='April', value=4, inplace=True)
df['bulan_kedatangan_cat'].replace(to_replace='May', value=5, inplace=True)
df['bulan_kedatangan_cat'].replace(to_replace='June', value=6, inplace=True)
df['bulan_kedatangan_cat'].replace(to_replace='July', value=7, inplace=True)
df['bulan_kedatangan_cat'].replace(to_replace='August', value=8, inplace=True)
df['bulan_kedatangan_cat'].replace(to_replace='September', value=9, inplace=True)
df['bulan_kedatangan_cat'].replace(to_replace='October', value=10, inplace=True)
df['bulan_kedatangan_cat'].replace(to_replace='November', value=11, inplace=True)
df['bulan_kedatangan_cat'].replace(to_replace='December', value=12, inplace=True)

df['bulan_kedatangan_cat'].unique()

#cek dengan heatmap
sns.heatmap(df.corr(),linewidth=.5,annot=True,cmap="RdYlGn")
fig = plt.gcf()
fig.set_size_inches(15,8)
plt.show()

# Cek Urutan korelasi terendah ke tertinggi
korelasi = df.corr()["pembatalan_cat"].sort_values()
korelasi

"""**Berdasarkan matrix didapat beberapa variabel yang memiliki korelasi besar yaitu :**
- anak_anak                                0.005048
- minggu_kedatangan                        0.008148
- tahun_kedatangan                         0.016660
- menginap_in_week_nights                  0.024765
- days_in_waiting_list                     0.054186
- market_segment                           0.059338
- dewasa                                   0.060017
- pembatalan_sebelumnya                    0.110133
- negara                                   0.264223
- waktu_tunggu                             0.293123
- tipe_deposit                             0.468634
- pembatalan                               1.000000

**Kita lihat secara spesifik matrix korelasi dari variabel2 tersebut**

required_car_parking_spaces             -0.195498
tipe_kamar_ditentukan                   -0.176028
perubahan_pemesanan                     -0.144381
tipe_hotel                              -0.136531
tamu_berulang                           -0.084793
tipe_customer                           -0.068140
tipe_ruang                              -0.061282
pemesanan_sebelumnya_tidak_dibatalkan   -0.057358
"""

cekspesifikmatrix = df[["pembatalan_cat","anak_anak","minggu_kedatangan","tahun_kedatangan","menginap_in_week_nights","days_in_waiting_list","market_segment_cat","dewasa","pembatalan_sebelumnya","negara_cat","waktu_tunggu","tipe_deposit_cat"]]

sns.heatmap(cekspesifikmatrix.corr(),linewidth=.5,annot=True,cmap="RdYlGn")
fig = plt.gcf()
fig.set_size_inches(15,8)
plt.show()

"""Tipe deposite memiliki korelasi paing besar disusul dengan waktu tunggu,negara dan pembatalan sebelumnya

## **FEATURE ENGINEERING**

Dilipih beberapa fiture yang dirasa memiliki korelaso baik/positive untuk dijadikan variabel input
"""

features = df[["pembatalan_cat","tipe_deposit_cat","waktu_tunggu","negara_cat","pembatalan_sebelumnya","days_in_waiting_list","minggu_kedatangan"]]

features.head()

# define min max scaler
scaler = MinMaxScaler()
# transform data
scaled = scaler.fit_transform(features)
data_scaled = pd.DataFrame(scaled,columns=['pembatalan_cat','tipe_deposit_cat','waktu_tunggu','negara_cat','pembatalan_sebelumnya','days_in_waiting_list','minggu_kedatangan'])
data_scaled

"""## **MODELING**

MEMBAGI TRAIN TEST DATA
"""

X = data_scaled.drop('pembatalan_cat', axis=1)
y = data_scaled['pembatalan_cat']

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=0)

"""### Stats Model (Logistic Regression)"""

Input = sm.add_constant(X_train)

model = sm.Logit(y_train,X_train,missing='drop')
result = model.fit()
print(result.summary())

"""P-value dari feature yang kita pilih kurang dari 0.005 artinya feature kita memiliki pengaruh yang signifikan"""

# odds ratio
round(np.exp(result.params), 3)

"""PREDIKSI MODEL"""

prediction = result.predict(X_test)

pred_results = pd.DataFrame(prediction, columns = ["logreg_pred"])
pred_results["prediksi"] = pred_results['logreg_pred'].apply(lambda x: 1 if x > 0.5 else 0)
pred_results['actual'] = y_test
pred_results.head()

"""####Model Evaluasi Statsmodel"""

print('Test accuracy =  {:.3f}'.format(accuracy_score(pred_results['actual'], pred_results["prediksi"])))
print('Test precision =  {:.3f}'.format(precision_score(pred_results['actual'], pred_results["prediksi"], average='binary')))
print('Test recall =  {:.3f}'.format(recall_score(pred_results['actual'], pred_results["prediksi"], average='binary')))
print('Test f-score =  {:.3f}'.format(f1_score(pred_results['actual'], pred_results["prediksi"], average='binary')))

"""### SKLEARN (Logistic Regression)"""

LR = LogisticRegression ()
LR.fit(X_train, y_train)

y_pred = LR.predict(X_test)
logreg_test = pd.merge(X_test, y_test, left_index=True, right_index=True, how='outer')
logreg_test['prediction'] = y_pred
logreg_test.head()

print('Accuracy of logistic regression classifier train data: {:.3f}'.format(LR.score(X_train, y_train)))
print('Accuracy of logistic regression classifier test data: {:.3f}'.format(LR.score(X_test, y_test)))

"""####Model Evaluasi Logistic Regresion"""

print(metrics.classification_report(y_test, y_pred))

"""Recall msekitar 39% dg presisi 91% dan akurasi 76%"""

metrics.plot_roc_curve(LR, X_test, y_test)

"""Dari test AUC dapat dilihat ada di angka 0.76 ini menunjukan model kita cukup baik, namun kita akan coba denga Tunning Model untuk mendapatkan akurasi yang maksimal

#### Model Validation Logistics Regression

Menerapkan cross validation pada model
"""

# Memilih k-fold (dipilih k = 5)
kfold = KFold(n_splits=5, shuffle=True, random_state=42)

logreg = LogisticRegression(solver='lbfgs', max_iter=1000)
scores = cross_val_score(logreg, X_train, y_train, cv=kfold)
print("Cross-validation scores: {:.3f}".format(scores.mean()))

"""Dari hasil cross validation dengan menggunakan k-fold didapat rata-rata score adalah 0,758 dimana terhitung sudah lumayan bagus.
<br>
Untuk membuat hasil model lebih bagus lagi maka akan coba dilakukan tuning parameter untuk meningkatkan kinerja model.
"""

param_grid_lr = { 'C': [0.001, 0.01, 0.1, 1, 10, 100],
                 'class_weight':['balanced', None]}

grid_search_lr = GridSearchCV(logreg, param_grid_lr, cv=kfold)
grid_search_lr.fit(X_train, y_train)
print("Best parameters: {}".format(grid_search_lr.best_params_))
print("Best cross-validation score: {:.3}".format(grid_search_lr.best_score_))

scoring = {'acc': 'accuracy',
           'F1': 'f1',
           'prec': 'precision',
           'recall':'recall'}
 
acc = []
f1 = []
prec = []
recall = []
 
logreg = LogisticRegression(C = 100)
scores = cross_validate(logreg, X, y, cv=kfold, scoring=scoring)
 
acc.append(scores['test_acc'].mean())
f1.append(scores['test_F1'].mean())
prec.append(scores['test_prec'].mean())
recall.append(scores['test_recall'].mean())
 
print("Accuracy scores: ", acc)
print("f1 scores: ", f1)
print("Precision scores: ", prec)
print("Recall scores: ", recall)

# Terapkan pada data test
logreg.fit(X_train, y_train)
predictions = logreg.predict(X_test)
 
print("Accuracy score: ", accuracy_score(predictions, y_test))
print("Recall score: ", recall_score(predictions, y_test))

print('Accuracy of logistic regression classifier train data: {:.3f}'.format(logreg.score(X_train, y_train)))
print('Accuracy of logistic regression classifier test data: {:.3f}'.format(logreg.score(X_test, y_test)))

"""Mencoba Menerapkan Stratified k-fold cross validation"""

skfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

logreg = LogisticRegression(solver='lbfgs', max_iter=1000)
scores = cross_val_score(logreg, X_train, y_train, cv=skfold)
print("Stratified K-Fold Cross-validation scores: {:.3f}".format(scores.mean()))

param_grid_lr = { 'C': [0.001, 0.01, 0.1, 1, 10, 100],
                 'class_weight':['balanced', None]}

grid_search_lr = GridSearchCV(logreg, param_grid_lr, cv=skfold)
grid_search_lr.fit(X_train, y_train)
print("Best parameters: {}".format(grid_search_lr.best_params_))
print("Best cross-validation score: {:.3}".format(grid_search_lr.best_score_))

scoring = {'acc': 'accuracy',
           'F1': 'f1',
           'prec': 'precision',
           'recall':'recall'}
 
acc = []
f1 = []
prec = []
recall = []
 
logreg = LogisticRegression(C = 100)
scores = cross_validate(logreg, X, y, cv=skfold, scoring=scoring)
 
acc.append(scores['test_acc'].mean())
f1.append(scores['test_F1'].mean())
prec.append(scores['test_prec'].mean())
recall.append(scores['test_recall'].mean())
 
print("Accuracy scores: ", acc)
print("f1 scores: ", f1)
print("Precision scores: ", prec)
print("Recall scores: ", recall)

# Terapkan pada data test
logreg.fit(X_train, y_train)
predictions = logreg.predict(X_test)
 
print("Accuracy score: ", accuracy_score(predictions, y_test))
print("Recall score: ", recall_score(predictions, y_test))

print('Accuracy of logistic regression classifier train data: {:.3f}'.format(logreg.score(X_train, y_train)))
print('Accuracy of logistic regression classifier test data: {:.3f}'.format(logreg.score(X_test, y_test)))

"""**Tidak Terjadi peningkatan  score ketika dilakukan tuning parameter**, artinya dengan feature yang ada didapat score maksimal 76% apabila kita menggunakan logistik regresion. Kita akan menambahkan feature lain yaitu **company** dengan pertimbangan akan mempengaruhi karena bisa jadi customer ada yang memesan melalui biro jasa ataupun pesan langsung tanpa biro jasa, wich is proses cancel order akan lebih mudah dilakukan apabila customer melakukan pesanan secara langsung. Kita juga akan menambahkan feature **tamu berulang**, feature ini penting mengingat bisa jadi angka cancel order untuk tamu berulang/yang sudah langganan sangat kecil kemungkinan mereka melakukan batal pesanan. Feature lain yang akan ditambahkan yaitu **market_segment,tipe_hotel,tipe_customer,tipe_ruang dan tipe_kamar_ditentukan** karena di EDA sendiri cenderung mempengaruhi status order customer

Feature Awal :

df[["pembatalan","tipe_deposit","waktu_tunggu","negara","pembatalan_sebelumnya","days_in_waiting_list","minggu_kedatangan"]]
"""

df.info()

#penambahan feature
features = df[["pembatalan_cat","tipe_deposit_cat","waktu_tunggu","negara_cat","pembatalan_sebelumnya","days_in_waiting_list","minggu_kedatangan",
               "company","tamu_berulang","tipe_hotel_cat"]]

features

"""## **EVALUATION**

## **Modeling Ulang**

MEMBAGI TRAIN TEST DATA
"""

X = features.drop('pembatalan_cat', axis=1)
y = features['pembatalan_cat']

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=42)

"""#### Logistic Regression"""

LR = LogisticRegression()
LR.fit(X_train, y_train)

y_pred = LR.predict(X_test)
logreg_test = pd.merge(X_test, y_test, left_index=True, right_index=True, how='outer')
logreg_test['prediction'] = y_pred
logreg_test.head()

print('Accuracy of logistic regression classifier train data: {:.3f}'.format(LR.score(X_train, y_train)))
print('Accuracy of logistic regression classifier test data: {:.3f}'.format(LR.score(X_test, y_test)))

print(metrics.classification_report(y_test, y_pred))

"""Setelah penambahan fiture ternyata akurasinya hampir sama, namun secara bisnis feature2 baru tersebut dibutuhkan. oleh sebab itu kita akan tetap menggunakan modeling kedua dengan beberapa tambahan feature untuk memprediksi data karena secara akurasi tidak terlalu jauh, dimana pada model pertama yaitu :

Accuracy of logistic regression classifier train data: 0.761
Accuracy of logistic regression classifier test data: 0.758 

**perbedaanya hanya beda satu angka diblakang koma, kita ambil kesimpulan secara akurasi dan best accuration model logistik ini memang berada di kiradan 76 persen**

####**Uji Coba Clasification Dengan Model Lain**
"""

# Percobaan Model Lain
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

models = [KNeighborsClassifier(), DecisionTreeClassifier(), RandomForestClassifier()]

for model in models:
  print(model)
  model.fit(X_train,y_train)
  print('Accuracy of classifier train data: {:.3f}'.format(LR.score(X_train, y_train)))
  print('Accuracy ofclassifier test data: {:.3f}'.format(LR.score(X_test, y_test)))
  print('---------------------------------')

"""Dari hasil uji coba dengan model lain dapat disimpulkan bahwa akurasi terbaik memang tetap berada dikisaran akurasi 76 persen. Oleh karena itu kita akan menggunakan model Logistic Regression  untuk memprediksi new data

##**LOAD AND PREDICT NEW DATA**

Feature yang sudah digunakan adalah: 

"pembatalan_cat","tipe_deposit_cat","waktu_tunggu","negara_cat","pembatalan_sebelumnya","days_in_waiting_list","minggu_kedatangan",
"company","tamu_berulang","tipe_hotel_cat"

####**Lihat Label Setiap Kategory**
"""

df[["pembatalan","pembatalan_cat"]].value_counts()

df[["tipe_deposit","tipe_deposit_cat"]].value_counts()

df[["negara","negara_cat"]].value_counts()

df[["tipe_hotel","tipe_hotel_cat"]].value_counts()

"""####**Predict New Data**"""

LR = LogisticRegression()
LR.fit(X_train, y_train)

y_pred = LR.predict(X_test)
logreg_test = pd.merge(X_test, y_test, left_index=True, right_index=True, how='outer')
logreg_test['prediction'] = y_pred
logreg_test

confusion_matrix = metrics.confusion_matrix(y_test, y_pred) 

cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = [False, True])

cm_display.plot()
plt.show()

tipe_deposit = int(input('Apakah ada tipe_deposit')) #No Deposit  =  0 , Non Refund   = 1,Refundable    2 
waktu_tunggu = int(input('Masukan waktu_tunggu')) #7
negara= int(input('Masukan kode negara')) #PRT = 135
pembatalan_sebelumnya = int(input("Input pembatalan_sebelumnya")) #0
days_in_waiting_list = int(input("Input days_in_waiting_list"))#0
minggu_kedatangan = int(input("Input minggu_kedatangan"))#27
company = int(input("Input company")) #223
tamu_berulang = int(input("apakah tamu_berulang"))#1
tipe_hotel = int(input("Pilih tipe_hotel")) #City Hotel =0, Resort Hotel = 1

#model terbaik
databaru = np.array([[tipe_deposit, waktu_tunggu, negara, pembatalan_sebelumnya, days_in_waiting_list, minggu_kedatangan, company, tamu_berulang, tipe_hotel]])

prediksi2=LR.predict(databaru)

if prediksi2 == 0:
  print("Customer Tidak melakukan pembatalan")
else:
  print("Customer Melakukan pembatalan")

"""## **KESIMPULAN/SARAN**

Perusahaan perlu membuat promosi untuk resort hotel karena presentasi order yang lumayan kecil jika dibandingkan dengan city hotel, kemudian matrix yang mempengaruhi angka pembatalan pemesanan juga perlu di reduse seperti misalkan mengharuskan untuk deposite terlebih dahulu untuk pemesanan hotel dan perlu melakukan mekanisme promosi pada negara-negara dengan angka order terkecil, mungkin bisa mengadayakan upaya promosi kerjasama dengan destinasi wisata setempat untuk melakukan upaya marketing campaign atau promosi lainya dengan target negara-negara tersebut. Bisa juga mengadakan sistem loyalti point/rewards ataupun referal bagi pengunjung setia hotel.
"""