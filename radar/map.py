import pyart
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import osmnx
import osmnx.io


def make_plot(config, data, field, vmin, vmax, sweep):
    display = pyart.graph.RadarMapDisplay(data)

    # Set up a figure with a Cartopy projection
    fig = plt.figure(num=field, figsize=(10, 10))
    fig.subplots_adjust(wspace=0, hspace=0)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree()) # type: ignore
    ax.set_aspect('equal')
    ax.set_facecolor('black')

    display.plot_ppi_map(
        field,
        sweep=sweep,
        ax=ax,
        vmin=vmin,
        vmax=vmax,
        cmap='pyart_NWSRef',
        raster=True,
        mask_outside=True,
        add_grid_lines=False,
        colorbar_flag=False,
        title_flag=False,
        embellish=False,
        min_lat=config['radar.bbox']['min_lat'],
        max_lat=config['radar.bbox']['max_lat'],
        min_lon=config['radar.bbox']['min_lon'],
        max_lon=config['radar.bbox']['max_lon'])

    graph = osmnx.io.load_graphml('osm.graphml')

    osmnx.plot_graph(graph, ax=ax, bgcolor='none', edge_color='white', edge_linewidth=1, node_size=0) # type: ignore

    for col in ax.collections: # type: ignore
        if isinstance(col, LineCollection):
            col.set_antialiased(False)

    return fig


def render_composite(config, dry_run):
    data_path = config['files']['radar_raw_test'] if dry_run else config['files']['radar_raw']
    radar_data = pyart.io.read_nexrad_archive(data_path)

    composite_reflectivity = pyart.retrieve.composite_reflectivity(radar_data, field='reflectivity')

    fig = make_plot(config, composite_reflectivity, 'composite_reflectivity', 10, 100, 0)

    fig.savefig(config['files']['radar_img'], dpi=100, bbox_inches='tight', pad_inches=0.0)
