"""
class ArticleRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'myapp':
            return 'article'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'myapp':
            return 'article'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label == 'myapp' or
            obj2._meta.app_label == 'myapp'
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'myapp':
            return db == 'article'
        return None

"""