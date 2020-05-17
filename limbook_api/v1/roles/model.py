from limbook_api.db import db, BaseDbModel


class Role(BaseDbModel):
    """Roles"""

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    """
    format()
        format the data for the api
    """
    def format(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'name': self.name,
            'description': self.description,
            'permissions': [
                permission.format() for permission in self.permissions
            ],
            'created_on': self.created_on.__str__(),
            'updated_on': self.updated_on.__str__(),
        }