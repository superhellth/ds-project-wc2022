import threading
import multiprocessing


class MultiThreading:
    def __init__(self):
        self.num_threads = None
        self.threads = None

    def worker(self, task, queue):
        """Function run by the worker threads."""
        while True:
            text = queue.get()
            if text is None:
                break
            task(text)
            queue.task_done()

    def start_threads(self, task, queue, num_threads):
        """Start threads."""
        print("Starting worker threads...")
        self.num_threads = num_threads if num_threads else multiprocessing.cpu_count()
        self.threads = []
        for i in range(self.num_threads):
            t = threading.Thread(target=lambda: self.worker(task, queue))
            t.start()
            self.threads.append(t)

    def stop_threads(self, queue):
        """Stop threads."""
        print("Stopping worker threads...")
        for i in range(len(self.threads)):
            queue.put(None)
        for t in self.threads:
            t.join()
        print("Done!")
