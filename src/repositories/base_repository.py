class BaseRepository:
    def __init__(self, session):
        self.session = session

    def get_enumerator(self, model, enumerator):
        return self.session.query(model).filter(model.enumerator == enumerator).first()
