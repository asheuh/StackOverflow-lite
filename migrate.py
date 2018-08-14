from stackoverflow.api.v2.models import User, BlackList, Question

class Migration:
    @staticmethod
    def refresh_db():
        Migration.tear_down()
        Migration.create_all()

    @staticmethod
    def create_all():
        """Creates the tables"""
        User.migrate()
        Question.migrate()
        BlackList.migrate()

    @staticmethod
    def tear_down():
        """Deletes data from the the tables"""
        User.rollback()
        Question.rollback()
        BlackList.rollback()
