from django.test import TestCase
from django.contrib.auth.models import User
from django.http import HttpRequest

from board.models import Task, TaskStatus
from board.views import BoardManager
from board.messages import TaskInsertDataMessage
from board.exceptions import TaskDoesNotExistException

mock_tasks = [
    {
        "title": "Criar a rota de autenticação",
        "description": "Não esquecer de usar token!"
    },
    {"title": "Criar .env com as credenciais locais"},
    {
        "title": "Realizar a migração dos modelos", 
        "status": TaskStatus.CANCELED
    },
    {
        "title": "Instalar requests nas dependencias", 
        "status": TaskStatus.CONCLUDED
    },
]

def create_mocked_tasks(mock_tasks: [], user: User):
    bulk_tasks = []
    for task in mock_tasks:
        bulk_tasks.append(Task(user=user, **task))
    return Task.objects.bulk_create(bulk_tasks)

class BatchManagerViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.view = BoardManager()
        cls.user = User.objects.create(username='user', id=1)
        cls.another_user = User.objects.create(username='another_user', id=2)
        cls.mock_user_tasks = create_mocked_tasks(mock_tasks, cls.user)
        cls.mock_another_user_tasks = create_mocked_tasks(
            mock_tasks, cls.another_user
        )

    def setUp(self):
        self.request = HttpRequest()
        self.request.user = self.user
        
    def test_get(self):
        """
        When request to get non-specific task infos \
        Then returns all pending tasks for authenticated user \
        """
        
        expected_status_code = 200
        expected_task_quantity = 2
        expected_task_1_title = 'Criar a rota de autenticação'
        expected_task_1_description = 'Não esquecer de usar token!'
        expected_task_2_title = 'Criar .env com as credenciais locais'
        expected_task_2_description = None
        expected_status = TaskStatus.PENDING.name
        expected_task_keys =  [
            'id', 'title', 'description', 'status', 'statusLabel', 'createdAt',
            'updatedAt'
        ]

        response = self.view.get(self.request)

        self.assertEqual(expected_status_code, response.status_code)

        res_data = response.data
        task_keys = [key for key in res_data[0].keys()]
        self.assertEqual(expected_task_quantity, len(response.data))
        self.assertEqual(expected_task_1_title, res_data[0].get("title"))
        self.assertEqual(expected_task_1_description, res_data[0].get("description"))
        self.assertEqual(expected_task_2_title, res_data[1].get("title"))
        self.assertEqual(expected_task_2_description, res_data[1].get("description"))
        self.assertEqual(expected_status, res_data[0].get("status"))
        self.assertEqual(expected_status, res_data[1].get("status"))
        self.assertEqual(expected_task_keys, task_keys)

    def test_get_specific_task(self):
        """
        When request to get specific task infos through the task_id \
        Then returns only the specific task of the authenticated user  \
        """
        
        task_id = self.mock_user_tasks[0].id
        expected_status_code = 200
        expected_title = 'Criar a rota de autenticação'
        expected_description = 'Não esquecer de usar token!'
        expected_status = TaskStatus.PENDING.name

        response = self.view.get(self.request, task_id=task_id)

        self.assertEqual(expected_status_code, response.status_code)

        res_data = response.data[0]
        self.assertEqual(expected_title, res_data.get("title"))
        self.assertEqual(expected_description, res_data.get("description"))
        self.assertEqual(expected_status, res_data.get("status"))

    def test_get_another_user_task(self):
        """
        When request a task infos from another user through the task_id \
        Then not returns the task and return TaskDoesNotExistError \
        """
        
        task_id = self.mock_another_user_tasks[0].id
        expected_status_code = 400
        expected_response_type = 'TaskDoesNotExistError'

        response = self.view.get(self.request, task_id=task_id)

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_response_type, response.data.get("type"))
        self.assertRaises(TaskDoesNotExistException)
    
    def test_get_with_filters(self):
        """
        When request a task infos from another user through the task_id \
        Then not returns the task and return TaskDoesNotExistError \
        """
        
        self.request.query_params = {
            'title__icontains': 'criar',
            'description__icontains': 'token',
            'status': TaskStatus.PENDING.name
        }

        expected_status_code = 200
        expected_task_quantity = 1
        

        response = self.view.get(self.request)
        res_data = response.data

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_task_quantity, len(res_data))

    def test_post(self):
        """ When request to create a task without specific your status \
        Then create a pending task and returns success message \
        """
        
        expected_status_code = 200
        expected_res_type = 'TaskInsert'
        expected_res_msg = 'The task was inserted in your board successfully'
        expected_res_description = 'Insertion of task in user board'
        expected_task_title = 'Criar endpoint para exclusão de tarefas'
        expected_task_description = 'Criar exclusão específica e em massa'
        expected_task_status = TaskStatus.PENDING

        self.request.data = {
            "title": "Criar endpoint para exclusão de tarefas",
            "description": "Criar exclusão específica e em massa",
        }

        response = self.view.post(self.request)

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_res_type, response.data.get('type'))
        self.assertEqual(expected_res_msg, response.data.get('message'))
        self.assertEqual(
            expected_res_description, response.data.get('description')
        )

        task = Task.objects.filter(
            title=expected_task_title,
            description=expected_task_description,
            status=expected_task_status,
        )
        self.assertTrue(task)

    def test_post_with_specific_status(self):
        """ When request to create a task specifying your status \
        Then create a pending task and returns success message \
        """
        
        expected_status_code = 200
        expected_res_type = 'TaskInsert'
        expected_res_msg = 'The task was inserted in your board successfully'
        expected_res_description = 'Insertion of task in user board'
        expected_task_title = 'Criar endpoint para exclusão de tarefas'
        expected_task_description = 'Criar exclusão específica e em massa'
        expected_task_status = TaskStatus.CONCLUDED

        self.request.data = {
            "title": "Criar endpoint para exclusão de tarefas",
            "description": "Criar exclusão específica e em massa",
            "status": TaskStatus.CONCLUDED.name
        }

        response = self.view.post(self.request)

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_res_type, response.data.get('type'))
        self.assertEqual(expected_res_msg, response.data.get('message'))
        self.assertEqual(
            expected_res_description, response.data.get('description')
        )

        task = Task.objects.filter(
            title=expected_task_title,
            description=expected_task_description,
            status=expected_task_status,
        )
        self.assertTrue(task)

    def test_post_bulk_task(self):
        """ When request to create multiple tasks through an array \
        Then create all the tasks and returns success message \
        """
        
        expected_status_code = 200
        expected_res_type = 'BulkTaskInsert'
        expected_res_msg = 'The tasks was inserted in your board successfully'
        expected_tasks_quantity = 3

        self.request.data = [
            {
                "title": "bulk title 1",
                "description": "bulk description 1",
                "status": TaskStatus.PENDING.name,
            },
            {
                "title": "bulk title 2",
                "description": "bulk description 2",
                "status": TaskStatus.CONCLUDED.name,
            },
            {
                "title": "bulk title 3",
                "description": "bulk description 3",
                "status": TaskStatus.CANCELED.name,
            },
        ]

        response = self.view.post(self.request)

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_res_type, response.data.get('type'))
        self.assertEqual(expected_res_msg, response.data.get('message'))
        

        tasks = Task.objects.filter(
            title__icontains='bulk',
            description__icontains='bulk',
        )
        self.assertEqual(expected_tasks_quantity, len(tasks))

        titles = [task.title for task in tasks]
        description = [task.description for task in tasks]
        status = [task.status for task in tasks]

        self.assertTrue((titles[0] != titles[1] != titles[2]))
        self.assertTrue((description[0] != description[1] != description[2]))
        self.assertTrue((status[0] != status[1] != status[2]))

    def test_put(self):
        """ When request to update a task without specific your status \
        Then change for concluded task and returns success message \
        """
        
        expected_status_code = 200
        expected_res_type = 'TaskUpdate'
        expected_res_msg = 'The task was updated successfully'
        expected_res_description = 'Updating of a task in user board'
        expected_old_status = TaskStatus.PENDING
        expected_new_status = TaskStatus.CONCLUDED

        task = Task.objects.create(
            title='Realizar um stress test na api',
            user=self.user
        )
        task_id = str(task.id)
        self.assertEqual(expected_old_status, task.status)

        response = self.view.put(self.request, task_id=task_id)

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_res_type, response.data.get('type'))
        self.assertEqual(expected_res_msg, response.data.get('message'))
        self.assertEqual(
            expected_res_description, response.data.get('description')
        )

        updated_task = Task.objects.get(id=task_id)
        self.assertEqual(expected_new_status, updated_task.status)

    def test_put_with_specific_status(self):
        """ When request to update a task specifying your status \
        Then change the tasks status and returns success message \
        """
        
        expected_status_code = 200
        expected_res_type = 'TaskUpdate'
        expected_res_msg = 'The task was updated successfully'
        expected_res_description = 'Updating of a task in user board'
        expected_old_status = TaskStatus.PENDING
        expected_new_status = TaskStatus.CONCLUDED

        task = Task.objects.create(
            title='Realizar um stress test na api',
            user=self.user
        )
        task_id = str(task.id)
        self.assertEqual(expected_old_status, task.status)

        self.request.data = {"status": TaskStatus.CONCLUDED.name}
        response = self.view.put(self.request, task_id=task_id)

        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_res_type, response.data.get('type'))
        self.assertEqual(expected_res_msg, response.data.get('message'))
        self.assertEqual(
            expected_res_description, response.data.get('description')
        )

        updated_task = Task.objects.get(id=task_id)
        self.assertEqual(expected_new_status, updated_task.status)

    def test_put_bulk_task(self):
        """ When request to update multiple tasks without specifying status \
        Then update all the tasks to concluded and returns success message \
        """
        
        expected_status_code = 200
        expected_res_type = 'BulkTaskUpdate'
        expected_res_msg = 'The tasks was updated successfully'
        expected_res_description = 'Multiple tasks update in user board'
        expected_tasks_quantity = 3
        expected_new_tasks_status = [TaskStatus.CONCLUDED] * 3

        mocked_tasks = [
            {"title": "bulk update 1"},
            {"title": "bulk update 2"},
            {
                "title": "bulk update 3", 
                "status": TaskStatus.CANCELED
            },
        ]

        tasks = create_mocked_tasks(mocked_tasks, self.user)
        self.request.data = [{'task': str(task.id)} for task in tasks]
        response = self.view.put(self.request)
        
        self.assertEqual(expected_status_code, response.status_code)
        self.assertEqual(expected_res_type, response.data.get('type'))
        self.assertEqual(expected_res_msg, response.data.get('message'))
        self.assertEqual(
            expected_res_description, response.data.get('description')
        )

        tasks = Task.objects.filter(title__icontains='bulk update')
        self.assertEqual(expected_tasks_quantity, len(tasks))

        titles = [task.title for task in tasks]
        status = [task.task_status for task in tasks]
        
        self.assertTrue((titles[0] != titles[1] != titles[2]))
        self.assertListEqual(expected_new_tasks_status, status)
