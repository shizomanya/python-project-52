import pytest
from django.urls import reverse
from django.test import Client
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


@pytest.fixture
def test_user():
    user_data = {
        'username': 'testuser',
        'password': 'testpassword123'
    }
    user = User.objects.create_user(**user_data)
    return user


@pytest.fixture
def authenticated_user(client, test_user):
    client.login(username='testuser', password='testpassword123')
    return client, test_user


@pytest.mark.django_db
def test_status_create(authenticated_user):
    client, _ = authenticated_user
    status_data = {
        'name': 'New Status',
    }

    response = client.get(reverse('status_create'))
    assert response.status_code == 200

    response = client.post(reverse('status_create'), status_data)
    assert response.status_code == 302

    created_status = Status.objects.filter(name=status_data['name']).first()
    assert created_status is not None


@pytest.mark.parametrize('url_name', ['statuses', 'status_create'])
@pytest.mark.django_db
def test_status_no_authenticate(url_name):
    client = Client()

    response = client.get(reverse(url_name))
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_status_update(authenticated_user):
    client, _ = authenticated_user
    test_status = Status.objects.create(name='Test Status')

    response = client.get(reverse(
        'status_update',
        kwargs={'pk': test_status.pk})
    )
    assert response.status_code == 200

    updated_data = {
        'name': 'Status2',
    }
    response = client.post(reverse(
        'status_update',
        kwargs={'pk': test_status.pk}), updated_data
    )
    assert response.status_code == 302

    updated_status = Status.objects.filter(pk=test_status.pk).first()
    assert updated_status.name == updated_data['name']


@pytest.mark.django_db
def test_status_delete(authenticated_user):
    client, _ = authenticated_user
    test_status = Status.objects.create(name='Test Status')

    response = client.get(reverse(
        'status_delete',
        kwargs={'pk': test_status.pk})
    )
    assert response.status_code == 200

    response = client.post(reverse(
        'status_delete',
        kwargs={'pk': test_status.pk})
    )
    assert response.status_code == 302

    deleted_status = Status.objects.filter(pk=test_status.pk).first()
    assert deleted_status is None


@pytest.mark.django_db
def test_status_delete_in_use(authenticated_user):
    client, test_user = authenticated_user
    test_status = Status.objects.create(name='Test Status')
    test_executor = User.objects.create_user(
        username='executor',
        password='executorpassword'
    )
    Task.objects.create(
        name='Test Task',
        status=test_status,
        author=test_user,
        executor=test_executor
    )

    response = client.post(reverse(
        'status_delete',
        kwargs={'pk': test_status.pk})
    )

    if response.status_code == 302:
        response = client.get(response.url)

    assert response.status_code == 200

    existing_status = Status.objects.filter(pk=test_status.pk).exists()
    assert existing_status
