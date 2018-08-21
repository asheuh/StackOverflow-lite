from stackoverflow import create_app
from stackoverflow import settings
from migrate import DBMigration

migrate = DBMigration()
app = create_app(settings.DEVELOPMENT)

if __name__ == "__main__":
    migrate.create_all()
    app.run(debug=settings.FLASK_DEBUG)
