from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure, show, output_file
from objectDetection import time_dataFrame as df

df['Start'] = df['Start Time'].dt.strftime("%Y-%m-%d  %H:%M:%S")
df['End'] = df['End Time'].dt.strftime("%Y-%m-%d  %H:%M:%S")

graph = figure(x_axis_type='datetime', height=80, width=800, responsive=True, title='Time Graph')
graph.yaxis.minor_tick_line_color = None
graph.ygrid[0].ticker.desired_num_ticks = 1

hover = HoverTool(tooltips=[("Start Time","@Start"),("End Time", "@End")])
graph.add_tools(hover)

plot = graph.quad(left=df['Start Time'], right=df['End Time'], bottom=0, top=1, color='green',
                  source=ColumnDataSource(df))

output_file('Time Graph.html')
show(graph)



