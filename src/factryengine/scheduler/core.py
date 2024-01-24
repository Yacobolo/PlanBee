from ..models import Resource, Task
from .heuristic_solver.main import HeuristicSolver
from .scheduler_result import SchedulerResult
from .task_graph import TaskGraph


class Scheduler:
    def __init__(self, tasks: list[Task], resources: list[Resource]):
        self.tasks = tasks
        self.resources = resources
        self.task_dict = self.get_task_dict(tasks)
        self.task_graph = TaskGraph(self.task_dict)

    def schedule(self):
        # merge intervals for all resources
        for resource in self.resources:
            resource.merge_intervals()

        # schedule tasks
        task_order = self.task_graph.get_task_order()
        heuristic_solver = HeuristicSolver(self.task_dict, self.resources, task_order)
        result = heuristic_solver.solve()

        scheduler_result = SchedulerResult(result)
        print(scheduler_result.summary())
        return scheduler_result

    def get_task_dict(self, tasks: list[Task]):
        """
        returns the task dictionary with task id as key and task object as value
        """
        return {task.get_id(): task for task in tasks}
