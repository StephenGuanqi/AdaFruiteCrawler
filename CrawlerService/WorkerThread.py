from queue import Queue
from threading import Thread


class WorkerThread(Thread):
    """
    Consumer thread that is in charge of database access on data insertion and data update
    """
    def __init__(self, queue, client):
        Thread.__init__(self)
        self.queue = queue
        self.db = client.adafruite  # driver

    def run(self):
        while True:
            element = self.queue.get(block=True)
            if not element:
                break
            operation, item = element[0], element[1]
            if operation == 'insert':
                item['_id'] = item['ID']  # mongo document ID
                result = self.db.products.insert_one(item)
                if not result.acknowledged:
                    print("Insert ID {} failed".format(item['ID']))
                print("ITEM {} from {} inserted.".format(item['name'], item['category']))
            elif operation == 'update':
                print('ITEM UPDATE! {} to {}, {}'.format(item['name'], item['Availability'], item['Amount']))
                result = self.db.products.update_one(
                    {"_id": item['ID']},
                    {
                        "$set": {
                            "Availability": item["Availability"],
                            "Amount": item["Amount"]
                        }
                    }
                )
                if result.matched_count != 1:
                    print("Error! {} item updated".format(result.matched_count))
            self.queue.task_done()