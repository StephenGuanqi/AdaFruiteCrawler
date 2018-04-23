from queue import Queue
from threading import Thread
from Parser import get_categories_list, get_all_item_tags, parse_item_tag


class SchedulerThread(Thread):
    """
    Scheduler thread that is responsible for consume the html tag data from the data queue and parse to product item
    cache the products info, check the product status and
    produce Data Insertion or Updation task in the worker queue
    """

    def __init__(self, data_queue, worker_queue):
        Thread.__init__(self)
        self.data_queue = data_queue
        self.worker_queue = worker_queue
        self.cache = {}
        self.insert_count = 0
        self.update_count = 0

    def run(self):
        while True:
            element = self.data_queue.get(block=True)
            if not element:
                break
            category, item_tag = element[0], element[1]
            item = parse_item_tag(item_tag, category)

            # item status is "IN STOCK"
            if not item:
                self.data_queue.task_done()
                continue

            # item exist in the database and no update needed
            id = item['ID']
            if id in self.cache and self.cache[id]['Availability'] == item['Availability'] \
                    and self.cache[id]['Amount'] == item['Amount']:
                # print('cache hit')
                self.data_queue.task_done()
                continue

            # insert task on the worker thread
            if id not in self.cache:
                c = {'Availability': item['Availability'],
                     'Amount': item['Amount']
                     }
                self.cache[id] = c
                self.worker_queue.put(('insert', item), block=True)
                self.insert_count += 1
            else:
                self.cache[id]['Availability'] = item['Availability']
                self.cache[id]['Amount'] = item['Amount']
                self.worker_queue.put(('update', item), block=True)
                print('*****************************************cache update')
                self.update_count += 1

            self.data_queue.task_done()

    def count_reset(self):
        self.insert_count = 0
        self.update_count = 0

    def get_count_info(self):
        return self.insert_count, self.update_count