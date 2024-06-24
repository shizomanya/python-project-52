import pytest
from django.urls import reverse
from django.test import Client
from task_manager.tasks.models import Task
from task_manager.users.models import User
from task_manager.statuses.models import Status

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def authenticated_user(db, test_user):
    client = Client()
    client.login(username='testuser', password='testpassword')
    return client, test_user

@pytest.fixture
def test_status(db):
    return Status.objects.create(name='Test Status')

@pytest.fixture
def test_executor(db):
    return User.objects.create_user(username='testexecutor', password='testpassword')

@pytest.fixture
def test_task(db, test_user, test_status, test_executor):
    return Task.objects.create(
        name='Test Task',
        description='Description for Test Task',
        author=test_user,
        status=test_status,
        executor=test_executor
    )

@pytest.fixture
def task_data(test_status, test_executor):
    return {
        'name': 'Task1',
        'description': 'Description for Task1',
        'status': test_status.id,
        'executor': test_executor.id,
    }

@pytest.mark.django_db
def test_task_create(authenticated_user, task_data):
    client, test_user = authenticated_user
    assert Task.objects.count() == 0

    create_url = reverse('task_create')
    response = client.get(create_url)
    assert response.status_code == 200

    task_data['author'] = test_user.id  # Use the test user's ID
    response = client.post(create_url, task_data, follow=True)
    assert response.status_code == 200

    assert Task.objects.filter(name=task_data['name']).exists()

@pytest.mark.parametrize('url_name', ['tasks', 'task_create'])
@pytest.mark.django_db
def test_task_no_authenticate(client, url_name):
    url = reverse(url_name)
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_task_update(authenticated_user, test_task, test_status, test_executor):
    client, test_user = authenticated_user
    update_url = reverse('task_update', args=[test_task.pk])

    response = client.get(update_url)
    assert response.status_code == 200

    updated_data = {
        'name': 'Task2',
        'description': 'Updated description for Task2',
        'status': test_status.id,
        'executor': test_executor.id,
        'author': test_user.id,  # ensure the author is included
    }
    response = client.post(update_url, updated_data, follow=True)
    assert response.status_code == 200

    updated_task = Task.objects.get(pk=test_task.pk)
    assert updated_task.name == 'Task2'

@pytest.mark.django_db
def test_task_delete(authenticated_user, test_task):
    client, test_user = authenticated_user
    delete_url = reverse('task_delete', args=[test_task.pk])

    response = client.get(delete_url)
    assert response.status_code == 200

    response = client.post(delete_url, follow=True)
    assert response.status_code == 200

    assert not Task.objects.filter(pk=test_task.pk).exists()

@pytest.mark.django_db
def test_task_delete_another_user(client, test_task):
    another_user = User.objects.create_user(username='anotheruser', password='password')
    client.force_login(another_user)

    delete_url = reverse('task_delete', args=[test_task.pk])

    response = client.post(delete_url)
    assert response.status_code == 302  # Check for forbidden status

    assert Task.objects.filter(pk=test_task.pk).exists()
