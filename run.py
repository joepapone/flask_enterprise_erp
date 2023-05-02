#!/usr/bin/env python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app = create_app('development')

'''
#!/usr/bin/env python
from app import create_app, db
from app.auth.models import User, Book


if __name__ == '__main__':
    app = create_app('development')
    with app.app_context():
        db.create_all()
        if User.query.filter_by(email='joepapone@gmail.com').first() is None:
            User.register('joepap', 'abc')
            app.run()
'''
