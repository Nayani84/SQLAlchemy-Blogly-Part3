from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

DEFAULT_IMAGE_URL = 'https://cdn-icons-png.flaticon.com/512/10453/10453654.png'

"""Models for Blogly."""
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(db.Text, nullable=True, default=DEFAULT_IMAGE_URL)

    
    posts = db.relationship('Post', backref='users', cascade="all, delete-orphan")


    def __repr__(self):
        u = self
        return f"<user id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"
    

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"



class Post(db.Model):

    def format_date(self):

        months={1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
        month_key=self.created_at.month
        named_month=months[month_key]
        friendly_time=self.created_at.strptime(f'{self.created_at.hour}:{self.created_at.minute}','%H:%M').strftime('%I:%M %p')
        
        return f"{named_month} {self.created_at.day}, {self.created_at.year} at {friendly_time}"

    @classmethod
    def print_current_time(self):
        print(f"{datetime.now()}")
        return(f"{datetime.now()}")

    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


    def __repr__(self):
        p = self
        return f"<post id={p.id} title={p.title} content={p.content} created_at={p.created_at} user_id={p.user_id}>"
    
    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text, nullable=False, unique=True)


    def __repr__(self):
        t = self
        return f"<tag id={t.id} name={t.name}>"
    
    posts = db.relationship('Post', secondary="posts_tags", backref="tags")


class PostTag(db.Model):
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True )