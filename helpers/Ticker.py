from threading import Thread, Event
from time import time


class Ticker(Thread):
    """
    Helper Class to use in Hardware and Tracking. A threading template.
    Runs method step in a loop at specified frequency using threading.
    """
    def __init__(self, freq):
        """
        :param freq: max frequency to run method step in loop
        """
        # threading variables
        self.max_wait = 1.0 / freq
        self.stop = Event()  # to know when to stop the thread
        self.stopped = Event()  # to know if thread has stopped

        super(Ticker, self).__init__()

    def set_freq(self, freq):
        self.max_wait = 1.0 / freq

    def start(self):
        """
        Start threaded loop
        """
        self.stop.clear()
        self.stopped.clear()
        super(Ticker, self).start()

    def step(self):
        """
        Overwrite with necessary function to loop in a thread
        """
        pass

    def run(self):
        """
        Runs threaded loop
        """
        while not self.stop.is_set():
            start = time()

            self.step()

            wait_time = self.max_wait - (time() - start)
            wait_time = max(0.0, wait_time)

            self.stop.wait(wait_time)
        self.stopped.set()

    def stop(self):
        """
        Stops threaded loop
        """
        self.stop.set()
        self.stopped.wait()
