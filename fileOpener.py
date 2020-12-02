import contextlib
import json
from time import strftime
import datetime


@contextlib.contextmanager
def open_resume(filepath, update_when='after'):

    STATE_FILENAME = '{}~state.json'.format(filepath)
    LOG_FILENAME = '{}~{}.log'.format(filepath,  strftime("%Y-%m-%dZ%H-%M-%S"))

    state = {
        "i": 0,
    }

    # If a state file does not exists create a empty one
    # If one already exist open it with read/update without truncate
    try:
        with open(STATE_FILENAME, 'x'):
            pass
    except FileExistsError:
        pass
    fileState = open(STATE_FILENAME, 'r+')
    try:
        state = json.loads(fileState.read())
    except:
        pass

    def update():
        fileState.seek(0)
        fileState.write(json.dumps(state))
        fileState.truncate()
        fileState.flush()  # ensure the file is always flushed to disk in case of a process crash

    file_log = open(LOG_FILENAME, 'a+')

    # open file the actual file
    file = open(filepath)
    update()

    try:
        def wrapped_file_gen():
            nonlocal state

            log('* STARTED!', 'state:', json.dumps(state), file=file_log)
            curr = 0
            for line in file:
                curr += 1
                if curr > state["i"]:
                    state["i"] = curr

                    if update_when == 'before':
                        update()
                        log('LINE:', curr, 'TEXT:',
                            line.rstrip('\n'), file=file_log)

                    # dispatch the "next() callback"
                    yield {'text': line, 'index': curr}

                    if update_when == 'after':
                        update()
                        log('LINE:', curr, 'TEXT:',
                            line.rstrip('\n'), file=file_log)

            state['done'] = True
            update()

        yield wrapped_file_gen()
    except BaseException as ex:
        log('* EXCEPTION!', 'state:', json.dumps(state),
            'Exception:', ex, file=file_log)
        raise

    finally:
        log('* ENDED!', 'state:', json.dumps(state), file=file_log)
        fileState.close()
        file_log.close()
        file.close()


def log(*args, file=None, **kwargs):
    timestamp = '[{}]'.format(datetime.datetime.utcnow().isoformat())
    print(timestamp, "\t".join(map(str, args)), **kwargs, file=file)
    file.flush()  # ensure the file is always flushed to disk in case of a process crash
