# Create your tests here.
import datetime
from django.utils import timezone
from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from my_auth.models import OAuthUser
from booking.models import Booking


class SimpleTest(TestCase):
    def setUp(self):
        # User objects.Non auth user
        self.user1 = OAuthUser.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        # Auth user
        self.user2 = OAuthUser.objects.create_user('temporary2', 'temporary_second@gmail.com', 'temporary')

        self.user2.is_auth = True
        self.user2.save()

        # Auth user
        self.user3 = OAuthUser.objects.create_user('temporary3', 'temporary_third@gmail.com', 'temporary')

        self.user3.is_banned = True
        self.user3.save()

        # Create Booking object
        self.order = Booking(user=self.user2, swim_lane=3, start_date=datetime.datetime.now().date(),
                             start_time='11:30:00', end_time='12:00:00')
        self.order.save()
        # non exists order id
        self.fake_id = 9999

        self.client = Client()

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()
        self.order.delete()

    ########################
    # List of orders - GET #
    ########################
    def test_get_booking_list(self):
        url = reverse('booking_list_api')

        # Get by non login user
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # Get by no auth user
        self.client.login(email='temporary@gmail.com', password='temporary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # Get by banned user
        self.client.login(email='temporary_third@gmail.com', password='temporary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # Get by auth user
        self.client.login(email='temporary_second@gmail.com', password='temporary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    #########################
    # List of orders - POST #
    #########################
    def test_post_booking_list(self):
        url = reverse('booking_list_api')
        post = {'start_date': datetime.datetime.now().date(), 'start_time': '11:30:00', 'end_time': '12:00:00'}
        post_invalid_date_max = {'start_date': datetime.datetime.now().date() + datetime.timedelta(days=6),
                                 'start_time': '11:30:00', 'end_time': '12:00:00'}
        post_invalid_date_min = {'start_date': datetime.datetime.now().date() - datetime.timedelta(days=2),
                                 'start_time': '11:30:00', 'end_time': '12:00:00'}
        post_invalid_time = {'start_date': datetime.datetime.now().date(), 'start_time': '11:31:00',
                             'end_time': '12:00:00'}

        # Post by non login user
        response = self.client.post(url, post)
        self.assertEqual(response.status_code, 403)

        # Post by no auth user
        self.client.login(email='temporary@gmail.com', password='temporary')
        response = self.client.post(url, post)
        self.assertEqual(response.status_code, 403)

        # Post by banned user
        self.client.login(email='temporary_third@gmail.com', password='temporary')
        response = self.client.post(url, post)
        self.assertEqual(response.status_code, 403)

        # Post by auth user
        self.client.login(email='temporary_second@gmail.com', password='temporary')
        response = self.client.post(url, post)
        self.assertEqual(response.status_code, 201)

        # Post by auth user with invalid date - max
        response = self.client.post(url, post_invalid_date_max)
        self.assertEqual(response.status_code, 400)

        # Post by auth user with invalid date - post past date
        response = self.client.post(url, post_invalid_date_min)
        # print(response.content)
        self.assertEqual(response.status_code, 400)

        # Post by auth user with invalid time
        response = self.client.post(url, post_invalid_time)
        self.assertEqual(response.status_code, 400)

        # Post if fully booked at this time(6 lines)
        self.client.post(url, post)  # 3
        self.client.post(url, post)  # 4
        self.client.post(url, post)  # 5
        self.client.post(url, post)  # 6
        response = self.client.post(url, post)  # 7
        self.assertEqual(response.status_code, 400)

    def test_delete_order(self):
        url_detail = reverse('booking_detail_api', args=(self.order.id,))

        # delete order by no login user
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, 403)

        # delete order by no auth user
        self.client.login(email='temporary@gmail.com', password='temporary')
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, 403)
        '''
        # delete order by auth user, but no owner this order
        self.client.login(email='temporary@gmail.com', password='temporary')
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, 403)
        '''
        # delete order by auth user and owner this order
        self.client.login(email='temporary_second@gmail.com', password='temporary')
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, 204)
