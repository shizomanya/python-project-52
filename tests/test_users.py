import pytest
from django.urls import reverse
from task_manager.users.models import User
from django.test import Client

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
    client.login(username=user_data['username'], password=user_data['password'])
    return user

@pytest.fixture
def test_user():
    return User.objects.create_user(username='testuser2', password='testpassword2')


@pytest.mark.django_db
def test_user_signup(client: Client):
    user_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'password1': 'testpassword',
        'password2': 'testpassword',
        'username': 'testuser',
    }

    assert User.objects.count() == 0    

    signup_url = reverse('sign_up')
    response = client.post(signup_url, user_data)

    assert response.status_code == 302

    assert User.objects.filter(username=user_data['username']).exists()


@pytest.mark.django_db
def test_user_update(client: Client):
    authenticated_user = User.objects.create_user(
        username='testuser',
        password='testpassword'
    )

    client.force_login(authenticated_user)
    update_url = reverse('user_update', args=[authenticated_user.pk])

    response = client.get(update_url)
    assert response.status_code == 200

    new_data = {
        'username': 'updateduser',
        'first_name': 'Updated',
        'last_name': 'User',
        'password1': 'new_valid_password',
        'password2': 'new_valid_password',
    }

    response = client.post(update_url, new_data)

    assert response.status_code == 302

    updated_user = User.objects.get(pk=authenticated_user.pk)
    assert updated_user.username == 'updateduser'
    assert updated_user.first_name == 'Updated'
    assert updated_user.last_name == 'User'


@pytest.mark.django_db
def test_user_update_no_authenticate(client, test_user):
    update_url = reverse('user_update', args=[test_user.pk])
    response = client.get(update_url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_update_another_user(client, authenticated_user):
    another_user = User.objects.create_user(
        username='anotheruser',
        password='password'
    )
    update_url = reverse('user_update', args=[another_user.pk])
    response = client.get(update_url)
    assert response.status_code == 302
    assert response.url == reverse('users')


@pytest.mark.django_db
def test_user_delete(client, authenticated_user):
    delete_url = reverse('user_delete', args=[authenticated_user.pk])
    response = client.post(delete_url)
    assert response.status_code == 302
    assert not User.objects.filter(pk=authenticated_user.pk).exists()


@pytest.mark.django_db
def test_user_delete_no_authenticate(client, test_user):
    delete_url = reverse('user_delete', args=[test_user.pk])
    response = client.post(delete_url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_delete_another_user(client, authenticated_user):
    another_user = User.objects.create_user(
        username='anotheruser',
        password='password'
    )
    delete_url = reverse('user_delete', args=[another_user.pk])
    response = client.post(delete_url)
    assert response.status_code == 302
    assert response.url == reverse('users')
