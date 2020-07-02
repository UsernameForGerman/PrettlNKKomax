import pandas as pd

komax_number_dict = {2: '355.0281', 5: '355.0387'}  # must be changed

komax_df = pd.read_excel('C:\\Users\sadyk\PycharmProjects\\forKomax\modules\PrettlNKKomax\komax_modules\komax_df_{}.xlsx'.format(5))


print(komax_df.empty)

