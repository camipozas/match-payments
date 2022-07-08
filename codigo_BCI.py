

import pandas as pd
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.float_format', lambda x: '%.3f' % x)

DF = pd.read_excel('2000 Bancos 1.XLSX')
df_d = pd.read_excel('Descripcion BCI.xlsx').drop(0)
df_d = df_d.dropna(subset=['Saldo'])
######### 
#esta parte solo se aplica cuando es necesario trasformar
#a numero decimal y se tienen separadores de miles
if str(df_d['Saldo'].dtype) == 'object':
    df_d['Saldo'] = df_d['Saldo'].str.replace('.','')
    df_d['Saldo'] = df_d['Saldo'].str.replace(',','.')
    df_d['Saldo'] = df_d['Saldo'].astype(float)
#########
df_d['Saldo'] *= -1
condicion1 = DF['Clase de documento'] == 'CT'
condicion2 = DF['Cuenta de mayor'] == 1101021011
df = DF[condicion1&condicion2]
lista = ['FECHA', 'SUCURSAL', 'N° DE']
df_d = df_d.drop(lista,axis=1)
tabla = df.merge(df_d,how='left',left_on='Importe en moneda doc.', right_on='Saldo')
#########
#problema en el valor -70781, existen 6 valores provenientes del archivo descripcion
#soluciones posibles?, una solucion a esto puede ser descartar valores en que la informacion no es precisa
importes_problematicos = tabla['Importe en moneda doc.'].value_counts() > 1
importes_problematicos = pd.DataFrame(importes_problematicos)
importes_problematicos = importes_problematicos[importes_problematicos['Importe en moneda doc.']]


if importes_problematicos.shape[0] > 0:
    importes_problematicos = importes_problematicos.index
    #en la columna 'Importe en moneda doc.' se toman todos los registros que sean parte de los importes_a_eliminar
    condicion = df['Importe en moneda doc.'].isin(importes_problematicos)
    df = df.drop(df[condicion].index)
    condicion = df_d['Saldo'].isin(importes_problematicos)
    df_d = df_d.drop(df_d[condicion].index)
    tabla = df.merge(df_d,how='left',left_on='Importe en moneda doc.', right_on='Saldo')
##########
#Cambiando Texto por descripcion
inter = tabla.dropna(subset=['DESCRIPCION'])
tabla.loc[inter.index,'Texto'] = inter['DESCRIPCION']
tabla = tabla.drop(['DESCRIPCION','Saldo'],axis=1)
#########
#Reconstruyendo
#~ negacion de conjunto boleano
condicion3 = ~DF['Importe en moneda doc.'].isin(importes_problematicos)
tabla.index = DF[condicion1&condicion2&condicion3].index
DF.loc[condicion1&condicion2&condicion3] = tabla
DF.to_excel('2000 Bancos.xlsx',index=False)





