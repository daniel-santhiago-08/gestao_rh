class DBRoutes:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'price_crawler_inissia_daily':
            return 'antigo'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'price_crawler_inissia_daily':
            return 'antigo'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'price_crawler_inissia_daily' or \
           obj2._meta.app_label == 'price_crawler_inissia_daily':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'price_crawler_inissia_daily':
            return db == 'antigo'
        return None