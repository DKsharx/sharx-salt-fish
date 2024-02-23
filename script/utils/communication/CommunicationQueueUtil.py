import queue

BASE_INFO_QUEUE = queue.Queue()


def send_base_info(info):
    global BASE_INFO_QUEUE
    BASE_INFO_QUEUE.put(info)


def get_base_info():
    global BASE_INFO_QUEUE
    try:
        info = BASE_INFO_QUEUE.get_nowait()
        if info:
            return info
        else:
            return None
    except queue.Empty:
        return None

