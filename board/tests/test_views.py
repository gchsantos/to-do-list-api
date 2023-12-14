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
        expected_status = 'PENDING'
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
        expected_status = 'PENDING'

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
            'status': 'pending'
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
        """ When request to create a task without specific your status \
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
            "status": "concluded"
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
        """ When request to create a task without specific your status \
        Then create a pending task and returns success message \
        """
        
        expected_status_code = 200
        expected_res_type = 'BulkTaskInsert'
        expected_res_msg = 'The tasks was inserted in your board successfully'
        expected_res_description = 'Insertion of task in user board'
        expected_task_title = 'Criar endpoint para exclusão de tarefas'
        expected_task_description = 'Criar exclusão específica e em massa'
        expected_task_status = TaskStatus.PENDING

        self.request.data = [{
            "title": "Criar endpoint para exclusão de tarefas",
            "description": "Criar exclusão específica e em massa",
        }]

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