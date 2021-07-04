import pandas as pd
import dataframe_image as dfi

JLPT_LEVEL = 1

kanji_df = pd.read_json('kanji.json').T
n1_df = kanji_df.loc[kanji_df['jlpt_new'] == JLPT_LEVEL]
n1_df = n1_df[["strokes","grade","freq","meanings","readings_on","readings_kun"]]

def generate_todays_kanji_(todays_day_number, KANJI_AMOUNT):
    starting_kanji_index = (todays_day_number - 1) * KANJI_AMOUNT
    kanjis_of_the_day_df = n1_df.iloc[starting_kanji_index:starting_kanji_index + KANJI_AMOUNT]
    dfi.export(kanjis_of_the_day_df, "Todays_Kanji.png")

    kanji_and_meanings = kanjis_of_the_day_df[["meanings","readings_on","readings_kun"]]

    return kanji_and_meanings.to_string(header=False)



