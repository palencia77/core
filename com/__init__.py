import os.path
import jinja2

from com.restful.__init__ import services_app
from flask_mongoengine import MongoEngine, Pagination

app_path = os.path.dirname(os.path.dirname(__file__))
if app_path is not None and app_path != "":
    app_path += "/"

db_config = {}
execfile(app_path + "conf/properties/mongodb.cfg", db_config)

services_app.config['MONGODB_SETTINGS'] = {
    'DB': db_config["DB"],
    'HOST': db_config["HOST"],
    'PORT': db_config["PORT"],
    'USERNAME': db_config["USERNAME"],
    'PASSWORD': db_config["PASSWORD"]
}
services_app.jinja_loader = jinja2.FileSystemLoader(app_path + "conf/templates")
db = MongoEngine(services_app)
if __name__ == '__main__':
    services_app.run('0.0.0.0', 5000, True)
