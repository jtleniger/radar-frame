import os
from flask import Flask

from server.api import api


def create():
    app = Flask(__name__, root_path=os.getcwd())
    app.register_blueprint(api)

    # @app.route('/last-update')
    # def last_update_get():
    #     global last_update
    #     return jsonify({ 'last_update': last_update.isoformat() })

    # @app.route('/frame')
    # def frame_get():
    #     global last_update

    #     logger.info(f'last update: {last_update}')

    #     latest = nexrad_level2.latest_object(config['radar']['nexrad_id'])

    #     if not latest:
    #         logger.info('no latest object')
    #         # TODO
    #         return send_file(config['files']['output_img'], mimetype='image/png')

    #     now = datetime.now(tz=timezone.utc)

    #     if now - latest.last_modified > timedelta(minutes=int(config['radar']['stale_minutes'])):
    #         # TODO
    #         logger.info('radar stale')

    #     if latest.last_modified > last_update:
    #         logger.info(f'fetching data for {latest.key} (modified at: {latest.last_modified})')

    #         # Radar
    #         nexrad_level2.download(latest, to=config['files']['radar_raw'])
    #         render_radar(config, False)

    #         # Forecast
    #         res = open_meteo.get(open_meteo.Request.from_config(config))
    #         render_forecast(config, res)

    #         # Combine
    #         frame.frame.create(config)

    #         last_update = latest.last_modified
    #     else:
    #         logger.info('no new radar data, using previous image')

    #     return send_file(config['files']['output_img'], mimetype='image/png')

    return app
