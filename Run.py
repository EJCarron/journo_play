import pandas as pd
from matplotlib import pyplot as plt
from journo_play.tools.TimelineMapMaker import TimelineMap as tlm

syria_df = pd.read_csv('/Users/edcarron/code/journo_play/data/syria_df.csv')

syria_video = tlm('/Users/edcarron/code/journo_play/data/syria_shape_files/syrBound.shp')

syria_video.make_video(title='Syrian Civil War',
                       new_video_file_path='/Users/edcarron/code/journo_play/data/country_vids/finished/Syria.mp4',
                       stills_directory_path='/Users/edcarron/code/journo_play/data/country_vids/stills/Syria',
                       df=syria_df, start_date='2011-03-01', end_date='2011-04-01', time_increment='d'
                       )
change = "test change"




# palestine_df = pd.read_csv('/Users/edcarron/code/journo_play/data/palestine_df.csv')
#
# second_intifada_video = tlm('/Users/edcarron/code/journo_play/data/peace/peace_in_mid_east.shp')
#
# second_intifada_video.make_video(title='Second Intifada',
#                                  new_video_file_path='data/country_vids/finished/second_intifada.mp4',
#                                  stills_directory_path='data/country_vids/stills/second_intifada',
#                                  df=palestine_df,
#                                  start_date='2000-09-28', end_date='2005-02-08', time_increment='m'
#                                  )


# firstQ21 = pd.read_csv('/Users/edcarron/code/journo_play/data/GEDEvent_v21_01_21_03.csv')
#
# conflict_df = pd.read_csv('/Users/edcarron/code/journo_play/data/ged201.csv')
#
# for count in conflict_df['country'].unique():
#     print(count)
#
#
#
# all_columns = ['id', 'relid', 'year', 'active_year', 'code_status', 'type_of_violence', 'conflict_dset_id',
#                'conflict_new_id', 'conflict_name', 'dyad_dset_id', 'dyad_new_id', 'dyad_name', 'side_a_dset_id',
#                'side_a_new_id', 'side_a', 'side_b_dset_id', 'side_b_new_id', 'side_b', 'number_of_sources',
#                'source_article', 'source_office', 'source_date', 'source_headline', 'source_original', 'where_prec',
#                'where_coordinates', 'where_description', 'adm_1', 'adm_2', 'latitude', 'longitude', 'geom_wkt',
#                'priogrid_gid', 'country', 'country_id', 'region', 'event_clarity', 'date_prec', 'date_start',
#                'date_end', 'deaths_a', 'deaths_b', 'deaths_civilians', 'deaths_unknown', 'best', 'high', 'low', 'gwnoa',
#                'gwnob']
#
# interesting_columns = ['dyad_name',
#                        'adm_1', 'adm_2',
#                        'country',
#                        'region', 'event_clarity']
#
#
# def plot_coordinates(df, grouping):
#
#     groups = df.groupby(grouping)
#     for name, group in groups:
#         plt.plot(group['longitude'], group['latitude'], marker='o', linestyle='', markersize=5, label=name)
#
#     plt.legend()
#
#     plt.show()
#
#
# plot_coordinates(palestine_df, 'adm_1')