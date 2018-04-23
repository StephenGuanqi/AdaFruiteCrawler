from queue import Queue
from threading import Thread
from Parser import get_categories_list, get_all_item_tags, parse_item_tag


class ProducerThread(Thread):
    """
    Producer Thread that send http request and parse the response html file,
    generate item tags and insert to data_queue
    """

    def __init__(self, url_queue, data_queue):
        Thread.__init__(self)
        self.url_queue = url_queue
        self.data_queue = data_queue

    def run(self):
        while True:
            element = self.url_queue.get(block=True)
            if not element:
                break
            category, url = element[0], element[1]
            item_tags = get_all_item_tags(url)
            for tag in item_tags:
                self.data_queue.put((category, tag), block=True)
            self.url_queue.task_done()
