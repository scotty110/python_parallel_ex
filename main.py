from multiprocessing import Lock, Process, Queue, cpu_count

'''
Example for Multiprocessing data
'''

def process_data(data):
    return data*2


def dump_queue(q:Queue):
    q.put(None)
    return list(iter(q.get, None))


def worker(data_queue:Queue, return_queue:Queue, exit_queue:Queue):
    data = data_queue.get()
    while data != None:
        #Process Data
        #v = process_data(data)
        #return_queue.put(v)
        return_queue.put( process_data(data) )
        data = data_queue.get()

    exit_queue.put('exit')
    return


def runner():
    n_workers = cpu_count() # Overload the memory (when *2 get errors????, maybe this is due to big little arch???)

    data_queue = Queue()
    return_queue = Queue()
    exit_queue = Queue()

    # Read Data
    data = [ i for i in range(n_workers*100) ]
    for i in data:
        data_queue.put(i)
    
    processes = []
    for i in range(n_workers):
        p = Process(target=worker, args=(data_queue, return_queue, exit_queue))
        data_queue.put(None)
        processes.append(p)
        p.start()

    # Run while processing
    exit_count = 0
    while True:
        try:
            e_value = exit_queue.get()
            if e_value == 'exit':
                exit_count += 1
        except:
            pass
        if exit_count == n_workers:
            break

    for p in processes:
        #p.terminate()
        p.join()

    results = dump_queue( return_queue )
    results.sort()
    print(f'Data Len {len(data)} Results len {len(results)}')
    print('Done')
    return


if __name__ == '__main__':
    runner()
