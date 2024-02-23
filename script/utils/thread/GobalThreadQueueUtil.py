from script.utils.thread import MainThreadQueue
import threading
import inspect
import ctypes
# 定义一个函数作为子线程的入口点
queue = MainThreadQueue()


def my_thread_func():
    queue.start()


tmp_thread = threading.Thread(target=my_thread_func)
need_new_thread = False

def putTask(taskEntity):
    queue.putTask(taskEntity)


def queryTaskExist(taskName):
    return queue.queryTaskExist(taskName)


def stop():
    global tmp_thread,need_new_thread
    if queue.isRun:
        queue.stop()
        queue.mainQueue.clear()
        # 等待线程结束
        if tmp_thread.is_alive():
            stop_thread(tmp_thread)
        need_new_thread = True

def start():
    global tmp_thread,need_new_thread
    if not queue.isRun:
        if need_new_thread:
            tmp_thread = threading.Thread(target=my_thread_func)
        tmp_thread.start()



def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

