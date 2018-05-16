# coding=utf-8
import threading
import queue


class MyThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self):
        item = self._queue.get_nowait()
        print("%d ,I am thread %s" % (item, self.getName()))


def main():
    q=queue.Queue()
    for i in range(10):
        q.put(i)

    threads=[]
    threads_count=6

    for i in range(threads_count):
        threads.append(MyThread(q))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
