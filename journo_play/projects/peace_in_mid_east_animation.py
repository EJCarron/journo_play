# import libraries
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from moviepy.editor import ImageClip, concatenate_videoclips

# import street map
street_map = gpd.read_file('../../data/peace/peace_in_mid_east.shp')
palestine_df = pd.read_csv('/Users/edcarron/code/journo_play/data/palestine_df.csv')
israel_video_file_path = '/Users/edcarron/code/journo_play/data/country_vids/finished/israel/2014_conflict.mp4'
israel_stills_file_path = '/Users/edcarron/code/journo_play/data/country_vids/stills/isreal/2014_conflict{0}.png'


def date_loop(df, stills_file_path, video_file_path, title, start_date=None, end_date=None):
    df['date_start'] = df['date_start'].apply(lambda x: datetime.datetime.fromisoformat(x))

    start_date = df['date_start'].min() if start_date is None else start_date
    end_date = df['date_start'].max() if end_date is None else end_date

    current_day = start_date

    file_paths = []
    total_dead = 0
    total_civilian = 0


    while current_day <= end_date:
        current_day_df = df[df['date_start'] == current_day]

        current_geo_df = make_geo_df(current_day_df)

        date_string = current_day.strftime('%m-%d-%Y')

        file_path = stills_file_path.format(date_string)

        file_paths.append(file_path)

        todays_deaths = current_day_df['best'].sum()
        today_civilians = current_day_df['deaths_civilians'].sum()

        total_dead += todays_deaths
        total_civilian += today_civilians

        todays_title = title.format(date_string, total_dead, total_civilian, todays_deaths)

        plot_map(current_geo_df, file_path=file_path, title=todays_title)

        print('{0} + {1}'.format(date_string, str(len(current_geo_df))))

        current_day += datetime.timedelta(days=1)

    create_film_clip(still_file_paths=file_paths, fps=20, video_file_path=video_file_path)


def create_film_clip(still_file_paths, fps, video_file_path):
    print('making film')
    # file_list_sorted = natsorted(file_list,reverse=False)  # Sort the images
    clips = [ImageClip(m).set_duration(1)
             for m in still_file_paths]

    concat_clip = concatenate_videoclips(clips, method="compose")
    concat_clip.write_videofile(video_file_path, fps=fps)


def make_geo_df(df):
    # designate coordinate system
    crs = "EPSG:4326"
    # zip x and y coordinates into single feature
    geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
    # create GeoPandas dataframe
    geo_df = gpd.GeoDataFrame(df,
                              crs=crs,
                              geometry=geometry)

    return geo_df


def plot_map(geo_df, file_path, title):
    # create figure and axes, assign to subplot
    fig, ax = plt.subplots(figsize=(8, 8))
    # add .shp mapfile to axes
    street_map.plot(ax=ax, linewidth=1.5, alpha=0.9, color='grey', edgecolor='white')
    if len(geo_df) > 0:
        geo_df.plot(ax=ax, alpha=0.6, legend=True, markersize=10, color='red')
    plt.axes('off')
    plt.title(title, fontsize=15, fontweight='bold')
    plt.savefig(format='png', fname=file_path)
    plt.cla()


start_date = datetime.datetime.fromisoformat('2014-07-01')
end_date = datetime.datetime.fromisoformat('2014-09-01')




key_dates = {'1 July 2014': 'teenager, Yusef Ahmad Bani Gharrah was killed by Israeli security forces',
'2 July 2014':'Palestinian boy, Mohammed Abu Khdeir, was kidnapped, covered in petrol, and set on fire, outside of Jerusalem',
             '8 July 2014': 'War breaks out between Israel and Hamas'
             }

date_loop(palestine_df, stills_file_path=israel_stills_file_path,


          video_file_path=israel_video_file_path, title="""
          {1} Total Dead, {2} Civilian Casualties
          {0}: {3} Died 
          """,
          end_date=end_date, start_date=start_date
          )
