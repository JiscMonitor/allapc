from flask import Flask, request, abort, render_template, redirect, make_response, jsonify, send_file, \
    send_from_directory
from flask.views import View

from portality.core import app, initialise
from portality.lib.webapp import custom_static, javascript_config
import sys

@app.route("/")
def root():
    return render_template("index.html")

# this allows us to override the standard static file handling with our own dynamic version
@app.route("/static/<path:filename>")
def static(filename):
    return custom_static(filename)

# this allows us to serve our standard javascript config
@app.route("/javascript/config.js")
def configure_javascript():
    return javascript_config()

from portality.modules.es.autocomplete import blueprint as autocomplete
app.register_blueprint(autocomplete, url_prefix='/autocomplete')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


if __name__ == "__main__":
    initialise()

    pycharm_debug = app.config.get('DEBUG_PYCHARM', False)
    if len(sys.argv) > 1:
        if sys.argv[1] == '-d':
            pycharm_debug = True

    if pycharm_debug:
        app.config['DEBUG'] = False
        import pydevd
        pydevd.settrace(app.config.get('DEBUG_SERVER_HOST', 'localhost'), port=app.config.get('DEBUG_SERVER_PORT', 51234), stdoutToServer=True, stderrToServer=True)
        print "STARTED IN REMOTE DEBUG MODE"

    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=app.config['PORT'], threaded=False)
    # app.run(host=app.config.get("HOST", "0.0.0.0"), debug=app.config.get("DEBUG", False), port=app.config.get("PORT", 5000), threaded=True)
    # start_from_main(app)

