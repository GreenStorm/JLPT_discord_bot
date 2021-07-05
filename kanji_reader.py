import pandas as pd
#import dataframe_image as dfi
import config as CONFIG
#import imgkit
import tabulate

kanji_df = pd.read_json('kanji.json').T
n1_df = kanji_df.loc[kanji_df['jlpt_new'] == CONFIG.JLPT_LEVEL]
n1_df = n1_df[["strokes","grade","freq","meanings","readings_on","readings_kun"]]

def generate_todays_kanji_(todays_day_number, KANJI_AMOUNT):
    starting_kanji_index = (todays_day_number - 1) * KANJI_AMOUNT
    kanjis_of_the_day_df = n1_df.iloc[starting_kanji_index:starting_kanji_index + KANJI_AMOUNT]
    #dfi.export(kanjis_of_the_day_df, "Todays_Kanji.png")
    html = kanjis_of_the_day_df.to_html()
    #imgkit.from_string(html, "Todays_Kanji_Table.png")
    kanji_and_meanings = kanjis_of_the_day_df[["meanings","readings_on","readings_kun"]]

    outcome = tabulate.tabulate(kanjis_of_the_day_df, tablefmt="fancy_grid", headers="keys")
    return outcome
    #return kanji_and_meanings.to_string(header=False)



