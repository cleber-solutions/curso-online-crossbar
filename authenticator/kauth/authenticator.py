from autobahn.wamp.exception import ApplicationError
import records


class Authenticator:
    def __init__(self, db_url):
        self.db_url = db_url
        self.db = records.Database(db_url)

    def query(self, the_query, **kwargs):
        return self.db.query(the_query, **kwargs)

    def authenticate(self, realm, token, details):
        query = 'SELECT * FROM users_user_organization WHERE token = :token;'
        relations = self.query(query, token=token)
        relation = relations.first()

        if relation is None:
            raise ApplicationError("com.dronemapp.no_such_token", f'This token does not exist: {token}')

        query = 'SELECT * FROM users_user WHERE id = :user_id;'
        users = self.query(query, user_id=relation['user_id'])
        user = users.first()

        return {
            'secret': user['username'],
            'role': 'user'
        }

    def get_user_data(self, token):
        query = 'SELECT * FROM users_user_organization WHERE token = :token;'
        relations = self.query(query, token=token)
        relation = relations.first()

        if relation is None:
            raise ApplicationError("com.dronemapp.no_such_token", f'This token does not exist: {token}')

        query = 'SELECT * FROM users_user WHERE id = :user_id;'
        users = self.query(query, user_id=relation['user_id'])
        user = users.first()

        return {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'organization_id': relation['organization_id']
        }
