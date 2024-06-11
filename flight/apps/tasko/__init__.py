from .loop import Loop

__global_event_loop = None


def get_loop(debug=False):
    """Returns the singleton event loop"""
    global __global_event_loop
    if __global_event_loop is None:
        __global_event_loop = Loop(debug=debug)
    return __global_event_loop


def enable_debug_logging():
    get_loop().enable_debug_logging()


add_task = get_loop().add_task
run_later = get_loop().run_later
schedule = get_loop().schedule
schedule_later = get_loop().schedule_later
sleep = get_loop().sleep
suspend = get_loop().suspend

run = get_loop().run
