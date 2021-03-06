'''
Traveling Baseball Fan Problem
Author: Sertalp B. Cay

This file plots the route to the html using folium package and Leaflet
javascript library. The same code is also used in Jupyter notebook.
'''

import os, glob
import folium
import datetime


def plot_tbf(route, name='latest'):
    # Start map centered in US
    tbfmap = folium.Map(location=[39.82, -98.58], zoom_start=4, tiles="OpenStreetMap")
    # Define the popup markers
    for node in route:
        print(node)
        dt = datetime.datetime.strptime(node[5], '%Y-%m-%d %H:%M:%S')
        dt_text = dt.strftime("%A, %B %d, %Y - %I:%M %p") + ' (ET)'
        popup_text = '''<div>
        Game {}: {} @ {}<br>
        {}, {}<br>
        {}</div>
        '''.format(node[0], node[2], node[3], node[1], node[4],
                   dt_text)
        popup_html = folium.Popup(popup_text, min_width=200, max_width=250)
        folium.Marker(location=[float(node[7]), float(node[6])], popup=popup_html,
                      icon=folium.DivIcon(html='<i class="fa fa-map-pin fa-stack-2x"></i><strong style="text-align: center; color: white; font-family: Trebuchet MS;" class="fa-stack-1x">{}</strong>'.format(node[0]))
                      ).add_to(tbfmap)
    # Add the lines between stadiums
    lines = folium.PolyLine(locations=[(float(i[7]), float(i[6])) for i in route])
    lines.add_to(tbfmap)
    # Print maps to html
    tbfmap.save("maps/{}.html".format(name))


def read_schedule(f):
    schd = []
    resfile = open(f, 'r')
    for line in resfile:
        if 'schd' in line:
            for visit in resfile:
                if ']' not in visit:
                    items = visit.split(',')
                    items = [i.replace('\n', '') for i in items]
                    schd.append(items)
    resfile.close()
    return schd

if __name__ == '__main__':
    files = glob.glob("results/*.txt")
    files.sort(key=os.path.getmtime)
    for i, f in enumerate(files):
        schd = read_schedule(f)
        plot_tbf(schd, i+1)
