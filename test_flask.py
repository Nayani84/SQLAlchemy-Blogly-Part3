from unittest import TestCase

from app import app
from models import db, User, Post, Tag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

app.app_context().push()
app.app_context()

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""
        Post.query.delete()
        User.query.delete()
        Tag.query.delete()
        
        user = User(first_name="Jane", last_name="Smith", image_url='https://spor12.dk/wp-content/uploads/2017/05/speaker-1.jpg')
        db.session.add(user)
        db.session.commit()

        post = Post(title="Home", content="My Everything", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        tag = Tag(name="Brave")
        db.session.add(tag)
        db.session.commit()

        self.user_id = user.id
        self.user = user
        self.post_id = post.id
        self.post = post
        self.tag_id = tag.id
        self.tag = tag



    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_home_page(self):
        """Check to make sure correct HTML is displayed."""

        with app.test_client() as client:
            resp = client.get('/')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, '/users')

################################################ Users Route ################################################

    def test_list_users(self):
        """Check to make sure user_list displayed correctly."""

        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jane', html)
            

    def test_show_user(self):
        """Check to make sure user_detail displayed correctly."""

        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jane Smith', html)
            self.assertIn('Home', html)

            
    def test_new_user_form_page(self):
        """Test if new_user form page returns correct status code for GET request and returns included html"""

        with app.test_client() as client:
            resp=client.get("/users/new")
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1>Create a User</h1>',html)


    def test_add_user(self):
        """make sure add user data handle correctly."""

        with app.test_client() as client:
            data = {
                    "first_name" :"Jane",
                     "last_name" :"Smith", 
                     "image_url" :"https://spor12.dk/wp-content/uploads/2017/05/speaker-1.jpg"
                     }
            resp = client.post("/users/new", data=data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Jane Smith', resp.data)


    def test_delete_user(self):
        """make sure delete user data handle correctly."""

        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/delete')
            user = User.query.get(self.user_id)

            self.assertFalse(user)

################################################ Posts Route ################################################

    def test_show_new_post_form(self):
        """Test if new_post form page returns correct status code for GET request and returns included html"""

        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/posts/new')
            html = resp.get_data(as_text=True)
            user = User.query.get(self.user_id)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'Add Post for { user.first_name} {user.last_name }', html)
    

    def test_show_post(self):
        """Check to make sure post detail displayed correctly."""

        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Home', html)

################################################ Tags Route ################################################

    def test_list_tags(self):
        """Check to make sure tags list displayed correctly."""

        with app.test_client() as client:
            resp = client.get("/tags")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Brave', html)


    def test_show_new_tag_form(self):
        """Test if new tag form page returns correct status code for GET request and returns included html"""

        with app.test_client() as client:
            resp = client.get(f'/tags/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h1 class="ml-3">Create a tag</h1>', html)


    def test_add_tag(self):
        """make sure add tag data handle correctly."""

        with app.test_client() as client:
            data = {
                    "name" :"Test Tag"
                    }
            resp = client.post("/tags/new", data=data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Test Tag', resp.data)
