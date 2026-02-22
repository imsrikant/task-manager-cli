import json
import os
import tempfile
from unittest.mock import patch

import pytest
from task_manager import OPTIONS, Task, show_options


@pytest.fixture
def temp_dir(tmp_path, monkeypatch):
    """Change to a temporary directory for each test so tasks.json is isolated."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture
def task(temp_dir):
    """Create a Task instance with no pre-existing tasks.json."""
    return Task()


@pytest.fixture
def task_with_data(temp_dir):
    """Create a Task instance with some pre-existing tasks."""
    data = [
        {"title": "Buy groceries", "is_completed": False},
        {"title": "Clean house", "is_completed": True},
    ]
    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump(data, f)
    return Task()


class TestTaskInit:
    def test_init_no_file(self, temp_dir):
        t = Task()
        assert t._tasks == []

    def test_init_with_file(self, task_with_data):
        assert len(task_with_data._tasks) == 2
        assert task_with_data._tasks[0]["title"] == "Buy groceries"

    def test_init_invalid_json(self, temp_dir):
        with open("tasks.json", "w") as f:
            f.write("not valid json")
        t = Task()
        assert t._tasks == []


class TestIsTaskEmpty:
    def test_empty(self, task):
        assert task.is_task_empty() is True

    def test_not_empty(self, task_with_data):
        assert task_with_data.is_task_empty() is False


class TestIsValidIndex:
    def test_valid_index(self, task_with_data):
        assert task_with_data.is_valid_index(0) is True
        assert task_with_data.is_valid_index(1) is True

    def test_invalid_index(self, task_with_data):
        assert task_with_data.is_valid_index(-1) is False
        assert task_with_data.is_valid_index(2) is False
        assert task_with_data.is_valid_index(100) is False

    def test_empty_list(self, task):
        assert task.is_valid_index(0) is False


class TestAddTask:
    @patch("builtins.input", return_value="New Task")
    def test_add_task(self, mock_input, task):
        task.add_task()
        assert len(task._tasks) == 1
        assert task._tasks[0]["title"] == "New Task"
        assert task._tasks[0]["is_completed"] is False

    @patch("builtins.input", return_value="  ")
    def test_add_empty_title(self, mock_input, task, capsys):
        task.add_task()
        assert len(task._tasks) == 0
        assert "Please Enter valid title." in capsys.readouterr().out


class TestViewTask:
    def test_view_empty(self, task, capsys):
        task.view_task()
        assert "Task List is empty." in capsys.readouterr().out

    def test_view_tasks(self, task_with_data, capsys):
        task_with_data.view_task()
        output = capsys.readouterr().out
        assert "1: [ ] Buy groceries" in output
        assert "2: [X] Clean house" in output


class TestUpdateTask:
    def test_update_empty(self, task, capsys):
        task.update_task()
        assert "Task List is empty." in capsys.readouterr().out

    @patch("builtins.input", side_effect=["y", "1"])
    def test_update_task_toggle(self, mock_input, task_with_data):
        assert task_with_data._tasks[0]["is_completed"] is False
        task_with_data.update_task()
        assert task_with_data._tasks[0]["is_completed"] is True

    @patch("builtins.input", return_value="n")
    def test_update_task_cancel(self, mock_input, task_with_data):
        task_with_data.update_task()
        assert task_with_data._tasks[0]["is_completed"] is False


class TestDeleteTask:
    def test_delete_empty(self, task, capsys):
        task.delete_task()
        assert "Task List is empty." in capsys.readouterr().out

    @patch("builtins.input", side_effect=["y", "2"])
    def test_delete_completed_task(self, mock_input, task_with_data, capsys):
        task_with_data.delete_task()
        output = capsys.readouterr().out
        assert "Clean house task is deleted." in output
        assert len(task_with_data._tasks) == 1

    @patch("builtins.input", side_effect=["y", "1"])
    def test_delete_incomplete_task(self, mock_input, task_with_data, capsys):
        task_with_data.delete_task()
        output = capsys.readouterr().out
        assert "Buy groceries task is not completed." in output
        assert len(task_with_data._tasks) == 2

    @patch("builtins.input", return_value="n")
    def test_delete_task_cancel(self, mock_input, task_with_data):
        task_with_data.delete_task()
        assert len(task_with_data._tasks) == 2


class TestSaveTask:
    @patch("builtins.input", return_value="Save me")
    def test_save_task(self, mock_input, task, temp_dir):
        task.add_task()
        task.save_task()
        with open("tasks.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["title"] == "Save me"


class TestShowOptions:
    def test_show_options(self, capsys):
        show_options()
        output = capsys.readouterr().out
        assert "1. Add Task" in output
        assert "5. Exit" in output


class TestOptions:
    def test_options_list(self):
        assert OPTIONS == ["1", "2", "3", "4", "5"]
