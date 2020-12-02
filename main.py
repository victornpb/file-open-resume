import fileOpener
import time

filename = "test.txt"
with fileOpener.open_resume(filename) as f:
    for line in f:

        print("Processing line {}...\t{}".format(line['index'], line['text']))
        time.sleep(0.5)
