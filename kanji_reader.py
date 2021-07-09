from numpy import number
import pandas as pd
import config as CONFIG
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
from pandas.plotting import table  # EDIT: see deprecation warnings below


def getValue(x):
    if (isinstance(x, list)):
        if (len(x) > 5):
            x = x[::5]
        x = "\n".join(x)

    return x


fontprop = font_manager.FontProperties(fname='.fonts/ipaexg.ttf')
font_manager.fontManager.addfont(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 'fonts/ipaexg.ttf'))

kanji_df = pd.read_json(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kanji.json')).T
n1_df = kanji_df.loc[kanji_df['jlpt_new'] == CONFIG.JLPT_LEVEL]
n1_df = n1_df[[
    "strokes", "grade", "freq", "meanings", "readings_on", "readings_kun"
]]


def generate_todays_kanji_(todays_day_number, KANJI_AMOUNT):
    matplotlib.rc('font', family="IPAexGothic")
    starting_kanji_index = (todays_day_number - 1) * KANJI_AMOUNT
    if (starting_kanji_index >= len(n1_df)):
        starting_kanji_index = starting_kanji_index - len(n1_df)
    if (len(n1_df) < (starting_kanji_index + KANJI_AMOUNT)):
        kanjis_of_the_day_df = n1_df.iloc[starting_kanji_index:len(n1_df)]
    else:
        kanjis_of_the_day_df = n1_df.iloc[
            starting_kanji_index:starting_kanji_index + KANJI_AMOUNT]
    #kanjis_of_the_day_df_style = kanjis_of_the_day_df.style.set_table_styles(
    #    **{
    #       'background': '#E5E7EB',
    #       'border-color': '#374151',
    #       'border-radius': '16px',
    #       'box-shadow':
    #       '0 0 transparent,0 0 transparent),0 0 transparent,1.5px 1.5px 1.5px rgba(0,0,0,0.2)',
    #       'font-family': 'IPAexGothic'
    #   })
    fig_background_color = 'skyblue'
    fig_border = 'steelblue'
    plt.figure(
        linewidth=2,
        tight_layout={'pad': 1},
        edgecolor=fig_border,
        facecolor=fig_background_color,
    )
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.box(on=None)
    plt.suptitle(f"Kanjis of the Day #{todays_day_number}")
    kanji_and_meanings = kanjis_of_the_day_df[[
        "meanings", "readings_on", "readings_kun"
    ]]

    the_table = table(ax=ax,
                      data=kanjis_of_the_day_df.applymap(lambda x: getValue(x),
                                                         na_action='ignore'),
                      loc='center',
                      colWidths=[0.1, 0.1, 0.1, 0.3, 0.2, 0.2])
    the_table.scale(1.3, 4)
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(8)

    plt.draw()
    fig = plt.gcf()
    plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "Todays_Kanji.png"),
                edgecolor=fig.get_edgecolor(),
                facecolor=fig.get_facecolor(),
                bbox='tight',
                dpi=150)

    return kanji_and_meanings
