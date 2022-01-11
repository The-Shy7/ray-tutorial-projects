import ray


class TaskInput:
    def __init__(self, value=None):
        self.value = value


class Task:
    def __init__(self, task_input=None):
        self.task_input = task_input

    def run(self):
        return self.task_input.value**2


class Pipeline:
    def __init__(self, tasks=[]):
        self.tasks = tasks

    def run(self, initial):
        result = initial
        for task in self.tasks:
            task.task_input.value = result
            result = task.run()
        return result

    def remote_run(self, initial):
        ray.init("anyscale://raj-test")
        result = initial
        for task in self.tasks:
            task.task_input.value = result
            result = task.run()
        return result




def main():
    # p = Pipeline(tasks=[Task(TaskInput()), Task(TaskInput())])
    # result = p.run(2)
    p = ray.remote(Pipeline).remote(tasks=[Task(TaskInput()), Task(TaskInput())])
    result = p.remote_run.remote(2)
    print(ray.get(result))

if __name__ == "__main__":
    main()