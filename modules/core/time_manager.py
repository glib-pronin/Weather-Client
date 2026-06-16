import asyncio

class TimeManager:
    def __init__(self):
        self._timers = []

    def create_task(self, callback, interval):
        task = asyncio.create_task(
            self._timer_loop(callback, interval)
        )
        self._timers.append(task)

    async def _timer_loop(self, callback, interval):
        try:
            while True:
                await asyncio.sleep(interval)
                if asyncio.iscoroutinefunction(callback):
                    await callback()
                else:
                    callback()
        except asyncio.CancelledError:
            return
    
    def cancel_all(self):
        for task in self._timers:
            task.cancel()
        self._timers.clear()
        print('clear')