from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from contacts.models import CustomUser, Contacts, ContactStatus


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='root')
        self.user_2 = CustomUser.objects.create_user(username='testuser2', password='root')
        self.status_default = ContactStatus.objects.create(code='default', title='Default', is_active=True)
        self.status_blocked = ContactStatus.objects.create(code='blocked', title='Blocked', is_active=True)
        self.client.force_authenticate(user=self.user)

    def create_contacts(self):
        """Valid users"""
        cities = [
            "Warsaw", "Krakow", "Lodz", "Wroclaw", "Poznan", "Gdansk", "Szczecin", "Bydgoszcz", "Lublin",
            "Bialystok", "Katowice"
        ]
        contacts_to_create = []
        for i in range(11):
            contacts_to_create.append(
                Contacts(
                    owner=self.user,
                    first_name=f'User{i}',
                    last_name=f'CD_{i:02d}',
                    phone=f'+481234000{i:02d}',
                    email=f'user{i}@example.com',
                    city=cities[i],
                    status=self.status_default,
                )
            )
        contacts = Contacts.objects.bulk_create(contacts_to_create,  ignore_conflicts=False)
        return contacts


class ContactsListTests(BaseAPITestCase):
    """GET path('contacts/', ContactsApiView.as_view(), name='contacts')"""
    LIST_URL = reverse('contacts:contacts')

    def test_unauthenticated_user_cannot_access_list(self):
        self.client.logout()
        response = self.client.get(self.LIST_URL)
        self.assertEqual(response.status_code, 401)

    def test_get_contacts_list_with_pagination(self):
        self.create_contacts()

        response = self.client.get(self.LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('results', response.data)
        self.assertIn('count', response.data)

        self.assertEqual(response.data['count'], 11)
        self.assertEqual(len(response.data['results']), 10)

    def test_ordering_by_last_name_asc(self):
        self.create_contacts()

        response = self.client.get(self.LIST_URL, {'ordering': 'last_name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        last_names = [item['last_name'] for item in response.data['results']]
        self.assertEqual(last_names, sorted(last_names))

    def test_ordering_by_last_name_desc(self):
        self.create_contacts()

        response = self.client.get(self.LIST_URL, {'ordering': '-last_name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        last_names = [item['last_name'] for item in response.data['results']]
        self.assertEqual(last_names, sorted(last_names, reverse=True))

    def test_ordering_by_created_at_asc(self):
        self.create_contacts()

        response = self.client.get(self.LIST_URL,{'ordering': 'created_at'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        created_dates = [item['created_at'] for item in response.data['results']]
        self.assertEqual(created_dates, sorted(created_dates))

    def test_ordering_by_created_at_desc(self):
        self.create_contacts()

        response = self.client.get(self.LIST_URL, {'ordering': '-created_at'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        created_dates = [item['created_at'] for item in response.data['results']]
        self.assertEqual(created_dates, sorted(created_dates, reverse=True))

    def test_invalid_ordering_is_ignored(self):
        self.create_contacts()

        response = self.client.get(self.LIST_URL, {'ordering': 'invalid_field'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('results', response.data)
        self.assertEqual(response.data['count'], 11)

        last_names = [item['last_name'] for item in response.data['results']]
        self.assertEqual(len(last_names), 10)


class ContactsCreateTests(BaseAPITestCase):
    """POST path('contacts/', ContactsApiView.as_view(), name='contacts')"""
    LIST_URL = reverse('contacts:contacts')

    def test_unauthenticated_user_cannot_access_list(self):
        self.client.logout()
        payload = {'first_name': 'User',}
        response = self.client.post(self.LIST_URL, payload, format='json')
        self.assertEqual(response.status_code, 401)

    def test_create_contact_with_default_status(self):
        payload = {
            'first_name': 'User',
            'last_name': 'cu_1',
            'phone': '+48123400001',
            'email': 'user1@example.com',
            'city': 'Warsaw',
        }

        response = self.client.post(self.LIST_URL, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'User')
        self.assertEqual(response.data['status']['code'], 'default')

        contact = Contacts.objects.get(email='user1@example.com')
        self.assertEqual(contact.owner, self.user)

    def test_create_contact_with_invalid_status_code(self):
        payload = {
            'first_name': 'User',
            'last_name': 'cu_2',
            'phone': '+48123400002',
            'email': 'user2@example.com',
            'city': 'Gdansk',
            'status_code': 'unknown',
        }

        response = self.client.post(self.LIST_URL, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status_code', response.data)


class ContactDetailTests(BaseAPITestCase):
    """"GET path('contacts/<int:contact_id>/', ContactApiView.as_view(), name='contact')"""

    def setUp(self):
        super().setUp()
        self.contact = Contacts.objects.create(
            owner=self.user,
            first_name='user1',
            last_name='cd_1',
            phone='+48123401002',
            email='user1@example.com',
            city='Warsaw',
            status=self.status_default
        )
        self.url = reverse('contacts:contact', kwargs={'contact_id': self.contact.id})
        self.invalid_url = reverse('contacts:contact', kwargs={'contact_id': 9999})

    def test_unauthenticated_user_cannot_access_list(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_get_existing_contact(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.contact.id)
        self.assertEqual(response.data['first_name'], 'user1')
        self.assertEqual(response.data['status']['code'], 'default')

    def test_get_nonexistent_contact(self):
        response = self.client.get(self.invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ContactUpdateTests(BaseAPITestCase):
    """PUT path('contacts/<int:contact_id>/', ContactApiView.as_view(), name='contact')"""

    def setUp(self):
        super().setUp()
        self.contact = Contacts.objects.create(
            owner=self.user,
            first_name='user_1',
            last_name='cd_1',
            phone='+48123400010',
            email='putuser@example.com',
            city='Poznan',
            status=self.status_default
        )
        self.UPDATE_URL = reverse('contacts:contact', kwargs={'contact_id': self.contact.id})

    def test_unauthenticated_user_cannot_access_list(self):
        self.client.logout()
        payload = {'status_code': 'blocked'}
        response = self.client.put(self.UPDATE_URL, payload, format='json')
        self.assertEqual(response.status_code, 401)

    def test_update_contact_status(self):
        payload = {'status_code': 'blocked'}

        response = self.client.put(self.UPDATE_URL, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status']['code'], 'blocked')

        self.contact.refresh_from_db()
        self.assertEqual(self.contact.status.code, 'blocked')

    def test_update_contact_with_invalid_status_code(self):
        payload = {'status_code': 'does_not_exist'}

        response = self.client.put(self.UPDATE_URL, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status_code', response.data)


class ContactDeleteTests(BaseAPITestCase):
    """DELETE path('contacts/<int:contact_id>/', ContactApiView.as_view(), name='contact')"""

    def setUp(self):
        super().setUp()
        self.contact = Contacts.objects.create(
            owner=self.user,
            first_name='user_1',
            last_name='cd_1',
            phone='+48123400010',
            email='putuser@example.com',
            city='Poznan',
            status=self.status_default
        )
        self.url = reverse('contacts:contact', kwargs={'contact_id': self.contact.id})
        self.invalid_url = reverse('contacts:contact', kwargs={'contact_id': 9999})

    def test_unauthenticated_user_cannot_access_list(self):
        self.client.logout()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 401)

    def test_delete_existing_contact(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Contacts.objects.filter(id=self.contact.id).exists())

    def test_delete_nonexistent_contact(self):
        response = self.client.delete(self.invalid_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CityWeatherAPITests(APITestCase):
    """GET path('weather/', CityWeatherAPIView.as_view(), name='city-weather')"""
    WEATHER_URL = reverse('contacts:city-weather')

    def test_get_weather_success(self):
        response = self.client.get(self.WEATHER_URL, {'city': 'Wroclaw'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('city', response.data)
        self.assertIn('temperature', response.data)
        self.assertEqual(response.data['city'].lower(), 'wroclaw')

    def test_get_weather_invalid_city(self):
        response = self.client.get(self.WEATHER_URL, {'city': 'ranotor'})

        self.assertIn(response.status_code, [status.HTTP_502_BAD_GATEWAY, status.HTTP_400_BAD_REQUEST])
        self.assertIn('detail', response.data)



class ContactsBulkImportTests(BaseAPITestCase):
    """POST path('contacts/bulk/', ContactsBulkImportApiView.as_view(), name='contacts_bulk') """
    URL = reverse('contacts:contacts_bulk')

    def test_unauthenticated_user_cannot_access_list(self):
        self.client.logout()
        csv_content = (
            "first_name,last_name,phone,email,city\n"
            "user_1,cd_1,+48123456701,user1@example.com,Wroclaw\n"
            "user_2,cd_2,+48123456702,user2@example.com,Krakow\n"
        )
        csv_file = SimpleUploadedFile("contacts.csv", csv_content.encode('utf-8'), content_type="text/csv")
        response = self.client.post(self.URL, {'file': csv_file}, format='multipart')
        self.assertEqual(response.status_code, 401)

    def test_bulk_import_success(self):
        csv_content = (
            "first_name,last_name,phone,email,city\n"
            "user_1,cd_1,+48123456701,user1@example.com,Wroclaw\n"
            "user_2,cd_2,+48123456702,user2@example.com,Krakow\n"
        )
        csv_file = SimpleUploadedFile("contacts.csv", csv_content.encode('utf-8'), content_type="text/csv")

        response = self.client.post(self.URL, {'file': csv_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['created'], 2)

        self.assertEqual(Contacts.objects.filter(owner=self.user).count(), 2)
        self.assertTrue(Contacts.objects.filter(first_name='user_1').exists())
        self.assertTrue(Contacts.objects.filter(first_name='user_2').exists())

    def test_bulk_import_with_invalid_row(self):
        csv_content = (
            "first_name,last_name,phone,email,city\n"
            "user_1,cd_1,+4812345670,john@example.com,Wroclaw\n"
            "user_2,cd_2,+48123456702,jane@example.com,Krakow\n"
        )
        csv_file = SimpleUploadedFile("contacts.csv", csv_content.encode('utf-8'), content_type="text/csv")

        response = self.client.post(self.URL, {'file': csv_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)
        self.assertEqual(len(response.data['errors']), 1)
        self.assertEqual(response.data['errors'][0]['row'], 1)
        self.assertIn('phone', response.data['errors'][0]['errors'])


class ContactsIsolationTests(BaseAPITestCase):
    LIST_URL = reverse('contacts:contacts')

    def test_list_shows_only_own_contacts(self):
        # invisible
        Contacts.objects.create(
            owner=self.user_2, first_name='Other', last_name='User', phone='+48123450001',
            email='other@example.com', city='Gdansk', status=self.status_default
        )
        # visible
        Contacts.objects.create(
            owner=self.user, first_name='Mine', last_name='User', phone='+48123450002', email='mine@example.com',
            city='Warsaw', status=self.status_default
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', [])
        self.assertTrue(any(item['first_name'] == 'Mine' for item in results))
        self.assertFalse(any(item['first_name'] == 'Other' for item in results))

    def test_get_other_users_contact_returns_404(self):
        other_contact = Contacts.objects.create(
            owner=self.user_2, first_name='Other', last_name='User', phone='+48123450003', email='other2@example.com',
            city='Krakow', status=self.status_default
        )

        url = reverse('contacts:contact', kwargs={'contact_id': other_contact.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_other_users_contact_forbidden(self):
        other_contact = Contacts.objects.create(
            owner=self.user_2, first_name='Other', last_name='User', phone='+48123450004', email='other3@example.com',
            city='Lodz', status=self.status_default
        )

        url = reverse('contacts:contact', kwargs={'contact_id': other_contact.id})
        payload = {'first_name': 'fooled'}

        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        other_contact.refresh_from_db()
        self.assertEqual(other_contact.first_name, 'Other')

    def test_delete_other_users_contact_forbidden(self):
        other_contact = Contacts.objects.create(
            owner=self.user_2, first_name='Other', last_name='User', phone='+48123450005', email='other4@example.com',
            city='Lublin', status=self.status_default
        )

        url = reverse('contacts:contact', kwargs={'contact_id': other_contact.id})

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Contacts.objects.filter(id=other_contact.id).exists())
