import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
from moviepy.editor import ImageClip, concatenate_videoclips
import journo_play.tools.TimelineMapMaker.datetime_manager as di
from datetime import datetime
"""

new_video_file_path: the path to where you want the video to be saved to.

data_file_path: file path to the csv containing the data that you want timeline mapped
Was written to work with the UCPD conflict dataset
You can provide your own data, but it has to be in a csv with these columns and data_types

['date_start'] = date time string in iso format (the datetime of the event, the UCPD data is only accurate to the day 
and has the time always as 00:00:00)
['best'] = int (best estimate for total casualties of event)
['deaths_civilians'] = int (number of civilian casualties, this is a subset of best)

time_increment: takes one of the following strs:
'day', 'd'
'week', 'w'
'month', 'm'
'year', 'y'
it isn't case sensitive
ability to have the time increment be hours, minutes or seconds (so for example you could have the timeline of events 
over the course of a day) will be the first update 


time_line_info: is extra text that you want displayed next to the map, the argument is a dictionary of the format
{'iso format datetime str': 'text string'}
it will concat in order of oldest to youngest based on time time increment. So if you are incrementing one day at a time
any datestrings that falls on the same day will have their values concatted together. The program won't do any kind of
formatting for you, so you may have to use line breaks etc and trial and error to make it look right.

"""


# todo:
# make it so that the stills can be temp files so that stills_directory_path can be None
# customise rolling death data, have presets and ability to inject custom rules
# iterate by increments less than a day.

class TimelineMap:

    _default_map_formatting = {
        'color': 'grey',
        'edgecolor': 'white',
        'linewidth': 1.5,
        'alpha': 0.9
    }

    _default_plot_formatting = {
        'alpha': 0.6, 'legend': True, 'markersize': 10, 'color': 'red'
    }

    _default_still_title_formatting = {
        'fontsize': 15, 'fontweight': 'bold'
    }

    _default_subplot_formatting = {
        'figsize': (8, 8)
    }

    _default_video_formatting = {'fps': 20}

    MAP = 'map'
    PLOT = 'plot'
    VIDEO = 'video'
    STILL_TITLE = 'still_title'
    SUBPLOT = 'subplot'

    def __init__(self, map_shape_file_path):
        self._map = gpd.read_file(map_shape_file_path)

        self._map_formatting = self._default_map_formatting.copy()
        self._plot_formatting = self._default_plot_formatting.copy()
        self._video_formatting = self._default_video_formatting.copy()
        self._still_title_formatting = self._default_still_title_formatting.copy()
        self._subplot_formatting = self._default_subplot_formatting.copy()

        self._formattings_dict = {self.MAP: self._map_formatting,
                                  self.PLOT: self._plot_formatting,
                                  self.VIDEO: self._video_formatting,
                                  self.STILL_TITLE: self._still_title_formatting,
                                  self.SUBPLOT: self._subplot_formatting
                                  }

    def set_subplot_formatting(self, **kwargs):

        self.set_formatting(self.SUBPLOT, **kwargs)

    def set_map_formatting(self, **kwargs):

        self.set_formatting(self.MAP, **kwargs)

    def set_plot_formatting(self, **kwargs):
        self.set_formatting(self.PLOT, **kwargs)

    def set_video_formatting(self, **kwargs):
        self.set_formatting(self.VIDEO, **kwargs)

    def set_still_title_formatting(self, **kwargs):
        self.set_formatting(self.STILL_TITLE, **kwargs)

    def set_formatting(self, kind, **kwargs):

        formatting = self._formattings_dict.get(kind, None)

        if formatting is None:
            raise SyntaxError('{0} is not a valid formatting set'.format(kind))

        for setting, value in kwargs.items():
            if setting in formatting.keys():
                if not isinstance(value, type(formatting[setting])):
                    raise TypeError('{0} should be of type {1}'.format(setting, type(formatting[setting])))

            formatting[setting] = value

    @classmethod
    def render_video_from_stills(cls, still_file_paths, fps, video_file_path):
        print('making film')

        clips = [ImageClip(m).set_duration(1)
                 for m in still_file_paths]

        concat_clip = concatenate_videoclips(clips, method="compose")
        concat_clip.write_videofile(video_file_path, fps=fps)

    def make_video(self,
                   title,
                   stills_directory_path,
                   new_video_file_path,
                   data_file_path=None,
                   df=None,
                   end_date=None, start_date=None,
                   time_increment=None,
                   time_line_info=None
                   ):

        stills_file_paths = self.make_stills(stills_directory_path=stills_directory_path, end_date=end_date,
                                             start_date=start_date, time_line_info=time_line_info, title=title,
                                             time_increment=time_increment, data_file_path=data_file_path, df=df)

        self.render_video_from_stills(still_file_paths=stills_file_paths,
                                      video_file_path=new_video_file_path,
                                      **self._video_formatting
                                      )

    def make_stills(self, title, time_increment, df=None, data_file_path=None, stills_directory_path=None,
                    end_date=None,
                    start_date=None,
                    time_line_info=None,

                    ):

        manager, df, start_date, end_date, time_line_info = \
            self._make_stills_argument_check(df=df,
                                             end_date=end_date,
                                             start_date=start_date,
                                             time_increment=time_increment,
                                             time_line_info=time_line_info,
                                             data_file_path=data_file_path
                                             )

        df = manager.prepare_df(df)

        processing_range_start, processing_range_end = manager.set_first_processing_range(start_date=start_date)

        file_paths = []
        total_dead = 0
        total_civilian = 0

        while processing_range_end <= end_date:
            processing_df = manager.get_processing_df(processing_range_start,
                                                          processing_range_end,
                                                          df
                                                          )

            current_geo_df = self._make_geo_df(processing_df)

            date_string = manager.make_date_str(processing_range_start=processing_range_start,
                                                    processing_range_end=processing_range_end)

            file_path = self._make_still_file_path(stills_directory_path=stills_directory_path,
                                                   title=title, date_string=date_string)

            file_paths.append(file_path)

            processing_deaths = processing_df['best'].sum()
            processing_civilians = processing_df['deaths_civilians'].sum()

            total_dead += processing_deaths
            total_civilian += processing_civilians

            processing_title = """
                        {title}
            {total_dead} Total Dead, {total_civilian} Civilian Casualties
              {date_string}: {processing_deaths} Died 
            """.format(title=title, total_dead=total_dead, total_civilian=total_civilian, date_string=date_string,
                       processing_deaths=processing_deaths)

            self._plot_map(current_geo_df, file_path=file_path, title=processing_title)

            print('{0} + {1}'.format(date_string, str(len(current_geo_df))))

            processing_range_start, processing_range_end = manager.increment_date_range(processing_range_start,
                                                                                        processing_range_end)

        return file_paths

    @classmethod
    def _make_still_file_path(cls, stills_directory_path, title, date_string):
        file_path = stills_directory_path + '/{title}_{date}.png'.format(title=title, date=date_string)
        return file_path

    def _make_stills_argument_check(self, df, end_date, start_date,
                                    time_increment,
                                    time_line_info, data_file_path):

        datetime_manager = di.get_manager(time_increment)

        if df is None and data_file_path is None:
            raise ValueError('Only input either a dataframe or path to csv not both')

        if df is not None and data_file_path is not None:
            raise ValueError('Missing data! Either input a dataframe or a path to csv')

        if data_file_path is not None:
            df = pd.read_csv(data_file_path)

        df = self._clean_data(df)

        def check_dates(date_input, date_series):

            if type(date_input) is datetime:
                return date_input
            if type(date_input) is str:
                return datetime.fromisoformat(date_input)

            raise TypeError(f"'{date_series}' must be of type datetime or str")

        start_date = df['date_start'].min() if start_date is None else check_dates(start_date, 'start_date')
        end_date = df['date_start'].max() if end_date is None else check_dates(end_date, 'end_date')
        time_line_info = {} if time_line_info is None else time_line_info

        return datetime_manager, df, start_date, end_date, time_line_info

    def _clean_data(self, df):
        df['date_start'] = pd.to_datetime(df['date_start'])

        return df

    def _make_geo_df(self, df):
        # designate coordinate system
        crs = "EPSG:4326"
        # zip x and y coordinates into single feature
        geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
        # create GeoPandas dataframe
        geo_df = gpd.GeoDataFrame(df,
                                  crs=crs,
                                  geometry=geometry)

        return geo_df

    def _plot_map(self, geo_df, file_path, title):
        # create figure and axes, assign to subplot
        fig, ax = plt.subplots(**self._subplot_formatting)
        # add .shp mapfile to axes
        self._map.plot(ax=ax, **self._map_formatting)
        if len(geo_df) > 0:
            geo_df.plot(ax=ax, **self._plot_formatting)
        # plt.axes('off')
        plt.title(title, **self._still_title_formatting)
        plt.savefig(format='png', fname=file_path)
        plt.cla()
