## install the required library 
# pip install kmodes

from flask_pymongo import ASCENDING
from matplotlib import pyplot as plt
import pandas as pd
from kmodes.kmodes import KModes

### read the csv file into Pandas CSV file
df_customers = pd.read_csv("customers.csv")
df_line_items = pd.read_csv("line_items.csv")
df_orders = pd.read_csv("orders.csv")



## Lets start by running some  EDA first over the data

### What are states with top shipping cost?
report1 = df_orders[['ship_state','shipping_cost']].groupby('ship_state').mean('shipping_cost')
print(report1.sort_values(by='shipping_cost',ascending=False).head())

### What are states with most return items?
report2 = df_orders[df_orders['returned']==True].groupby('ship_state').count()
print(report2['returned'].sort_values(ascending=False).head())

### What are most sold item in each state?
report2 = pd.merge( df_line_items[['product_category','color','size','order_id']] , df_orders[['order_id','ship_state']])
print(report2.groupby(['ship_state','product_category','color','size']).count().sort_values(by='order_id',ascending=False))


## We can run segmentation over customers accoriding to some features collected
df_customers_list = pd.merge ( pd.merge(df_customers,df_orders, on='customer_uid') , df_line_items, on='order_id')
df_customers_list_selected_columns = df_customers_list[['product_category','color','size','acquisition_channel','ship_state','returned','is_business','has_account']] ## ,'returned','is_business','has_account'
print(df_customers_list_selected_columns.head())


### run segemntation over the data using k-mode algorithm
### we need to run kmode because are data columns are categorial



mark_array=df_customers_list_selected_columns.values
categorical_features_idx = [i for i in range(8)]

MAX_ITERATION = 10
cost = []
K = range(1,MAX_ITERATION)
for num_clusters in list(K):
    kmode = KModes(n_clusters=num_clusters, init = "random", n_init = 5, verbose=1)   
    kmode.fit_predict(mark_array,categorical=categorical_features_idx)
    cost.append(kmode.cost_)


plt.plot(K, cost, 'bx-')
plt.xlabel('No. of clusters')
plt.ylabel('Cost')
plt.title('Elbow Method For Optimal k')
plt.show()


