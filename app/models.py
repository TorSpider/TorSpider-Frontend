from sqlalchemy.ext.automap import automap_base

# We will map to the existing database here.
Base = automap_base()

from app import db

Base.prepare(db.engine, reflect=True)

Onions = Base.classes.onions
Urls = Base.classes.urls
Links = Base.classes.links
Pages = Base.classes.pages
Forms = Base.classes.forms
