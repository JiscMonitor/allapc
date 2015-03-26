from flask import Flask, request, abort, render_template, redirect, make_response, jsonify, send_file, \
    send_from_directory
from flask.views import View

from octopus.core import app, initialise
from octopus.lib.webapp import custom_static, jsonp
from service import dao
import sys, json

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/report/publisher")
def publisher():
    return render_template("publisher.html")

@app.route("/report/institution")
def institution():
    return render_template("institution.html")

@app.route("/report/oavshybrid")
def oavshybrid():
    return render_template("oavshybrid.html")

@app.route("/report/goldgreen")
def goldgreen():
    return render_template("goldgreen.html")

@app.route("/dates")
@jsonp
def dates():
    stats = dao.InstitutionalRecordDAO.date_statistics()
    resp = make_response(json.dumps(stats))
    resp.mimetype = "application/json"
    return resp

# this allows us to override the standard static file handling with our own dynamic version
@app.route("/static/<path:filename>")
def static(filename):
    return custom_static(filename)

from octopus.modules.clientjs.configjs import blueprint as configjs
app.register_blueprint(configjs)

# mount the blueprint for the api itself (which will appear at the root of the url space)
from service.view.api import blueprint as webapi
app.register_blueprint(webapi)

from octopus.modules.es.query import blueprint as query
app.register_blueprint(query, url_prefix="/inst_query")

from octopus.modules.es.autocomplete import blueprint as autocomplete
app.register_blueprint(autocomplete, url_prefix="/autocomplete")

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
        pydevd.settrace(app.config.get('DEBUG_SERVER_HOST', 'localhost'), port=app.config.get('DEBUG_SERVER_PORT', 6000), stdoutToServer=True, stderrToServer=True)
        print "STARTED IN REMOTE DEBUG MODE"

    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=app.config['PORT'], threaded=False)
    # app.run(host=app.config.get("HOST", "0.0.0.0"), debug=app.config.get("DEBUG", False), port=app.config.get("PORT", 5000), threaded=True)
    # start_from_main(app)

