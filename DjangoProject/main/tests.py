from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from main.models import Library, Book, Notification
from postman.models import Message


class UserAuthenticationTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='hassaan',
                                 email='h@gmail.com',
                                 password='123456')

    def test_index_view(self):
        resp = self.client.get('/main/')
        self.assertEqual(resp.status_code, 200)

    def test_register_view(self):
        """
        Ensures User instance is created and saved to the database
        Author: Rana El-Garem

        """
        init_user_count = User.objects.all().count()
        response = self.client.post(reverse('register'),
                                    {'username': u'rana',
                                     'password': u'123456'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(init_user_count + 1, User.objects.all().count())
        self.assertTrue(User.objects.get(username='rana'))

    def test_automatic_login(self):
        """
        Ensures user is automatically logged in
        after registering
        Author: Rana El-Garem

        """
        self.client.post(reverse('register'),
                         {'username': u'rana',
                          'password': u'123456'})
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """
        Ensures user is logged in
        Author: Rana El-Garem

        """
        response = self.client.post(reverse('login'),
                                    {'username': 'hassaan',
                                     'password': '123456'})
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        """
        Ensures user is logged out
        Author: Rana El-Garem

        """
        self.client.get(reverse('register'),
                        {'username': u'rana',
                         'password': u'123456'})
        self.client.get(reverse('logout'))
        response2 = self.client.get(reverse('profile'))
        self.assertEqual(response2.status_code, 302)


class LibraryTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(username='rana',
                                 email='r@gmail.com',
                                 password='123456')
        self.client.post(reverse('login'),
                         {'username': 'rana',
                          'password': '123456'})
        Library.objects.create(name='Diwan',
                               location='zamalek',
                               owner=User.objects.all()[0])

    def test_library_list_view(self):
        """
        Ensures that libraries are listed
        Author: Rana El-Garem

        """
        response = self.client.get('/main/library/list/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('library_list' in response.context)
        self.assertEqual(response.context['library_list'][0].name, 'Diwan')
        self.assertEqual(
            [library.pk for library in response.context['library_list']], [1])

    def test_library_create_view(self):
        """
        Ensures that an instance of Library is created by a POST request
        Author: Rana El-Garem

        """
        initial_lib_count = Library.objects.count()
        response = self.client.post(reverse('library-new'),
                                    {'name': 'Aleph',
                                    'location': u'Maadi',
                                     'owner': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(initial_lib_count + 1, Library.objects.count())
        response = self.client.post(reverse('library-new'),
                                    {
                                    'location': u'Maadi',
                                    'owner': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(initial_lib_count + 1, Library.objects.count())

    def test_library_detail_view(self):
        """
        Author: Rana El-Garem

        """
        resp = self.client.get('/main/library/1/')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/main/slug/')
        self.assertEqual(resp.status_code, 404)


class BookTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(username='rana',
                                 email='r@gmail.com',
                                 password='123456')
        self.client.post(reverse('login'),
                         {'username': 'rana',
                          'password': '123456'})
        library = Library.objects.create(name='Diwan',
                                         location='zamalek',
                                         owner=User.objects.all()[0])
        Book.objects.create(name='Hepta',
                            author='X',
                            library=library)

    def test_book_detail_view(self):
        """
        Ensures details of a book is displayed
        Author: Rana El-Garem

        """
        resp = self.client.get('/main/book/hepta/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['object'].pk, 1)
        self.assertEqual(resp.context['object'].name, 'Hepta')

    def test_book_create_view(self):
        """
        Ensures an instance of Book is created by a POST request
        Author: Rana El-Garem

        """
        initial_book_count = Book.objects.count()
        response = self.client.post(reverse('book-new', kwargs={'pk': "1"}),
                                    {'name': u'Alchemist',
                                    'author': u'X',
                                     'library': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(initial_book_count + 1, Book.objects.count())

    def test_ensure_user_logged_in_book_create(self):
        """
        Ensures user must be logged in to create a Book
        Author: Rana El-Garem

        """
        self.client.get(reverse('logout'))
        initial_book_count = Book.objects.count()
        response = self.client.post(reverse('book-new', kwargs={'pk': "1"}),
                                    {'name': u'Alchemist',
                                    'author': u'X',
                                     'library': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(initial_book_count, Book.objects.count())

    def test_book_delete_view(self):
        response = self.client.post(reverse('book-delete',
                                    kwargs={'slug': 'hepta'}), {})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 0)

    def test_ensure_user_logged_in_book_delete(self):
        self.client.get(reverse('logout'))
        response = self.client.post(reverse('book-delete',
                                    kwargs={'slug': 'hepta'}), {})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 1)

    def test_book_update_view(self):
        response = self.client.post(reverse('edit-books'), data={
            'form-TOTAL_FORMS': 1,
            'form-INITIAL_FORMS': 1,
            'form-0-name': 'alchemist',
            'form-0-author': 'Y',
            'form-0-library': 1,
            'form-0-id': 1
            })
        print response
        print Book.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.all()[0].name, 'alchemist')


class NotificationTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(username='rana',
                                 email='r@gmail.com',
                                 password='123456')
        self.client.post(reverse('login'),
                         {'username': 'rana',
                          'password': '123456'})
        Library.objects.create(name='Diwan',
                               location='zamalek',
                               owner=User.objects.all()[0])
        User.objects.create_user(username='hassaan',
                                 email='h@gmail.com',
                                 password='123456')

    def test_notification_when_book_created(self):
        """
        Ensures notification instance is created
        for every user when a book is created
        Author:Rana El-Garem

        """
        init_notification_count = Notification.objects.count()
        Book.objects.create(name='Hepta',
                            author='X',
                            library=Library.objects.all()[0])
        self.assertEqual(init_notification_count + 2,
                         Notification.objects.count())

    def test_notification_list_view(self):
        """
        Ensures notifications are listed for a user
        Author: Rana El-Garem

        """
        Book.objects.create(name='Hepta',
                            author='X',
                            library=Library.objects.all()[0])
        self.client.get(reverse('logout'))
        self.client.post(reverse('login'),
                         {'username': 'hassaan',
                          'password': '123456'})
        response = self.client.get(reverse('notification'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('object_list' in response.context)
        self.assertEqual(response.context['object_list'][0].library_id, 1)

    def test_enure_user_logged_notification_list(self):
        """
        Ensures user must be logged in to view notifications
        Author: Rana El-Garem

        """
        self.client.get(reverse('logout'))
        response = self.client.post(reverse('notification'))
        self.assertEqual(response.status_code, 302)


class MessageTestCase(TestCase):

    # def setUp(self):
    #     User.objects.create_user(username='rana',
    #                              email='r@gmail.com',
    #                              password='123456')
    #     User.objects.create_user(username='hassaan',
    #                              email='h@gmail.com',
    #                              password='123456')
    #     self.client.post(reverse('login'),
    #                      {'username': 'rana',
    #                       'password': '123456'})

    def test_send_message(self):
        user1 = User.objects.create_user(username='rana',
                                         email='r@gmail.com',
                                         password='123456')
        user2 = User.objects.create_user(username='hassaan',
                                         email='h@gmail.com',
                                         password='123456')

        self.client.post(reverse('login'),
                         {'username': 'rana',
                          'password': '123456'})

        response = self.client.post('/messages/write/?next=/messages/inbox/',
                                    {'subject': 'test',
                                     'body': 'Test',
                                     'sender_id': 1, 'recipient_id': 2})
        Message.objects.create(subject='hi',
                               body='hi',
                               sender=user1,
                               recipient=user2)
        print response.status_code
        self.assertEqual(Message.objects.count(), 1)
