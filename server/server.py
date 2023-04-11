import logging
from flask import Flask, send_file, jsonify
import os
from datetime import datetime, timezone, timedelta
from sources import nexrad_level2, open_meteo
from components.radar.render import render as render_radar
from components.forecast.render import render as render_forecast
import frame.frame

last_update = datetime(1970, 1, 1, tzinfo=timezone.utc)


def create(config):
    logger = logging.getLogger(__name__)

    app = Flask(__name__, root_path=os.getcwd())

    @app.route('/last-update')
    def last_update_get():
        global last_update
        return jsonify({ 'last_update': last_update.isoformat() })

    @app.route('/frame')
    def frame_get():
        global last_update

        logger.info(f'last update: {last_update}')

        latest = nexrad_level2.latest_object(config['radar']['nexrad_id'])

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
            nexrad_level2.download(latest, to=config['files']['radar_raw'])
            render_radar(config, False)

            # Forecast
            res = open_meteo.get(open_meteo.Request.from_config(config))
            render_forecast(config, res)

            # Combine
            frame.frame.create(config)

            last_update = latest.last_modified
        else:
            logger.info('no new radar data, using previous image')

        return send_file(config['files']['output_img'], mimetype='image/png')

    return app
