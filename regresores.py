import pandas as pd 
import os 
from datetime import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDRegressor
from sklearn.model_selection import cross_validate
from sklearn.gaussian_process.kernels import RBF
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import mean_squared_error, r2_score
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.data_utils import load_csv
import tensorflow as tf
from tflearn.layers.conv import conv_1d, global_max_pool
from tflearn.layers.merge_ops import merge
from tflearn.layers.estimator import regression
from sklearn.metrics import r2_score


# LECTURA DE LOS DATOS
data = pd.read_csv('lecturas2.dat', sep=" ", header=None, names=["lat_hip","lon_hip","prof_hip","sta_name","lat_sta","lon_sta","elev_sta","t_p","t_s" ])

data = data.drop(columns="sta_name")

data.describe()

data.info()

# SEPARACIÓN DE CARACTERÍSTICAS
features = data.loc[:, :"t_p"]

y = data["t_s"]


X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.1,random_state=42)

# SCALER PARA LAS CARACTERISTICAS
scaler = StandardScaler()
scaler.fit(features)  
transformed_X = scaler.transform(features)


#PRIMER CLASIFICADOR
classifier1 = SGDRegressor(loss="huber", penalty="elasticnet",max_iter=100, tol=1e-3)

scoring=['explained_variance','neg_mean_absolute_error','neg_mean_squared_error','neg_mean_squared_log_error','neg_median_absolute_error','r2']

cv_results = cross_validate(classifier1,transformed_X, y, cv = 10, n_jobs=10, scoring = scoring, return_train_score= True)

print('explained_variance:', np.mean(cv_results['test_explained_variance']))
print('neg_mean_absolute_error:', np.mean(cv_results['test_neg_mean_absolute_error']))
print('neg_mean_squared_error:', np.mean(cv_results['test_neg_mean_squared_error']))
print('neg_mean_squared_log_error:', np.mean(cv_results['test_neg_mean_squared_log_error']))
print('neg_median_absolute_error:', np.mean(cv_results['test_neg_median_absolute_error']))
print('r2:', np.mean(cv_results['test_r2']))


#SCALAR PARA TESTING, CASO PARTICULAR
scaler2 = StandardScaler()
scaler2.fit(X_train)  
transformed_X_train = scaler.transform(X_train)
transformed_X_test = scaler.transform(X_test)


classifier1.fit(transformed_X_train,y_train)

preds1 = classifier1.predict(transformed_X_test)

print("score: %.5f" %(classifier1.score(transformed_X_test,y_test)))

print("Error cuadratico medio: %.5f" % mean_squared_error( y_test, preds1 ))


# GRAFICOS COMPARATIVOS
y_reg = y_test.tolist()

plt.rcParams["figure.figsize"] = (20,10)
plt.plot(preds1[1:500])
plt.plot(y_reg[1:500])
plt.xlabel('Datos')
plt.ylabel('Tiempo [s]')
plt.legend(['predicciones', 'datos'], loc='upper left')
plt.show()


plt.rcParams["figure.figsize"] = (20,10)
plt.plot(preds1[501:1000])
plt.plot(y_reg[501:1000])
plt.xlabel('Datos')
plt.ylabel('Tiempo [s]')
plt.legend(['predicciones', 'datos'], loc='upper left')
plt.show()

plt.rcParams["figure.figsize"] = (20,10)
plt.plot(preds1[1001:1500])
plt.plot(y_reg[1001:1500])
plt.xlabel('Datos')
plt.ylabel('Tiempo [s]')
plt.legend(['predicciones', 'datos'], loc='upper left')
plt.show()




# KERNEL GAUSSIANO

rbf_kernel = RBF(length_scale=10)  
ker_regr_rbf = KernelRidge(kernel=rbf_kernel)


cv_results2 = cross_validate(ker_regr_rbf,transformed_X, y, cv = 10,  n_jobs=10, scoring = scoring, return_train_score= True)

print('explained_variance:', np.mean(cv_results2['test_explained_variance']))
print('neg_mean_absolute_error:', np.mean(cv_results2['test_neg_mean_absolute_error']))
print('neg_mean_squared_error:', np.mean(cv_results2['test_neg_mean_squared_error']))
print('neg_mean_squared_log_error:', np.mean(cv_results2['test_neg_mean_squared_log_error']))
print('neg_median_absolute_error:', np.mean(cv_results2['test_neg_median_absolute_error']))
print('r2:', np.mean(cv_results['test_r2']))


scaler2 = StandardScaler()
scaler2.fit(X_train)  
transformed_X_train = scaler.transform(X_train)
transformed_X_test = scaler.transform(X_test)


rbf_kernel = RBF(length_scale=10)  
ker_regr_rbf = KernelRidge(kernel=rbf_kernel)

ker_regr_rbf.fit(transformed_X_train,y_train)

ker_rbf_pred = ker_regr_rbf.predict(transformed_X_test)

print("score: %.5f" %( ker_regr_rbf.score(transformed_X_test,y_test) ))
print("Error cuadratico medio: %.5f" % mean_squared_error( y_test, ker_rbf_pred ))


# GRAFICOS PARA COMPARAR
plt.rcParams["figure.figsize"] = (20,10)
plt.plot(ker_rbf_pred[1:500])
plt.plot(y_reg[1:500])
plt.xlabel('Datos')
plt.ylabel('Tiempo [s]')
plt.legend(['predicciones', 'datos'], loc='upper left')
plt.show()


plt.rcParams["figure.figsize"] = (20,10)
plt.plot(ker_rbf_pred[501:1000])
plt.plot(y_reg[501:1000])
plt.xlabel('Datos')
plt.ylabel('Tiempo [s]')
plt.legend(['predicciones', 'datos'], loc='upper left')
plt.show()


plt.rcParams["figure.figsize"] = (20,10)
plt.plot(ker_rbf_pred[1001:1500])
plt.plot(y_reg[1001:1500])
plt.xlabel('Datos')
plt.ylabel('Tiempo [s]')
plt.legend(['predicciones', 'datos'], loc='upper left')
plt.show()



# RED NEURONAL FULLY CONNECTED
datos = data.values
datos_X = datos[:,:-1].tolist()
datos_Y = datos[:,-1:].tolist()
X_train_TF, X_test_TF, y_train_TF, y_test_TF = train_test_split(datos_X, datos_Y, test_size=0.1,random_state=42)

scaler3 = StandardScaler()
scaler3.fit(X_train_TF)  
transformed_X_train_TF = scaler.transform(X_train_TF)
transformed_X_test_TF = scaler.transform(X_test_TF)


tf.reset_default_graph()

input_ = tflearn.input_data(shape=[None,7])

r1 = tflearn.fully_connected(input_,7)
r1 = tflearn.fully_connected(r1,6)
r1 = tflearn.fully_connected(r1,5)
r1 = tflearn.fully_connected(r1,4)
r1 = tflearn.fully_connected(r1,3)
r1 = tflearn.fully_connected(r1,2)
r1 = tflearn.fully_connected(r1,1)
r1 = tflearn.regression(r1, optimizer='adam', loss='mean_square')

m = tflearn.DNN(r1)
m.fit(transformed_X_train_TF,y_train_TF, n_epoch=30, show_metric=True, snapshot_epoch=False)



DNN_pred = m.predict(transformed_X_test_TF)
print("score: %.5f" %( r2_score( y_test_TF, DNN_pred ) ))
print("Error cuadratico medio: %.5f" % mean_squared_error( y_test_TF, DNN_pred ))


plt.rcParams["figure.figsize"] = (20,10)
plt.plot(DNN_pred[1:500])
plt.plot(y_test_TF[1:500])
plt.xlabel('Datos')
plt.ylabel('Tiempo [s]')
plt.legend(['predicciones', 'datos'], loc='upper left')
plt.show()


plt.rcParams["figure.figsize"] = (20,10)
plt.plot(DNN_pred[501:1000])
plt.plot(y_test_TF[501:1000])
plt.xlabel('Datos')
plt.ylabel('Tiempo [s]')
plt.legend(['predicciones', 'datos'], loc='upper left')
plt.show()

plt.rcParams["figure.figsize"] = (20,10)
plt.plot(DNN_pred[1001:1500])
plt.plot(y_test_TF[1001:1500])
plt.xlabel('Datos')
plt.ylabel('Tiempo [s]')
plt.legend(['predicciones', 'datos'], loc='upper left')
plt.show()


####################################################################################################
# SEGUNDA PARTE
####################################################################################################

data_S = pd.read_csv('lecturas_S.dat', sep=" ", header=None, names=["lat_hip","lon_hip","prof_hip","sta_name","lat_sta","lon_sta","elev_sta","t_s" ])

data_S = data_S.drop(columns="sta_name")

data_S.describe()
data_S.info()


features_S = data_S.loc[:, :"elev_sta"]

y_S = data_S["t_s"]


X_train_S, X_test_S, y_train_S, y_test_S = train_test_split(features_S, y_S, test_size=0.1,random_state=42)


scaler_S = StandardScaler()
scaler_S.fit(features_S)  
transformed_X_S = scaler_S.transform(features_S)



classifier1 = SGDRegressor(loss="huber", penalty="elasticnet",max_iter=1000, tol=1e-4)

scoring=['explained_variance','neg_mean_absolute_error','neg_mean_squared_error','neg_mean_squared_log_error','neg_median_absolute_error','r2']

cv_results = cross_validate(classifier1,transformed_X_S, y_S, cv = 10, n_jobs=10, scoring = scoring, return_train_score= True)

print('explained_variance:', np.mean(cv_results['test_explained_variance']))
print('neg_mean_absolute_error:', np.mean(cv_results['test_neg_mean_absolute_error']))
print('neg_mean_squared_error:', np.mean(cv_results['test_neg_mean_squared_error']))
print('neg_mean_squared_log_error:', np.mean(cv_results['test_neg_mean_squared_log_error']))
print('neg_median_absolute_error:', np.mean(cv_results['test_neg_median_absolute_error']))
print('r2:', np.mean(cv_results['test_r2']))



classifier1 = SGDRegressor(loss="huber", penalty="elasticnet",max_iter=1000, tol=1e-4)

scaler2_S = StandardScaler()
scaler2_S.fit(X_train_S)  
transformed_X_train_S = scaler2_S.transform(X_train_S)
transformed_X_test_S = scaler2_S.transform(X_test_S)

classifier1.fit(transformed_X_train_S,y_train_S)

preds1_S = classifier1.predict(transformed_X_test_S)

print("score: %.5f" %(classifier1.score(transformed_X_test_S,y_test_S)))

print("Error cuadratico medio: %.5f" % mean_squared_error( y_test_S, preds1_S ))


y_reg_S = y_test_S.tolist()

plt.rcParams["figure.figsize"] = (20,10)
plt.plot(preds1_S[1:500])
plt.plot(y_reg_S[1:500])
plt.xlabel('Datos')
plt.ylabel('Tiempo [s]')
plt.legend(['predicciones', 'datos'], loc='upper left')
plt.show()


# Kernel Gaussiano
rbf_kernel = RBF(length_scale=10)  
ker_regr_rbf = KernelRidge(kernel=rbf_kernel)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
cv_results2 = cross_validate(ker_regr_rbf,transformed_X_S, y_S, cv = 10, scoring = scoring, return_train_score= True)

print('explained_variance:', np.mean(cv_results2['test_explained_variance']))
print('neg_mean_absolute_error:', np.mean(cv_results2['test_neg_mean_absolute_error']))
print('neg_mean_squared_error:', np.mean(cv_results2['test_neg_mean_squared_error']))
print('neg_mean_squared_log_error:', np.mean(cv_results2['test_neg_mean_squared_log_error']))
print('neg_median_absolute_error:', np.mean(cv_results2['test_neg_median_absolute_error']))
print('r2:', np.mean(cv_results['test_r2']))


datos_S = data_S.values
datos_X_S = datos_S[:,:-1].tolist()
datos_Y_S = datos_S[:,-1:].tolist()
X_train_TF_S, X_test_TF_S, y_train_TF_S, y_test_TF_S = train_test_split(datos_X_S, datos_Y_S, test_size=0.1,random_state=42)

scaler3_S = StandardScaler()
scaler3_S.fit(X_train_TF_S)  
transformed_X_train_TF_S = scaler3_S.transform(X_train_TF_S)
transformed_X_test_TF_S = scaler3_S.transform(X_test_TF_S)

tf.reset_default_graph()

input_ = tflearn.input_data(shape=[None,6])

r1 = tflearn.fully_connected(input_,6)
r1 = tflearn.fully_connected(r1,1)
r1 = tflearn.regression(r1, optimizer='adam', loss='mean_square')

m = tflearn.DNN(r1)
m.fit(transformed_X_train_TF_S,y_train_TF_S, n_epoch=50, show_metric=True, snapshot_epoch=False)
DNN_pred_S = m.predict(transformed_X_test_TF_S)
print("score: %.5f" %( r2_score( y_test_TF_S, DNN_pred_S ) ))
print("Error cuadratico medio: %.5f" % mean_squared_error( y_test_TF_S, DNN_pred_S ))



from sklearn.ensemble import GradientBoostingRegressor

X_train_S, X_test_S, y_train_S, y_test_S = train_test_split(features_S, y_S, test_size=0.1,random_state=42)
scaler2_S = StandardScaler()
scaler2_S.fit(X_train_S)  
transformed_X_train_S = scaler2_S.transform(X_train_S)
transformed_X_test_S = scaler2_S.transform(X_test_S)

low_coef = 0.1
up_coef  = 0.9

lower_model = GradientBoostingRegressor(loss="quantile",alpha=low_coef,n_estimators=5000)
mid_model = GradientBoostingRegressor(loss="ls",n_estimators=5000)
upper_model = GradientBoostingRegressor(loss="quantile",alpha=up_coef,n_estimators=5000)

scoring=['explained_variance','neg_mean_absolute_error','neg_mean_squared_error','neg_mean_squared_log_error','neg_median_absolute_error','r2']

cv_results = cross_validate(mid_model,features_S, y_S, cv = 10, n_jobs=10, scoring = scoring, return_train_score= True)

print('explained_variance:', np.mean(cv_results['test_explained_variance']))
print('neg_mean_absolute_error:', np.mean(cv_results['test_neg_mean_absolute_error']))
print('neg_mean_squared_error:', np.mean(cv_results['test_neg_mean_squared_error']))
print('neg_mean_squared_log_error:', np.mean(cv_results['test_neg_mean_squared_log_error']))
print('neg_median_absolute_error:', np.mean(cv_results['test_neg_median_absolute_error']))
print('r2:', np.mean(cv_results['test_r2']))


mid_model.fit(transformed_X_train_S,y_train_S)

from sklearn.metrics import mean_squared_error, r2_score

preds1_S = mid_model.predict(transformed_X_test_S)

print("score: %.5f" %(mid_model.score(transformed_X_test_S,y_test_S)))

print("Error cuadratico medio: %.5f" % mean_squared_error( y_test_S, preds1_S ))

lower_model.fit(transformed_X_train_S,y_train_S)
upper_model.fit(transformed_X_train_S,y_train_S)

predictions_lower = lower_model.predict(transformed_X_test_S)
predictions_mid   = mid_model.predict(transformed_X_test_S)
predictions_upper = upper_model.predict(transformed_X_test_S)

predictions = y_test_S.tolist()
n_init=0
N_sam = 150
x=np.linspace(n_init+1,N_sam+n_init,N_sam)

plt.rcParams["figure.figsize"] = (20,10)
plt.plot(x,predictions[n_init:N_sam+n_init],linewidth=2.0, color='red')
plt.plot(x,predictions_mid[n_init:N_sam+n_init],linewidth=1.0, color='blue')
plt.plot(x,predictions_lower[n_init:N_sam+n_init], color='gray',alpha=0.4)
plt.plot(x,predictions_upper[n_init:N_sam+n_init], color='gray',alpha=0.4)
plt.fill_between(x, predictions_lower[n_init:N_sam+n_init],predictions_upper[n_init:N_sam+n_init], color='gray',alpha=0.4)
plt.legend(['Datos', 'predicción','Rango']);
plt.show()

predictions = y_test_S.tolist()
n_init=151
N_sam = 150
x=np.linspace(n_init+1,N_sam+n_init,N_sam)

plt.rcParams["figure.figsize"] = (20,10)
plt.plot(x,predictions[n_init:N_sam+n_init],linewidth=2.0, color='red')
plt.plot(x,predictions_mid[n_init:N_sam+n_init],linewidth=1.0, color='blue')
plt.plot(x,predictions_lower[n_init:N_sam+n_init], color='gray',alpha=0.4)
plt.plot(x,predictions_upper[n_init:N_sam+n_init], color='gray',alpha=0.4)
plt.fill_between(x, predictions_lower[n_init:N_sam+n_init],predictions_upper[n_init:N_sam+n_init], color='gray',alpha=0.4)
plt.legend(['Datos', 'predicción','Rango']);
plt.show()




