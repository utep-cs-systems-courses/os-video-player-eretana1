#!/usr/bin/env python3

import cv2
import threading

from TQueue import TQueue

# globals
outputDir = 'frames'
clipFileName = 'clip.mp4'
frameDelay = 42  # the answer to everything


# Consumer (Displays image )
def display_frames(consumer: TQueue):
    # initialize frame count
    count = 0

    while True:
        # load the frame
        frame = consumer.dequeue()

        # We have reached end of video
        if frame == 'END':
            break

        print(f'Displaying frame {count}\n')
        # Display the frame in a window called "Video"
        cv2.imshow('Video', frame)

        # Wait for 42 ms and check if the user wants to quit
        if cv2.waitKey(frameDelay) and 0xFF == ord("q"):
            break

            # get the next frame filename
        count += 1

    # make sure we cleanup the windows, otherwise we might end up with a mess
    print('-----------Video has Terminated--------------')
    cv2.destroyAllWindows()


def convert_to_grayscale(producer: TQueue, consumer: TQueue):
    # initialize frame count
    count = 0

    while True:
        # Load color frame
        inputFrame = producer.dequeue()

        # Converter has finished sending grayscale images to queue
        if inputFrame == 'END':
            break
        print(f'Converting frame {count}\n')

        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)

        # Enqueue the image to gray scale for consumer to display
        consumer.enqueue(grayscaleFrame)

        count += 1

    # When gray scale is done, enqueue END
    consumer.enqueue('END')


# Producer thread (extracts frames and places them into queue)
def extract_frames(producer: TQueue):
    global clipFileName

    # initialize frame count
    count = 0

    # open the video clip
    vidcap = cv2.VideoCapture(clipFileName)

    # read one frame
    success, image = vidcap.read()

    print(f'Reading frame {count} {success}\n')
    while success:
        # Add frame to queue to send to grayscale thread
        producer.enqueue(image)

        success, image = vidcap.read()
        print(f'Reading frame {count}')
        count += 1

    # Determine whether you are at the end of the file
    producer.enqueue('END')


producer_q = TQueue()  # Producer sends to Queue, grayscale dequeues
consumer_q = TQueue()  # grayscale sends to queue, consumer dequeues

# Create threads that will extract frames, convert the frames, and display the frame
producer_thread = threading.Thread(target=extract_frames, args=(producer_q,))
grayscale_thread = threading.Thread(target=convert_to_grayscale, args=(producer_q, consumer_q))
consumer_thread = threading.Thread(target=display_frames, args=(consumer_q,))

# Start executing all threads
producer_thread.start()
grayscale_thread.start()
consumer_thread.start()
