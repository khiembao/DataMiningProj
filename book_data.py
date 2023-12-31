# -*- coding: utf-8 -*-
"""book_data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MeTsQBKc81lRceXkQEWKmiAfuXpxdhUC
"""



import pandas as pd

df_book = pd.read_csv("/content/drive/MyDrive/KPDL/BTL/books.csv")

df_book = df_book.drop('Unnamed: 0', axis = 1)

df_book = df_book[['product_id','current_price', 'quantity', 'category', 'n_review', 'avg_rating', 'manufacturer']]
df_book

a = df_book.sort_values(by=['quantity'], ascending=False)
a

df_book = df_book.drop(121)

df_book['quantity'].max()

min_quan = df_book['quantity'].min()
max_quan = df_book['quantity'].max()
df_book['quantity_new'] = ((df_book[['quantity']] -min_quan)) /(max_quan -min_quan).round(3)
df_book

min_price = df_book['current_price'].min()
max_price = df_book['current_price'].max()
df_book['current_price_new'] = ((df_book[['current_price']] -min_price)) /(max_price -min_price).round(3)
df_book

min_review = df_book['n_review'].min()
max_review = df_book['n_review'].max()
df_book['n_review_new'] = ((df_book[['n_review']] -min_review)) /(max_review -min_review).round(3)
df_book

min_rating = df_book['avg_rating'].min()
max_rating = df_book['avg_rating'].max()
df_book['avg_rating_new'] = ((df_book[['avg_rating']] -min_rating)) /(max_rating -min_rating).round(3)
df_book

# Thống kê tần suất xuất hiện
frequency_table = df_book['manufacturer'].value_counts().sort_index().reset_index()
frequency_table.columns = ['manufacturer', 'Tần suất xuất hiện']

# Tính giá trị nhỏ nhất
min_frequency = frequency_table['Tần suất xuất hiện'].min()
# Tính giá trị lớn nhất
max_frequency = frequency_table['Tần suất xuất hiện'].max()

frequency_table['Tần suất xuất hiện'] = frequency_table['Tần suất xuất hiện'].apply(lambda x: (x-min_frequency)/(max_frequency-min_frequency)).round(4)
frequency_table

data_new = df_book.merge(frequency_table[['manufacturer', 'Tần suất xuất hiện']], on='manufacturer')
data_new = data_new.rename(columns={'Tần suất xuất hiện':'manufacturer_new'})
data_new['manufacturer_new'] = 1 - data_new['manufacturer_new']

# Thống kê tần suất xuất hiện
frequency_table_cate = df_book['category'].value_counts().sort_index().reset_index()

frequency_table_cate.columns = ['category', 'cate_freq']

frequency_table_cate

# Tính giá trị nhỏ nhất
min_frequency_cate = frequency_table_cate['cate_freq'].min()
# Tính giá trị lớn nhất
max_frequency_cate = frequency_table_cate['cate_freq'].max()

frequency_table_cate['cate_freq'] = frequency_table_cate['cate_freq'].apply(lambda x: (x-min_frequency_cate)/(max_frequency_cate-min_frequency_cate)).round(4)

frequency_table_cate

data_new = data_new.merge(frequency_table_cate[['category', 'cate_freq']], on='category')
data_new = data_new.rename(columns={'cate_freq':'cate_freq_new'})

data_new['cate_freq_new'] = 1 - data_new['cate_freq_new']

data_new

data_new = data_new[["current_price_new","quantity_new","cate_freq_new","n_review_new" ,"avg_rating_new","manufacturer_new",]]
# data_new.to_csv('/content/drive/MyDrive/KPDL/BTL/Datanew.csv')

data_new

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import cluster


max_clusters = 10
sse = []
for k in range(1, max_clusters + 1):
  kmeans = KMeans(n_clusters=k, random_state=42)
  kmeans.fit(data_new)
  sse.append(kmeans.inertia_)

plt.plot(range(1, max_clusters + 1), sse, marker = 'o')
plt.xlabel('Số lượng cụm')
plt.ylabel('SSE')
plt.title('Phương pháp Elbow')
plt.show()

data_new['KQ'] = data_new.sum(axis=1)

data_new

# Commented out IPython magic to ensure Python compatibility.
import seaborn as sns
# %matplotlib inline
g = sns.relplot(
data = data_new,
x = 'KQ',
y = 'quantity_new',
aspect= 3,
height = 3,
hue = 'avg_rating_new')
g.ax.set_xlabel('Sự chênh lệch khoảng cách bằng phép toán Manhattan')
g.ax.set_ylabel('Tỷ lệ của số lượng sản phẩm bán ra')
g.fig.suptitle('Biểu đồ')

# Gom cụm bằng phương pháp K-Means
from sklearn.cluster import KMeans
from sklearn import cluster
import matplotlib.pyplot as plt

#Phân thành 4 cụm
kmeans = KMeans(n_clusters= 5)

#Tạo tọa độ
data_ToaDo = data_new[['KQ','quantity_new']]

# Nạp tọa độ
kmeans.fit(data_ToaDo)

# Lấy trung tâm của các cụm
centers = kmeans.cluster_centers_
centers.round(4)

25
#Phân vùng bằng thư viện của K-Means
labels = kmeans.labels_
# Vẽ biểu đồ dữ liệu
plt.figure(figsize = (15,5))
plt.scatter(data_new['KQ'], data_new['quantity_new'], c = labels)
plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='x', s = 100)
plt.xlabel('KQ')
plt.ylabel('quantity_new')
plt.show()

# Tạo Class
data_new['PhanLoai'] = labels
data_new['PhanLoai'] = data_new['PhanLoai'].replace({0: 'Top Seller', 1: 'Bán chạy', 2: 'Bán vừa',
3: 'Bán thấp', 4:'Bán tệ'})

# Sử dụng phương pháp KNN dựa trên Class
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report,confusion_matrix

# Phương pháp split test: lấy 20% dữ liệu ban đầu để test
train_df, test_df = train_test_split(data_new, test_size= 0.3, random_state = 42)
knn_model = KNeighborsClassifier( n_neighbors= 9)

knn_model.fit(train_df[["current_price_new","quantity_new","cate_freq_new","n_review_new","avg_rating_new","manufacturer_new","KQ"]],train_df["PhanLoai"])
knn_prediction = knn_model.predict(test_df[["current_price_new","quantity_new","cate_freq_new","n_review_new","avg_rating_new","manufacturer_new","KQ"]])

print("Confusion matrix: ")
print(confusion_matrix(test_df["PhanLoai"],knn_prediction))
print("KNN Classification Report: ")
print(classification_report(test_df["PhanLoai"],knn_prediction))

nb_model = GaussianNB()

nb_model.fit(train_df[["current_price_new","quantity_new","cate_freq_new",
"n_review_new","avg_rating_new","manufacturer_new","KQ"]], train_df["PhanLoai"])

nb_predicious = nb_model.predict(test_df[["current_price_new","quantity_new","cate_freq_new","n_review_new","avg_rating_new","manufacturer_new","KQ"]])

print("Confusion matrix: ")
print(confusion_matrix(test_df["PhanLoai"],nb_predicious))
print("Navie-Bayes Classitification Report: ")
print(classification_report(test_df["PhanLoai"], nb_predicious))