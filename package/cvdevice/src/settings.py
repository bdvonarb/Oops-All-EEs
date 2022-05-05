import gevent
from gevent.queue import Queue

frameQueue = Queue(2)

testQueue = Queue()

PD_MAC = 'B8:27:EB:C2:8A:73'

testImage = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAIBAQEBAQIBAQECAgICAgQDAgICAgUEBAMEBgUGBgYFBgYGBwkIBgcJBwYGCAsICQoKCgoKBggLDAsKDAkKCgr/2wBDAQICAgICAgUDAwUKBwYHCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgr/wAARCAAYABkDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD8X/2Y/BX2Lw54g/aq0Gy8P+J9X+CniDw34l1L4b+LNA+2aVrWhNqItrm5vS0say20eoS6NZS2S5luE1hnXbHbTMPb/wBsn4KeFfAP7HOseBfh5qGoL4U+Gfxw0rxJ4Ik1qVJ9R1TQPiN4RtdX0pL4xJHHb31lY+GLZLkRCSKW41GURsqWyvcH/BNHWfh78avjL8MPhLpPhPT9K8d2un6r4Au9N0ySw06T4i+GvEQ1Gx1JLe7vZYLeHxTb2utXi2Ul7MLS7jgsrf8AdzWUVvqvqHwO/aF/Y2+Inw6+I/7K2qfCTxB8TfEGlfswSeHr74laF4zfQdR8e23h7xDYeJXWwa+0+4SwtrLSbG8jSbUoZ7i607w1pVvbw6VK7WLgHwB4A+Fvjv4n/wBtyeCtC+1QeG/D9zrev3s11Fb22nWEG0NNNNMyRx75ZIbeJSwae4ube3iEk08Ub8/X1f8AFvwJ8M/2a/8Agno2rfA745af4+tPjx8UJdPbX9O0O90fUdD0jw5Z2t7JoepRXEeJZbu48Q6VdXFtbTXFjDcaBaNHc3zbJLb5QoAK+7/+Ccnizwr+21+2F4Y0Dx14m0/QfjJ460/WfAOs+KNWvUgtfGdr4k0i88Py6xM0hVG8QWSak140bPGuurbFDLDqjebq5RQB4B+2l4s8K6FP4R/ZI+HPibT9a0T4M6fqOial4m8O3qPpHi3X5tUurjUNdtBESksTo1np8N4xMt3Y6Np8riAFLS28PoooA//Z"
#testImage = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAIBAQEBAQIBAQECAgICAgQDAgICAgUEBAMEBgUGBgYFBgYGBwkIBgcJBwYGCAsICQoKCgoKBggLDAsKDAkKCgr/2wBDAQICAgICAgUDAwUKBwYHCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgr/wAARCAAYABkDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD8fv8Ak/8A/wCzgP8A1av/AOEn/p6/7Cv/ACGvAKK9/wD+T/8A/s4D/wBWr/8AhJ/6ev8AsK/8hoA8AooooAKKKKAPf/8Ak/8A/wCzgP8A1av/AOEn/p6/7Cv/ACGvAKKKAP/Z"

cvStatus = 'Off'
btStatus = 'Not Connected'

currentFrameTime = 0
previousFrameTime = 1

FGColor = (255,255,255)
BGColor = (0,0,0)

def newFrameTime(time):
    global previousFrameTime
    global currentFrameTime
    previousFrameTime = currentFrameTime
    currentFrameTime = time
    