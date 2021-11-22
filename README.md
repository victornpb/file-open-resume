# file-open-resume


A substitute for `open()` that lets you resume from where you left off.

Very use full for consuming large files, or running a ETL script.


# Example

```py
import fileOpener
import time

filename = "test.txt"
with fileOpener.open_resume(filename) as f:
    for line in f:

        print("Processing line {}...\t{}".format(line['index'], line['text']))
        
        # Do something complicated with it
        time.sleep(0.5)
```

If your program crashes by a exception or you stop it by Killing or CTRL-C running it again will make sure it will resume from the failed line.
