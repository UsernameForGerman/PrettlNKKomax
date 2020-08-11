import pandas as pd

df = pd.DataFrame({"Примечание" : [pd.np.nan, pd.np.nan, "Кабель", "Скрутить..."],
                   "Маркировка" : ["чёрный", "чёрный", "белый", "чёрный"]})

temp = df.loc[:, "Примечание"]
print(temp)

rows_drop = []

for row in df.iterrows():
    print(row[1])


print(df)
