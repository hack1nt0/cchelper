import asyncio
from threading import Thread, Event
from concurrent.futures import ThreadPoolExecutor, Future


__all__ = ["global_threadpool", "global_stopflag"]

global_threadpool = ThreadPoolExecutor(max_workers=2)
global_stopflag = Event()
# global_asyncloop = asyncio.get_event_loop()
