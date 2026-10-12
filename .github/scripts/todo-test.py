import unittest
from todo import Task, TaskPool
from io import StringIO
import sys


class TestTaskPool(unittest.TestCase):

    # Runs before each test: creates a fresh TaskPool
    def setUp(self):
        self.pool = TaskPool()

    # Tests add_task(): adding one task gives a pool of size 1
    def test_add_task(self):
        task = Task("New Task")
        self.pool.add_task(task)
        self.assertEqual(len(self.pool.tasks), 1)

    # Tests get_open_tasks(): populate() creates 3 "ToDo" tasks
    def test_get_open_tasks(self):
        self.pool.populate()
        open_tasks = self.pool.get_open_tasks()
        self.assertEqual(len(open_tasks), 3)
        self.assertTrue(all(task.status == "ToDo" for task in open_tasks))

    # Tests get_done_tasks(): populate() creates 3 "Done" tasks
    def test_get_done_tasks(self):
        self.pool.populate()
        done_tasks = self.pool.get_done_tasks()
        self.assertEqual(len(done_tasks), 3)
        self.assertTrue(all(task.status == "Done" for task in done_tasks))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTaskPool)

    captured_output = StringIO()

    # Run tests with verbosity 2 (detailed)
    result = unittest.TextTestRunner(stream=captured_output, verbosity=2).run(suite)

    # Capture the relevant output (test names and "ok")
    output_lines = captured_output.getvalue().splitlines()

    # Print the output of each test with the status "ok"
    for line in output_lines:
        if "ok" in line:
            # Keep only the test name from the line
            print(line.split(' ')[0] + ' ... ok')

    # Print total, passed, and failed summary
    total_tests = result.testsRun
    failed_tests = [t[0] for t in result.failures + result.errors]
    passed_tests = [test for test in suite if test not in failed_tests]

    print(f"Total Tests: {total_tests}")
    print(f"Passed: {len(passed_tests)} ({(len(passed_tests) / total_tests) * 100:.2f}%)")
    print(f"Failed: {len(failed_tests)} ({(len(failed_tests) / total_tests) * 100:.2f}%)")

    # Exit non-zero if any test failed, so the pipeline shows the failure
    sys.exit(0 if result.wasSuccessful() else 1)
