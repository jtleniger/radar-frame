import logging
from flask import Flask, send_file
import os
from datetime import datetime, timezone, timedelta
import radar.fetch
import radar.map
import forecast.render
import forecast.open_meteo
import frame.frame

last_update = datetime(1970, 1, 1, tzinfo=timezone.utc)


def create(config):
    logger = logging.getLogger(__name__)

    app = Flask(__name__, root_path=os.getcwd())

    @app.route('/frame')
    def frame_get():
        global last_update

        logger.info(f'last update: {last_update}')

        latest = radar.fetch.latest_object(config)

        if not latest:
            logger.info('no latest object')
            # TODO
            return send_file(config['files']['output_img'], mimetype='image/png')

        now = datetime.now(tz=timezone.utc)

        if now - latest.last_modified > timedelta(minutes=int(config['radar']['stale_minutes'])):
            # TODO
            logger.info('radar stale')

        if latest.last_modified > last_update:
            logger.info(f'fetching data for {latest.key} (modified at: {latest.last_modified})')

            # Radar
            radar.fetch.fetch_radar(config, latest)
            radar.map.render_composite(config, False)

            # Forecast
            current_conditions, forecast_data = forecast.open_meteo.fetch(config)
            forecast.render.render_image(config, current_conditions, forecast_data)

            # Combine
            frame.frame.create(config)

            last_update = latest.last_modified
        else:
            logger.info('no new radar data, using previous image')

        return send_file(config['files']['output_img'], mimetype='image/png')

    return app
