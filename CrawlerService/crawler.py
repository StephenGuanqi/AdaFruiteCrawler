from pymongo import MongoClient
import pymongo
from Parser import get_categories_list, get_all_item_tags, parse_item_tag
import json
from queue import Queue
from threading import Thread
from ProducerThread import ProducerThread
from WorkerThread import WorkerThread
from SchedulerThread import SchedulerThread
import time

if __name__ == '__main__':
    # built in connection pool support with thread-safe operations
    # user name and password should use env var instead
    client = MongoClient("mongodb://guanqiy:2415@ds149567.mlab.com:49567/adafruite", maxPoolSize=50)

    num_producer_thread = 32
    num_worker_thread = 32

    max_category_size = 35
    max_item_size = 5000
    max_task_size = 2000

    categories, urls = get_categories_list()
    # create url Buffer queue to hold all urls from the main category page
    url_queue = Queue(max_category_size)

    # create item buffer queue to hold all html item tag to be parsed
    data_queue = Queue(max_item_size)

    # create task buffer queue to hold all parsed item ro be transmitted to database
    worker_queue = Queue(max_task_size)

    producer_threads = []
    for i in range(num_producer_thread):
        producer = ProducerThread(url_queue, data_queue)
        producer.start()
        producer_threads.append(producer)

    scheduler = SchedulerThread(data_queue, worker_queue)
    scheduler.start()

    worker_threads = []
    for i in range(num_worker_thread):
        worker = WorkerThread(worker_queue, client)
        worker.start()
        worker_threads.append(worker)

    count = 0
    while True:
        ts = time.time()
        # crawler begin
        for category, url in zip(categories, urls):
            url_queue.put((category, url), block=True)

        # block until finish one round of all url parsing
        url_queue.join()
        data_queue.join()
        worker_queue.join()

        print('finish {} round of crawling. '.format(count))
        count += 1
        insert_count, update_cpount = scheduler.get_count_info()
        print('{} new data insert, {} data update'.format(insert_count, update_cpount))
        scheduler.count_reset()

        print('Took {}s to parse this round'.format(time.time() - ts))  # 7.5 s

        if count == 1:
            db = client.adafruite
            db.products.create_index([
                ("Availability", pymongo.TEXT),
                ('Amount', pymongo.ASCENDING)
            ]
            )

        # !!!!!! have to wait for a while until next parsing
        # other wise http request frequency will exceed the website's threshold
        time.sleep(3)

    # stop loop and join threads
    for i in range(num_producer_thread):
        url_queue.put(None)
    data_queue.put(None)
    for i in range(num_worker_thread):
        worker_queue.put(None)

    for t in producer_threads:
        t.join()
    scheduler.join()
    for t in worker_threads:
        t.join()
