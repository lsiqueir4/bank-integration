import logging
from extensions import db


class BaseController:
    def __init__(self):
        self.db = db
        self.logger = logging.getLogger(__name__)
