import eventlet

def period_task(period=5):
    def decorator(func):
        def _do_task(*args, **kw):
            while True:
                eventlet.sleep(period)
                func(*args, **kw)
        def _period_task(*args, **kw):
            eventlet.spawn_n(_do_task, *args, **kw)
        return _period_task
    return decorator

def delay_run(delay=5):
    def decorator(func):
        def _do_task(*args, **kw):
            eventlet.sleep(delay)
            func(*args, **kw)
        def _delay_run(*args, **kw):
            eventlet.spawn_n(_do_task, *args, **kw)
        return _delay_run
    return decorator
