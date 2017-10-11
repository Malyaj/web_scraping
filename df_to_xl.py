import pandas as pd

asin1 = 'B01NBXH3LD'
df1 = pd.DataFrame({'Prices': ['Rs. 8,304.00'], 'Sellers': ['eCommerce India']})
asin2 = 'B00LOWZWTW'
df2 = pd.DataFrame({'Prices': ['Rs. 4,417.00', 'Rs. 6,058.70'], 'Sellers': ['G. G.', 'LUSSO LIV']})


'''{'B01NBXH3LD':          Prices          Sellers
0  Rs. 8,304.00  eCommerce India,'B00LOWZWTW':          Prices    Sellers
0  Rs. 4,417.00      G. G.
1  Rs. 6,058.70  LUSSO LIV}'''

filename = asin2
format = '.xlsx'

writer = pd.ExcelWriter(filename + format)

df2.to_excel(writer, startcol=0, startrow=1)
writer.save()