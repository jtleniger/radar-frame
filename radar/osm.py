import osmnx
import osmnx.io as io


def download_data(config):
    bbox_config = config['radar.bbox']

    graph = osmnx.graph_from_bbox(
        bbox_config['max_lat'],
        bbox_config['min_lat'],
        bbox_config['max_lon'],
        bbox_config['min_lon'],
        custom_filter=('["highway"~"motorway|primary"]'))

    io.save_graphml(graph, filepath=config['files']['osm'])
