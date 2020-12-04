from django.test import TestCase
from django.contrib.auth.models import User
import typing as t
from ..models import Memory
from ..forms import MemoryModelForm


class MockLogic:
    @staticmethod
    def home(user: User):
        return Memory.objects.filter(user=user)

    @staticmethod
    def add_memory(user: User, form_data: t.Dict[str, str]):
        form = MemoryModelForm(data=form_data)
        if form.is_valid():
            memory = Memory.objects.create(
                user=user,
                location=form_data['location'],
                title=form_data['title'],
                description=form_data['description'],
            )
            memory.save()

    @staticmethod
    def delete_memory(memory_id: int):
        memory = Memory.objects.get(id=memory_id)
        memory.delete()


class ViewsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create_user(
            username='Mr.Robot',
            first_name='Eliot',
            last_name='Alderson',
        )

    def test_home(self):
        mock = MockLogic()
        user = User.objects.get(id=3)
        test_memory1 = Memory.objects.create(
            user=user,
            location='США, Нью-Йорк',
            title='Я устроился работать в Allsafe',
            description='Я почти не помню, как я сюда устроился...'
        )
        test_memory2 = Memory.objects.create(
            user=user,
            location='CША, Нью-Йорк',
            title='Все только начинается...',
            description='Я наконец то устроился в Allsafe'
        )
        self.assertEqual(list(mock.home(user)), [test_memory1, test_memory2])
        self.assertEqual(len(mock.home(user)), 2)

    def test_add_memory(self):
        mock = MockLogic()
        user = User.objects.get(id=3)
        form_data = {
            'location': 'США, Нью-Йорк',
            'title': 'Я устроился работать в Allsafe',
            'description': 'Я почти не помню, как я сюда устроился...'
        }
        self.assertEqual(len(Memory.objects.all()), 0)
        mock.add_memory(user, form_data)
        self.assertEqual(len(Memory.objects.all()), 1)
        incorrect_data = {
            'location': 'Место которого не существует',
            'title': 'Я устроился работать в Allsafe',
            'description': 'Я почти не помню, как я сюда устроился...'
        }
        mock.add_memory(user, incorrect_data)
        self.assertEqual(len(Memory.objects.all()), 1)

    def test_delete_memory(self):
        mock = MockLogic()
        user = User.objects.get(id=3)
        test_memory1 = Memory.objects.create(
            user=user,
            location='США, Нью-Йорк',
            title='Я устроился работать в Allsafe',
            description='Я почти не помню, как я сюда устроился...'
        )
        test_memory1.save()
        mock.delete_memory(test_memory1.id)
        self.assertFalse(Memory.objects.all())
