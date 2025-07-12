from app import create_app
from app.extensions import db

app = create_app()
app.app_context().push()

db.drop_all()
db.create_all()
print("Test DB reset done")

