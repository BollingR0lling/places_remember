from django.db.utils import IntegrityError
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Memory


class MemoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        test_user1 = User.objects.create_user(
            username='Mr.Robot',
            first_name='Eliot',
            last_name='Alderson'
        )
        test_user2 = User.objects.create_user(
            username='RealMr.Robot',
            first_name='Edward',
            last_name='Alderson'
        )
        Memory.objects.create(
            user=test_user1,
            location='США, Нью-Йорк',
            title='Я устроился работать в Allsafe',
            description='Я почти не помню, как я сюда устроился...'
        )
        Memory.objects.create(
            user=test_user2,
            location='CША, Нью-Йорк',
            title='Все только начинается...',
            description='Я наконец то устроился в Allsafe'
        )

    def test_field_labels(self):
        memories = Memory.objects.all()
        for memory in memories:
            self.assertEqual(memory._meta.get_field('user').verbose_name, 'Пользователь')
            self.assertEqual(memory._meta.get_field('location').verbose_name, 'Место')
            self.assertEqual(memory._meta.get_field('title').verbose_name, 'Воспоминание')
            self.assertEqual(memory._meta.get_field('description').verbose_name, 'Описание')

    def test_title_length(self):
        memories = Memory.objects.all()
        for memory in memories:
            self.assertEqual(memory._meta.get_field('title').max_length, 50)

    def test_object_name(self):
        user = User.objects.get(id=1)
        expected_object_name = f'{user.first_name, user.last_name}, воспоминание: Я устроился работать в Allsafe'
        memory = Memory.objects.get(user=user)
        self.assertEqual(str(memory), expected_object_name)

    def test_nullable_fields(self):
        user = User.objects.get(id=2)
        try:
            a = Memory.objects.create(
                user=user,
                location=None,
                title=None,
                description=None
            )
            a.save()
        except IntegrityError:
            self.assertTrue(True)
