import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.management import call_command


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
   with django_db_blocker.unblock():
       call_command('loaddata', 'fixture.json')


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def get_authorized_client(api_client):
    def get_client(user_id):
        if user_id:
            user = User.objects.get(pk=user_id)
            api_client.force_authenticate(user=user)
        return api_client

    return get_client


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('user', 'status_code'), [
        ('', 401),
        (1, 200),
        (2, 200),
        (3, 200),
        (4, 200),
    ]
)
def test_user_request(user, status_code, get_authorized_client):
    client = get_authorized_client(user)
    url = reverse('task-list')
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('user', 'task', 'status_code'), [
        # Permission denied
        ('', 1, 401),
        # Not Found
        (1, 99, 404),
        (2, 99, 404),
        (4, 99, 404),
        # Found
        (1, 1, 200),
        (2, 1, 200),
        (4, 1, 200),
    ]
)
def test_task_retrieve(user, task, status_code, get_authorized_client):
    client = get_authorized_client(user)
    url = reverse('task-detail', kwargs={'pk': task})
    response = client.get(url)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('user', 'title', 'description', 'priority', 'deadline', 'status_code'), [
        # Permission denied
        ('', '', '', '', '', 401),
        (1, '', '', '', '', 403),
        (4, '', '', '', '', 403),
        # Invalid
        (2, 'Test task', '', '', '', 400),
        (2, '', 'Teet description', '', '', 400),
        # Valid
        (2, 'Test task', 'Test description', '', '', 201),
        (3, 'Test task', 'Test description', '1', '', 201),
        (3, 'Test task', 'Test description', '1', '2021-10-03 08:00:00+00:00', 201),
    ]
)
def test_task_create(user, title, description, priority, deadline, status_code, get_authorized_client):
    client = get_authorized_client(user)
    url = reverse('task-list')
    data = {
        'user': user, 
        'title': title, 
        'description': description,
        'priority': priority, 
        'deadline': deadline
    }

    response = client.post(url, data=data)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('user', 'id', 'title', 'description', 'status_code'), [
        # Permission denied
        ('', 1, 'Updated task', 'Updated description', 401),
        (4, 1, 'Updated task', 'Updated description', 403),
        (3, 1, 'Updated task', 'Updated description', 403),
        # Not Found
        (1, 99, 'Updated task', 'Updated description', 404),
        # Invalid
        (2, 1, '', '', 400),
        (2, 1, 'Updated task', '', 400),
        (2, 1, '', 'Updated description', 400),
        (1, 1, '', '', 400),
        (1, 1, 'Updated task', '', 400),
        (1, 1, '', 'Updated description', 400),
        # Valid
        (2, 1, 'Updated task', 'Updated description', 200),
        (1, 1, 'Updated task', 'Updated description', 200),
    ]
)
def test_task_update(user, id, title, description, status_code, get_authorized_client):
    client = get_authorized_client(user)
    url = reverse('task-detail', kwargs={'pk': id})
    data = {
        'id': id,
        'user': user, 
        'title': title, 
        'description': description
    }

    response = client.put(url, data=data)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('user', 'id', 'data', 'status_code'), [
        # Permission denied
        ('', 1, {}, 401),
        (4, 1, {}, 403),
        (3, 1, {}, 403),
        # Not Found
        (1, 99, {}, 404),
        # Valid
        (2, 1, {}, 200),
        (2, 1, {'title': 'Updated task'}, 200),
        (2, 1, {'priority': 1}, 200),
        (1, 1, {'description': 'Updated description'}, 200),
        (1, 1, {'deadline': '2021-10-03 08:00:00+00:00'}, 200),
    ]
)
def test_task_partial_update(user, id, data, status_code, get_authorized_client):
    client = get_authorized_client(user)
    url = reverse('task-detail', kwargs={'pk': id})
    data = {
        'id': id,
        'user': user, 
        **data
    }

    response = client.patch(url, data=data)
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('user', 'task', 'status_code'), [
        # Permission denied
        ('', 1, 401),
        (3, 1, 403),
        (4, 1, 403),
        # Valid
        (1, 1, 204),
        (2, 1, 204),
    ]
)
def test_task_delete(user, task, status_code, get_authorized_client):
    client = get_authorized_client(user)
    url = reverse('task-detail', kwargs={'pk': task})
    response = client.delete(url)
    assert response.status_code == status_code
