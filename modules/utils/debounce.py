import asyncio, flet

class Debounce:
    def __init__(self, delay, page: flet.Page):
        self.delay = delay / 1000
        self.page = page
        self._task = None

    def run(self, callback, *args, **kwargs):
        if self._task and not self._task.done():
            self._task.cancel()

        async def wrapper():
            await asyncio.sleep(self.delay)
            await callback(*args, **kwargs)
        
        self._task = self.page.run_task(wrapper)
        