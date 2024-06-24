import pytest
from django.urls import reverse
from task_manager.labels.models import Label
from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status


@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'password': 'testpassword',
        'first_name': 'Test',
        'last_name': 'User',
    }


@pytest.fixture
def authenticated_user(client, user_data):
    user = User.objects.create_user(**user_data)
    client.login(
        username=user_data['username'],
        password=user_data['password']
    )
    return user


@pytest.fixture
def test_user():
    return User.objects.create_user(
        username='testuser2',
        password='testpassword2'
    )


@pytest.mark.django_db
def test_label_create(client, authenticated_user):
    label_data = {
        'name': 'New Label',
    }
    client.force_login(authenticated_user)

    response = client.get(reverse('label_create'))
    assert response.status_code == 200

    response = client.post(reverse('label_create'), label_data)
    assert response.status_code == 302

    created_label = Label.objects.filter(name=label_data['name']).first()
    assert created_label is not None
    assert created_label.name == label_data['name']


@pytest.mark.django_db
def test_label_no_authenticate(client):
    label_create_url = reverse('label_create')
    label_update_url = reverse('label_update', kwargs={'pk': 1})
    label_delete_url = reverse('label_delete', kwargs={'pk': 1})

    response = client.get(label_create_url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

    response = client.get(label_update_url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

    response = client.get(label_delete_url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_label_update(client, authenticated_user):
    test_label = Label.objects.create(name='Test Label')

    client.force_login(authenticated_user)

    response = client.get(reverse(
        'label_update',
        kwargs={'pk': test_label.pk})
    )
    assert response.status_code == 200

    updated_data = {
        'name': 'Label2',
    }
    response = client.post(reverse(
        'label_update',
        kwargs={'pk': test_label.pk}), updated_data
    )
    assert response.status_code == 302

    updated_label = Label.objects.get(pk=test_label.pk)
    assert updated_label.name == updated_data['name']


@pytest.mark.django_db
def test_label_delete(client, authenticated_user):
    test_label = Label.objects.create(name='Test Label')

    client.force_login(authenticated_user)

    response = client.get(reverse(
        'label_delete',
        kwargs={'pk': test_label.pk})
    )
    assert response.status_code == 200

    response = client.post(reverse(
        'label_delete',
        kwargs={'pk': test_label.pk})
    )
    assert response.status_code == 302

    deleted_label = Label.objects.filter(pk=test_label.pk).first()
    assert deleted_label is None


@pytest.mark.django_db
def test_label_delete_in_use(client, authenticated_user):
    test_label = Label.objects.create(name='Test Label')
    test_status = Status.objects.create(name='Test Status')
    test_task = Task.objects.create(
        name='Test Task',
        description='Description for Test Task',
        author=authenticated_user,
        status=test_status,
        executor=authenticated_user
    )
    test_task.labels.add(test_label)

    client.force_login(authenticated_user)

    response = client.post(reverse(
        'label_delete',
        kwargs={'pk': test_label.pk})
    )
    assert response.status_code == 302
    assert response.url == reverse('labels')

    existing_label = Label.objects.filter(pk=test_label.pk).exists()
    assert existing_label

    assert test_label in test_task.labels.all()
