import asyncio
from functools import wraps

def cls_sync_async(f):
    "Decorator to make a class method that makes api calls synchronous or asynchronous."
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        # only works on classes what have an api attribute
        # the api attribute will have a boolean for async or not
        if self.api.asynchronous:
            return f(self, *args, **kwargs)
        else:
            # Get pythons current execution thread and use that
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(f(self, *args, **kwargs))
    return wrapper