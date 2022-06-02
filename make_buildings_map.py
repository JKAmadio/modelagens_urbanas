import osmnx as ox
import contextily as ctx

def make_buildings_map(location):
    # access the buildings geometries within 1000m x 1000m area
    osm = ox.geometries_from_address(location, tags={'building':True}, dist=1000)
    print(f'dados de {location} acessados!')
    print(osm.sample(10))

    # reproject to Web Mercator (defined in https://github.com/darribas/contextily)
    osm_web_mercator = osm.to_crs(epsg=3857)
    print('ajuste da projeção das geomatrias para EPSG 3857')

    # configure the map (https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.plot.html#geopandas.GeoDataFrame.plot) 
    ax = osm_web_mercator.plot(figsize=(10,10),
                    column='building',    # what we what to categorize our map with
                    cmap='tab20',         # set the color map https://matplotlib.org/2.0.2/users/colormaps.html
                    legend=True,          # turns on or off the legend
                    legend_kwds={'loc':'upper left', 'bbox_to_anchor': (1,1), 'frameon':False}    # legends settings such as location, anchor and frame on/off
                    )
    print('mapa preparados para plotagem')

    # add a title
    ax.set_title('Building types in ' + location)
    print('título preparados para plotagem')
    # remove the axis
    ax.axis('off')
    print('eixos retirados da plotagem')

    # add OpenStreetMap Mapnik as basemap
    #ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

    # add CartoDB DarkMatter as basemap
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.DarkMatter)
    print('mapa base adicionado')

