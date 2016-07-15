class EmissionsRouter(object):
    """
    A router to control all database operations on models in the
    avoided emissions application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read emissions models go to emissions.
        """
        if model._meta.app_label == 'emissions':
            return 'emissions'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write emissions models go to emissions_db.
        """
        if model._meta.app_label == 'emissions':
            return 'emissions'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the emissions app is involved.
        """
        if obj1._meta.app_label == 'emissions' or \
           obj2._meta.app_label == 'emissions':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the emissions app only appears in the 'emissions_db'
        database.
        """
        if app_label == 'emissions':
            return db == 'emissions'
        return None
