# -*- coding: utf-8 -*-
"""Aditya H - ML Assignment  .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/164nzwPKVWcIiEpmgRIi2CQRu7M8dSBtL

# Introduction

We're told by our colleagues at the hypothetical company that customer churn is at 50% within 3 months. That means that within 3 months of a set of customers that sign up for the paid product, by the end of 3 months half of them will have cancelled. This is an urgent problem we need to help fix with machine learning!

## Metadata

Here are some types of data that are useful in customer churn analysis:
* Customer ID or other identification information
* Date the customer was acquired
* How the customer was acquired (source of sale i.e. referral, web signup, etc.)
* Plan type (what subscription they are on)
* Cohort analysis by user type (seasonal onboards by marketing campaign or time of year, etc.)
* If they use add ons (sush as Online Security or Device Protection)? 
* Have they set up to pay for their subscription online? 
* Customer size
* Customer segment type (i.e. company user, accountant)
* Customer country of residence
* Customer state of residence
* NPS score (satisfaction level 0-10 from questionnaire) 
* Time to first success moment (days)
* Total number of times logged in
* Time since last login
* Days since key inflection points (work with SME in marketing/product) this could be days since logging in, since getting their first result from the technology, etc. 
* Time spent logged in past month
* Time spent logged in average/mo for length of subscription
* Number of times they have contacted customer service over life of subscription
* Number of customer service calls in the prior month that they cancelled
* Number of times they opened and clicked on the Help text in the app or online
* What they typed into the search box in the help text in the app
* Tenure (Lifetime account duration in days)
* Total subscription amount paid
* Date unsubscribed (timestamp)
* How many other products they have from our company
* What other products they have from our company, as a separate column for each (yes / no)
* Anything else specific to the business of note
* Cancelled yes or no (Churn)

# Install & Load Library
"""

!pip install dalex
!pip install scikit-plot

!pip install xgboost

# Commented out IPython magic to ensure Python compatibility.
# load pandas untuk data wrangling
import pandas as pd
# load numpy untuk manipulasi vektor
import numpy as np
# load matplotlib untuk visualisasi data
import matplotlib.pyplot as plt
# load seaborn untuk visualisasi data
import seaborn as sns

# load metrics object dari sklearn
from sklearn import metrics
# load train-test data splitter
from sklearn.model_selection import train_test_split
# load Decision Tree classifier model
from sklearn.tree import DecisionTreeClassifier
# load Random Forest classifier model
from sklearn.ensemble import RandomForestClassifier
# load SVM classifier model
from sklearn.svm import SVC
# load KNN classifier model
from sklearn.neighbors import KNeighborsClassifier

# load xgboost classifier model
from xgboost import XGBClassifier

# Load DALEX untuk interpretability
import dalex as dx

# load scikitplot untuk visualisasi metrik
import scikitplot as skplt

# %matplotlib inline

"""# Load Dataset"""

# load dataset ke raw_data
raw_data = pd.read_csv("https://raw.githubusercontent.com/hadimaster65555/dataset_for_teaching/main/dataset/telco_customer_churn/Telco-Customer-Churn.csv")

"""# Data Inspection

## Soal 1: 

1. Cek struktur data. Berdasarkan sturktur data yang anda miliki saat ini, variabel apa saja yang merupakan:
  - variabel yang seharusnya bertipe numerik
  - variabel yang seharusnya bertipe kategorik

2. Cek nilai yang hilang pada dataset
  - Jika ada nilai yang hilang, masuk dalam kategori apakah data yang hilang tersebut (MNAR, MCAR, MAR)? Jelaskan alasan anda
  - Apa yang akan anda lakukan pada data yang hilang tersebut? Jelaskan alasan anda
"""

# cek struktur data
df = raw_data
df.dtypes

#memperbesar ukuran display pada data
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df.head(7)

# Cek data yang hilang
df.isnull().sum()

# memeriksa frekuensi pada data colums
print(f"{df['gender'].value_counts()} \n")
print(f"{df['SeniorCitizen'].value_counts()} \n")
print(f"{df['Partner'].value_counts()} \n")
print(f"{df['Dependents'].value_counts()} \n")
print(f"{df['tenure'].value_counts()} \n")
print(f"{df['PhoneService'].value_counts()}\n")
print(f"{df['MultipleLines'].value_counts()}\n")
print(f"{df['InternetService'].value_counts()} \n")
print(f"{df['OnlineSecurity'].value_counts()} \n")
print(f"{df['OnlineBackup'].value_counts()} \n")
print(f"{df['DeviceProtection'].value_counts()}\n")
print(f"{df['TechSupport'].value_counts()}\n")
print(f"{df['StreamingTV'].value_counts()} \n")
print(f"{df['StreamingMovies'].value_counts()} \n")
print(f"{df['Contract'].value_counts()} \n")
print(f"{df['PaperlessBilling'].value_counts()} \n")
print(f"{df['PaymentMethod'].value_counts()}\n")
print(f"{df['MonthlyCharges'].value_counts()}\n")
print(f"{df['TotalCharges'].value_counts()} \n")
print(f"{df['Churn'].value_counts()} \n")

#data mising value 'TotalCharges'
a = df['TotalCharges']==' '
df.loc[a]

"""**Penjelasan**

---
1. Jawaban Pertanyaan No 1

var numerik : 
tenure
monthly_charges
total_charges

var categorical : 
gender 
seniorcitizen
partner 
dependents
phoneservice
multiplelines
internetService
onlineSecurity
onlinebackup
DeviceProtection
techsupport
streamingtv
streamingmovies
contract
paperlessbilling
paymentmethod
churn 

2. Jawaban Pertanyaan No 2 

a. Terdapat missing value pada variabel 'TotalCharges', Asumption Missing Value masuk kedalam kategori MAR karena Missing Value yang ada bergantung pada value yang diamati. 

b. Data yang hilang tersebut akan saya drop dikarenakan jika missing value tersebut di isi dengan nilai yang lain(rata2,mode,dll) maka akan berdampak pada model yang akan didevelop nantinya, kemudian jumlah komposisi mising value terebut tergolong tidak terlampau banyak jumlahnya. maka akan sangat ideal jika missing value tersebut di drop
"""

#Menghapus Missing Values
df = df.drop(df[df.TotalCharges ==' '].index)

#Mengubah Data Pada Column churn
def churn(row):
    if row['Churn']=='No':
        return(0)
    else :
        return(1)

df['Churn'] = df.apply(churn, axis=1)

#mengubah variabel yang belum sesuai
ubah = {'TotalCharges' : float,
        'SeniorCitizen': str,
        'Churn': str}
df = df.astype(ubah)

#Mengecek Tipe Data 
df.dtypes

# Drop column customer ID
df = df.drop('customerID', axis = 1)

df.head(3)



"""# Train-Test Split Data"""

# buang kolom Churn dari raw_data lalu masukkan ke X
X = df.drop(["Churn"], axis = 1)
# masukkan nilai kolom Churn ke y
y = df["Churn"]

# pisahkan data menjadi data train dan data test
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y, 
    test_size=0.2,
    stratify = y, 
    random_state=1000
)

"""# Data Exploration"""

# buat kolom Churn pada X_train dengan memasukkan nilai y_train ke dalamnya
X_train["Churn"] = y_train

X_train.head()

"""## Soal 2

1. Cek distribusi dari kelas target dengan visualisasi lalu interpretasikan maksud dari visualisasi yang terbentuk

2. Apa yang akan anda lakukan pada data ini jika kelas targetnya tidak seimbang? Jelaskan alasan anda.
"""

# Cek distribusi kelas target
sns.countplot(data = X_train, x = "Churn")

# proporsi dari variabel 'Churn'
X_train['Churn'].value_counts(normalize=True)

"""**Interpretasi**

---
1. Pertanyaan 1 :
dari hasil visualisasi dapat diketahui bahwa distribusi kelas target tidak seimbang, dalam hal ini variabel kelas target yang bernilai 0 atau tidak berhenti berlangganan memiliki proporsi 73,42% sedangkan variabel kelas target yang bernilai 1 atau pelanggan yang berhenti berlangganan memiliki proporsi 26,58%

2. Pertanyaan 2: 
yang akan saya lakukan adalah melakukan treatment dengan Hyperparameter Tuning, karena jumlah data testing dan training > 1000 dan juga agar pada data imbalance tidak menghasilkan akurasi yang rendah dikarenakan proporsi kelas target yang tidak seimbang

## Soal 3

Lakukan dua analisis berikut

1. Analisis korelasi antar variabel dengan menggunakan correlation matrix

2. Analisis hubungan antara prediktor dengan target dengan menggunakan visualisasi berikut:
  - Jika kategorik vs kategorik, gunakan barplot
  - Jika kategorik vs numerik, gunakan boxplot
"""

# membuat dummy variabel dari variabel kategorik pada X_train
X_train = pd.get_dummies(X_train, drop_first = True)

# membuat dummy variabel dari variabel kategorik pada X_test
X_test = pd.get_dummies(X_test, drop_first = True)

# Correlation Matrix
plt.figure(figsize=(16,10))
sns.heatmap(X_train.corr(method='spearman'), cmap="YlGnBu", annot=True)

X_train = X_train.rename(columns={'Churn_1':'Churn', 'gender_Male' : 'gender'})
X_test = X_test.rename(columns={'Churn_1':'Churn', 'gender_Male' : 'gender'})

"""**Interpretasi**

Diketahui bahwa terdapat variabel yang mengandung multikolonearitas sehingga salah satu dari variabel tersbut harus di hapus untuk menghindari multikolonearitas


"""

#menghapus variabel yang memiliki nilai multikolonearitas yang tinggi 
X_train = X_train.drop(['TotalCharges', 'PhoneService_Yes','MonthlyCharges'], axis = 1)
X_test = X_test.drop(['TotalCharges', 'PhoneService_Yes','MonthlyCharges'], axis = 1)

# Correlation Matrix
plt.figure(figsize=(16,10))
sns.heatmap(X_train.corr(method='spearman'), cmap="YlGnBu", annot=True)

"""---

## Categorical Data vs Churn
"""

# Definisikan fungsi untuk menghitung proporsi
def prop_agg(df, y, x):
  temp_df = df.groupby([y,x], as_index = False).size()
  temp_df['prop'] = temp_df['size'] / temp_df.groupby(y)['size'].transform('sum')
  return temp_df

# hitung proporsi gender dan Churn
prop_agg(X_train, "gender", "Churn")

"""**Gender vs Churn**"""

# membuat fungsi untuk menghitung proporsi kategori
# terhadap kelas target
def prop_agg(df, y, x):
  temp_df = df.groupby([y,x], as_index = False).size()
  temp_df['prop'] = temp_df['size'] / temp_df.groupby(y)['size'].transform('sum')
  return temp_df

# variabel 'Gender' vs 'Churn'
g = sns.FacetGrid(
    data = prop_agg(X_train, "gender", "Churn"),
    col = "gender"
)
g.map(sns.barplot, "Churn", "prop");

"""**Interpretasi**

Diketahui bahwa untuk kategori churn terhadap gender memiliki proporsi yang hampir mirip dan merata. 
artinya secara gender jumlah laki - laki dan perempuan yang memilih untuk berhenti berlangganan dan tetap berlangganan tidak jauh berbeda

**Senior Citizen vs Churn**
"""

# variabel 'Senior Citizen' vs 'Churn'
g = sns.FacetGrid(
    data = prop_agg(X_train, "SeniorCitizen", "Churn"),
    col = "SeniorCitizen"
)
g.map(sns.barplot, "Churn", "prop");

"""**Interpretasi**

Diketahui bahwa untuk kategori churn terhadap variabel SeniorCitizen memiliki proporsi yang berbeda. 
pelanggan yang berusia lanjut cenderung memiliki presentase lebih tinggi untuk tidak berlangganan kembali dibandingkan dengan mereka yang bukan termasuk dalam kategori warga berusia lanjut

**Partner vs Churn**
"""

# variabel 'Patner' vs 'Churn'
g = sns.FacetGrid(
    data = prop_agg(X_train, "Partner", "Churn"),
    col = "Partner"
)
g.map(sns.barplot, "Churn", "prop");

"""**Interpretasi**

Diketahui bahwa untuk kategori churn terhadap variabel partner memiliki proporsi yang berbeda.
Pelanggan yang tidak bermitra cenderung memiliki presentase lebih tinggi untuk tidak berlangganan kembali di bandingkan dengan pelanggan yang bermitra

**Dependent vs Churn**
"""

# variabel 'Dependent' vs 'Churn'
g = sns.FacetGrid(
    data = prop_agg(X_train, "Dependents", "Churn"),
    col = "Dependents"
)
g.map(sns.barplot, "Churn", "prop");

"""**Interpretasi**

Diketahui bahwa untuk kategori churn terhadap variabel dependent memiliki proporsi yang berbeda.
Pelanggan yang tidak bergantung pada layanan cenderung memiliki presentase lebih tinggi untuk tidak berlangganan kembali di bandingkan dengan pelanggan yang bergantung pada layanan

**Online Security vs Churn**
"""

# variabel 'Online Security' vs 'Churn'
g = sns.FacetGrid(
    data = prop_agg(X_train, "OnlineSecurity", "Churn"),
    col = "OnlineSecurity"
)
g.map(sns.barplot, "Churn", "prop");

"""**Interpretasi**

Diketahui bahwa untuk kategori churn terhadap variabel online security memiliki proporsi yang berbeda.
Pelanggan yang tidak menggunakan layanan internet memiliki presentase lebih kecil untuk tidak berlangganan kembali 
Jika di bandingkan dengan pelanggan yang menggunakan layanan internet maka pelanggan yang menggunakan keamanan online akan memiliki presentase untuk berlangganan kembali lebih besar ketimbang pelanggan yang menggunakan layanan internet namun tidak menggunakan keamanan online

**Online Backup vs Churn**
"""

# variabel 'OnlineBackup' vs 'Churn'
g = sns.FacetGrid(
    data = prop_agg(X_train, "OnlineBackup","Churn"),
    col = "OnlineBackup"
)
g.map(sns.barplot, "Churn", "prop");

"""**Interpretasi**

Diketahui bahwa untuk kategori churn terhadap variabel online backup memiliki proporsi yang berbeda.
Pelanggan yang tidak menggunakan layanan internet memiliki presentase lebih kecil untuk tidak berlangganan kembali 
Jika di bandingkan dengan pelanggan yang menggunakan layanan internet maka pelanggan yang menggunakan layanan backup online akan memiliki presentase untuk berlangganan kembali lebih besar ketimbang pelanggan yang menggunakan layanan internet namun tidak menggunakan layanan backup online

**Device Protection vs Churn**
"""

# variabel 'Device Protection' vs 'Churn'
g = sns.FacetGrid(
    data = prop_agg(X_train, "DeviceProtection", "Churn"),
    col = "DeviceProtection"
)
g.map(sns.barplot, "Churn", "prop");

"""**Interpretasi**

Diketahui bahwa untuk kategori churn terhadap variabel device protection memiliki proporsi yang berbeda.
Pelanggan yang tidak menggunakan layanan internet memiliki presentase lebih kecil untuk tidak berlangganan kembali 
Jika di bandingkan dengan pelanggan yang menggunakan layanan internet maka pelanggan yang menggunakan device protection akan memiliki presentase untuk berlangganan kembali lebih besar ketimbang pelanggan yang menggunakan layanan internet namun tidak menggunakan device protection

**Streaming TV vs Churn**
"""

# variabel 'Streaming TV' vs 'Churn'
g = sns.FacetGrid(
    data = prop_agg(X_train, "StreamingTV","Churn"),
    col = "StreamingTV"
)
g.map(sns.barplot, "Churn", "prop");

"""**Interpretasi**

Diketahui bahwa untuk kategori churn terhadap variabel streaming tv memiliki proporsi yang berbeda.
Pelanggan yang tidak menggunakan layanan internet memiliki presentase lebih kecil untuk tidak berlangganan kembali 
Jika di bandingkan dengan pelanggan yang menggunakan layanan internet maka pelanggan yang menggunakan layanan Streaming TV akan memiliki presentase untuk berlangganan kembali lebih besar ketimbang pelanggan yang menggunakan layanan internet namun tidak menggunakan layanan Streaming TV

**Streaming Movies vs Churn**
"""

# variabel 'Streaming Movies' vs 'Churn'
g = sns.FacetGrid(
    data = prop_agg(X_train, "StreamingMovies","Churn"),
    col = "StreamingMovies"
)
g.map(sns.barplot, "Churn", "prop");

"""**Interpretasi**
Diketahui bahwa untuk kategori churn terhadap variabel streaming movies memiliki proporsi yang berbeda.
Pelanggan yang tidak menggunakan layanan internet memiliki presentase lebih kecil untuk tidak berlangganan kembali 
Jika di bandingkan dengan pelanggan yang menggunakan layanan internet maka pelanggan yang menggunakan layanan Streaming Movies akan memiliki presentase untuk berlangganan kembali lebih besar ketimbang pelanggan yang menggunakan layanan internet namun tidak menggunakan layanan Streaming Movies

**Contract vs Churn**
"""

# variabel 'Contract' vs 'Churn'
g = sns.FacetGrid(
    data = prop_agg(X_train, "Contract", "Churn"),
    col = "Contract"
)
g.map(sns.barplot, "Churn", "prop");

"""**Interpretasi**

Diketahui bahwa untuk kategori churn terhadap variabel conract memiliki proporsi yang berbeda.
Pelanggan yang memiliki kontrak langganan perbulan lebih cenderung memiliki presentase untuk tidak menggunakan layanan produk kembali jika dibangingkan dengan kontrak berdurasi 1 tahun atau 2 tahunan maka kontrak berdurasi 1 tahun atau 2 tahun memiliki presentase berlangganan kembali yang lebih tinggi

**Tech Support vs Churn**
"""

# variabel 'Tech Support' vs 'Churn'
g = sns.FacetGrid(
    data = prop_agg(X_train, "TechSupport", "Churn"),
    col = "TechSupport"
)
g.map(sns.barplot, "Churn", "prop");

"""**Interpretasi**

Diketahui bahwa untuk kategori churn terhadap variabel tech support memiliki proporsi yang berbeda.
Pelanggan yang tidak menggunakan layanan internet memiliki presentase lebih kecil untuk tidak berlangganan kembali 
Jika di bandingkan dengan pelanggan yang menggunakan layanan internet maka pelanggan yang menggunakan layanan tech support akan memiliki presentase untuk berlangganan kembali lebih besar ketimbang pelanggan yang menggunakan layanan internet namun tidak menggunakan layanan tech support

**Paperless Billing vs Churn**
"""

# variabel 'PaperlessBilling' vs 'Churn'
g = sns.FacetGrid(
    data = prop_agg(X_train, "PaperlessBilling", "Churn"),
    col = "PaperlessBilling"
)
g.map(sns.barplot, "Churn", "prop");

"""**Interpretasi**

Diketahui bahwa untuk kategori churn terhadap variabel paapelessbilling memiliki proporsi yang berbeda.
Pelanggan yang menggunakan metode paperlessbilling memiliki presentase untuk tidak kembali berlangganan yang lebih besar ketimbang pelanggan yang tidak menggunakan metode paperlessbilling

**Payment Method vs Churn**
"""

# variabel 'Payment Method' vs 'Churn'
g = sns.FacetGrid(
    data = prop_agg(X_train, "PaymentMethod", "Churn"),
    col = "PaymentMethod"
)
g.map(sns.barplot, "Churn", "prop");

"""**Interpretasi**

Diketahui bahwa untuk kategori churn terhadap variabel payment method memiliki proporsi yang berbeda.
Pelanggan yang metode pembayaran dengan automatic (bank transfer dan credit card) memiliki presentase yang lebih besar untuk berlangganan kembali ketimbang pelanggan yang menggunakan metode pembayaran selain automatic

**Phone Service vs Churn**
"""

# variabel 'Phone Service' vs 'Churn'
g = sns.FacetGrid(
    data = prop_agg(X_train, "PhoneService", "Churn"),
    col = "PhoneService"
)
g.map(sns.barplot, "Churn", "prop");

"""**Interpretasi**

Diketahui bahwa untuk kategori churn terhadap variabel phone service memiliki proporsi yang hampir mirip dan sama.
Pelanggan yang tidak menggunakan layanan phoneservice dan yang menggunakan layanan phoneservice memiliki proporsi churn yang sama.

**Internet Service vs Churn**
"""

# variabel 'Internet Service' vs 'Churn'
g = sns.FacetGrid(
    data = prop_agg(X_train, "InternetService", "Churn"),
    col = "InternetService"
)
g.map(sns.barplot, "Churn", "prop");

"""**Interpretasi**

Diketahui bahwa untuk kategori churn terhadap variabel internet service memiliki proporsi yang berbeda.
Pelanggan yang tidak menggunakan layanan internet memiliki presentase lebih kecil untuk tidak berlangganan kembali 
Jika di bandingkan dengan pelanggan yang menggunakan layanan internet maka pelanggan yang menggunakan layanan DSL akan memiliki presentase untuk berlangganan kembali lebih besar ketimbang pelanggan yang menggunakan layanan internet namun menggunakan layanan Fiber optic

## Numerical Data vs Churn

**Total Charges vs Churn**
"""

# variabel 'Total Charges vs Churn'
sns.boxplot(data = X_train, x ='Churn', y = 'TotalCharges');

"""**Interoretasi**

Diketahui bahwa untuk kategori churn terhadap variabel total charges
Pelanggan yang churn (tidak menggunakan product kembali) memiliki nilai totalcharges yang lebih rendah jika di bandingkan dengan pelanggan yang tetap menggunakan product kembali yang nilai totalcharges nya jauh lebih besar

**Monthly Charges vs Churn**
"""

# variabel 'Monthly Charges vs Churn'
sns.boxplot(data = X_train, x ='Churn', y = 'MonthlyCharges');

"""**Interpretasi**

Diketahui bahwa untuk kategori churn terhadap variabel mothnly charges
Pelanggan yang churn (tidak menggunakan product kembali) secara median memiliki nilai monthly charges yang lebih tinggi jika di bandingkan dengan pelanggan yang tetap menggunakan product kembali yang nilai monthly charges nya jauh lebih kecil

**Tenure**
"""

# variabel 'Monthly Charges vs Churn'
sns.boxplot(data = X_train, x ='Churn', y = 'tenure');

"""**Interpretasi**

Diketahui bahwa untuk kategori churn terhadap variabel tenure
Pelanggan yang churn (tidak menggunakan product kembali) secara median memiliki nilai tenure yang lebih rendah jika di bandingkan dengan pelanggan yang tetap menggunakan product kembali yang nilai tenure jauh lebih besar

---

# Modeling

## Define Model

## Soal 4

Buatlah model dengan 5 model dengan setting parameter berikut:

- KNN
  - jumlah neighbors: 5
- Decision tree
  - max depth = 5
  - cpp_alpha = 0.001
- Random Forest
  - random state = 1000
  - total estimators = 1000
- SVM RBF
  - probability = True
  - random state = 1000
- XGBoost
  - random state = 1000
  - total estimator = 1000

**Check Before Modeling**
"""

print(X_test.shape)
X_test.dtypes

print(X_train.shape)
X_train.dtypes

X_train = X_train.drop('Churn', axis = 1)

y_test.dtype

y_train.dtype

y_train = y_train.astype(str)
y_test = y_test.astype(str)



**KNN**

"""KNeighborsClassifier(n_neighbors=5, *,weights='uniform', algorithm='auto', leaf_size=30, p=2, metric='minkowski', metric_params=None, n_jobs=None)"""

# definisikan model kNN
knn_model = KNeighborsClassifier(n_neighbors=5)



"""**Decision Tree**

DecisionTreeClassifier(*, criterion='gini', splitter='best', max_depth=5, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=None, random_state=None, max_leaf_nodes=None, min_impurity_decrease=0.0, class_weight=None, ccp_alpha=0.001)
"""

# definisikan model decision tree
dt_model = DecisionTreeClassifier(max_depth=5,ccp_alpha=0.001 )



"""**Random Forest**

RandomForestClassifier(n_estimators=1000, *, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='sqrt', max_leaf_nodes=None, min_impurity_decrease=0.0, bootstrap=True, oob_score=False, n_jobs=None, random_state=1000, verbose=0, warm_start=False, class_weight=None, ccp_alpha=0.0, max_samples=None
"""

# definisikan model random forest
rf_model = RandomForestClassifier(n_estimators = 1000, random_state=1000)



"""**SVM RBF**

SVC(*, C=1.0, kernel='rbf', degree=3, gamma='scale', coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape='ovr', break_ties=False, random_state=None)
"""

# definisikan model random forest
sv_model = SVC(probability=True, random_state = 1000)



"""**XGBoost**

XGBClassifier(max_depth=None, max_leaves=None, max_bin=None, grow_policy=None, learning_rate=None, n_estimators=1000, verbosity=None, objective=None, booster=None, tree_method=None, n_jobs=None, gamma=None, min_child_weight=None, max_delta_step=None, subsample=None, sampling_method=None, colsample_bytree=None, colsample_bylevel=None, colsample_bynode=None, reg_alpha=None, reg_lambda=None, scale_pos_weight=None, base_score=None, random_state=1000, missing=nan, num_parallel_tree=None, monotone_constraints=None, interaction_constraints=None, importance_type=None, gpu_id=None, validate_parameters=None, predictor=None, enable_categorical=False, feature_types=None, max_cat_to_onehot=None, max_cat_threshold=None, eval_metric=None, early_stopping_rounds=None, callbacks=Nones)
"""

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_train = le.fit_transform(y_train)

y_test = y_test.astype(y_train)

# definisikan model random forest
xg_model = XGBClassifier(n_estimators = 1000, random_state=1000)



"""## Fitting Model to Data

**KNN**
"""

# fit model dengan data X_train dan y_train
knn_model.fit(X_train, y_train)
# hasilkan hard prediction dari KNN menggunakan X_test
knn_result = knn_model.predict(X_test)
# hasilkan probability prediction dari KNN menggunakan X_test
knn_proba = knn_model.predict_proba(X_test)

"""**Decision Tree**"""

# fit model dengan data X_train dan y_train
dt_model.fit(X_train, y_train)
# hasilkan hard prediction dari dt_model menggunakan X_test
dt_result = dt_model.predict(X_test)
# hasilkan probability prediction dari dt_model menggunakan X_test
dt_proba = dt_model.predict_proba(X_test)

"""**Random Forest**"""

# fit model dengan data X_train dan y_train
rf_model.fit(X_train, y_train)
# hasilkan hard prediction dari rf_model menggunakan X_test
rf_result = dt_model.predict(X_test)
# hasilkan probability prediction dari rf_model menggunakan X_test
rf_proba = rf_model.predict_proba(X_test)

"""**SVM RBF**"""

# fit model dengan data X_train dan y_train
sv_model.fit(X_train, y_train)
# hasilkan hard prediction dari rf_model menggunakan X_test
sv_result = sv_model.predict(X_test)
# hasilkan probability prediction dari rf_model menggunakan X_test
sv_proba = sv_model.predict_proba(X_test)

"""**XGBoost**"""

# fit model dengan data X_train dan y_train
xg_model.fit(X_train, y_train)
# hasilkan hard prediction dari rf_model menggunakan X_test
xg_result = xg_model.predict(X_test)
# hasilkan probability prediction dari rf_model menggunakan X_test
xg_proba = xg_model.predict_proba(X_test)

"""## Model Evaluation

---

## Soal 5

Lakukan evaluasi pada semua model di atas dan interpretasi hasil dari model. Pilih model terbaik berdasarkan hasil evaluasi

**KNN Evaluation**

**Confusion Matrix**
"""

# check confusion matrix
skplt.metrics.plot_confusion_matrix(y_test, knn_result, figsize=(5,5));

"""**Classification Report**"""

# Evaluasi model KNN
pd.DataFrame(metrics.classification_report(y_test, knn_result, target_names = ['Not Left', 'Left'], output_dict=True))

"""**ROC Curve**"""

# Evaluasi model KNN menggunakan ROC AUC
skplt.metrics.plot_roc_curve(y_test, knn_proba, figsize=(5,5));

"""**Decision Tree Evaluation**

**Confusion Matrix**
"""

# check confusion matrix
skplt.metrics.plot_confusion_matrix(y_test, dt_result, figsize=(5,5));

"""**Classification Report**"""

# Evaluasi model Decission Tree
pd.DataFrame(metrics.classification_report(y_test, dt_result, target_names = ['Not Left', 'Left'], output_dict=True))

"""**ROC Curve**"""

# Evaluasi model Random Forest menggunakan ROC AUC
skplt.metrics.plot_roc_curve(y_test, dt_proba, figsize=(5,5));

"""**Random Forest**

**Confusion Matrix**
"""

# check confusion matrix
skplt.metrics.plot_confusion_matrix(y_test, rf_result, figsize=(5,5));

"""**Classification Report**"""

# Evaluasi model Random Forest
pd.DataFrame(metrics.classification_report(y_test, rf_result, target_names = ['Not Left', 'Left'], output_dict=True))

"""**ROC Curve**"""

# Evaluasi model Random Forest menggunakan ROC AUC
skplt.metrics.plot_roc_curve(y_test, rf_proba, figsize=(5,5));

"""**SVM RBF**

**Confusion Matrix**
"""

y_test = y_test.astype(int)

# check confusion matrix
skplt.metrics.plot_confusion_matrix(y_test, sv_result, figsize=(5,5));

"""**Classification Repport**"""

# Evaluasi model Knn
pd.DataFrame(metrics.classification_report(y_test, sv_result, target_names = ['Not Left', 'Left'], output_dict=True))

"""**ROC Curve**"""

# Evaluasi model logistic regression menggunakan ROC AUC
skplt.metrics.plot_roc_curve(y_test, sv_proba, figsize=(5,5));

"""**XGBoost**

**Confussion Matrix**
"""

# check confusion matrix
skplt.metrics.plot_confusion_matrix(y_test, xg_result, figsize=(5,5));

"""**Classification Report**"""

# Evaluasi model Knn
pd.DataFrame(metrics.classification_report(y_test, xg_result, target_names = ['Not Left', 'Left'], output_dict=True))

"""**ROC Curve**"""

# Evaluasi model logistic regression menggunakan ROC AUC
skplt.metrics.plot_roc_curve(y_test, xg_proba, figsize=(5,5));

"""** Interpretasi**

Dari Ke 5 Model, Model KNN merupakan model dengan nilai F1-score yang lebih baik di bandingkan model lainnya

**Hyperparameter Tuning**
"""

import sklearn

from sklearn.model_selection import RandomizedSearchCV

knn_param = { 
    'n_neighbors' : [5,7,9,11,13,15],
    'weights' : ['uniform','distance'],
    'metric' : ['minkowski','euclidean','manhattan']
}

# Menggunakan Model Terbaik
# define decision KNN classifier
knn_clf = KNeighborsClassifier()

"""sklearn.model_selection.RandomizedSearchCV(
  estimator, 
  *,
  param_distributions,  
  n_iter=10, 
  scoring=None, 
  n_jobs=None, 
  refit=True, 
  cv=None, 
  verbose=0, 
  pre_dispatch='2*n_jobs', 
  random_state=None, 
  error_score=nan, 
  return_train_score=False
)
"""

# definisikan model dengan RandomizedSearchCV
random_search_knn = RandomizedSearchCV(
    estimator=knn_clf, 
    param_distributions=knn_param, 
    n_jobs=1, 
    verbose=1,
    n_iter = 5,
    cv = 5,
    scoring = "f1"
)

# fit model dengan random search CV
random_search_knn.fit(X_train, y_train)



# Score pada KNN
score_df_knn = pd.DataFrame(random_search_knn.cv_results_)
score_df_knn.nlargest(5,"mean_test_score")

# check the best estimator
random_search_knn.best_estimator_

# assign the best estimator to new variable
knn_best_rn = random_search_knn.best_estimator_

# hasilkan hard prediction dari knn_model menggunakan X_test
knn_rn_result = knn_best_rn.predict(X_test)

# visualisasikan confusion matrix model yang dibuat dengan RandomSearchCV
skplt.metrics.plot_confusion_matrix(y_test, knn_rn_result);

# visualisasikan confusion matrix model yang dibuat tanpa CV
skplt.metrics.plot_confusion_matrix(y_test, knn_result);

**Interpretasi**

Dengan dilakukan Hyperparameter Tuning diketahui bahwa model KNN dengan jumlah neighbors = 5 
merupakan model terbaik setelah dibandingkan dengan semua model yang ada 
Sehingga digunakanlah model KNN dengan jumlah neighbors = 5 untuk melakukan permodelan

"""## Soal 6

Berdasarkan model terbaik, gunakan evaluasi metrik lainnya:
- lift curve
- cummulative gain curve
- profit curve

Khusus untuk profit curve, buatlah matriks profit sebagai berikut:

Kita akan mengeluarkan `$150` dolar jika bisa me-retain mereka yang akan churn (dalam bentuk promosi, marketing, dll). Jika kita dapat memprediksi dengan tepat mereka yang akan pergi dan mampu me-retain mereka kembali, maka kita akan memperoleh keuntungan berdasarkan lifetime value dikurangi biaya retain (`$325` - `$150`).

Ambil desil 20% sebagai acuan untuk menilai seberapa baik performa model.

**Lift Curve**
"""

skplt.metrics.plot_lift_curve(y_test, knn_proba)

"""**Cummulative Gain Curve**"""

skplt.metrics.plot_cumulative_gain(y_test, knn_proba)

**Interpretasi**

Denga menggunakan desil 20% maka berdasarkan grafik dapat diketahui bahwa model dapat memprediksi dengan baik sebesar 40%

"""**Profit Curve**"""

# membuat confusion matrix untuk perhitungan cost-benefit
def standard_confusion_matrix(y_true, y_pred):
    [[tn, fp], [fn, tp]] = metrics.confusion_matrix(y_true, y_pred)
    return np.array([[tp, fp], [fn, tn]])

# visualisasikan profit curve
# parameter 1: objek model
# parameter 2: matrix cost-benefit
# parameter 3: nilai probabilitas untuk kelas positif
# parameter 4: nilai y sebenarnya
def plot_profit_curve(model_object, costbenefit_mat, y_proba, y_test):

    # Profit curve data
    profits = []
    thresholds = sorted(y_proba, reverse=True)

    # Untuk tiap threshold, hitung profit - mulai dari threshold terbesar
    for T in thresholds:
        y_pred = (y_proba > T).astype(int)
        confusion_mat = metrics.confusion_matrix(y_test, y_pred)
        # hitung total profit dari threshold berikut
        profit = sum(sum(confusion_mat * costbenefit_mat)) / len(y_test)
        profits.append(profit)
    
    # visualisasikan profit curve
    model_name = model_object.__class__.__name__
    max_profit = max(profits)
    plt.plot(np.linspace(0, 1, len(y_test)), profits, label = '{}, max profit ${:.2f} per user'.format(model_name, max_profit))

# create cost benefit matrix
costbenefit_mat = np.array([[0, -325],
                            [(-150), (325-150)]])

# check cost benefit matrix
costbenefit_mat

y_test = y_test.astype(int)
y_train = y_train.astype(int)

# check model confusion matrix
metrics.confusion_matrix(y_test, knn_result)

plot_profit_curve(knn_result, costbenefit_mat, knn_proba[:,1], y_test)

**Interpretasi**

Dari grafik diketahui bahwa dengan desil 20 % 
maka kita akan mengalami kerugian di bandingkan dengan kita mengambil desil lebih dari 20 %