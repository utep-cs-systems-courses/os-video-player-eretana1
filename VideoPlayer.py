#!/usr/bin/env python3

import cv2
import os

# globals
outputDir    = 'frames'
clipFileName = 'clip.mp4'
frameDelay   = 42       # the answer to everything


def display_frames:
    # initialize frame count
    count = 0

    # Generate the filename for the first frame 
    frameFileName = f'{outputDir}/grayscale_{count:04d}.bmp'

    # load the frame
    frame = cv2.imread(frameFileName)

    while frame is not None:
    
        print(f'Displaying frame {count}')
        # Display the frame in a window called "Video"
        cv2.imshow('Video', frame)

        # Wait for 42 ms and check if the user wants to quit
        if cv2.waitKey(frameDelay) and 0xFF == ord("q"):
            break    
    
        # get the next frame filename
        count += 1
        frameFileName = f'{outputDir}/grayscale_{count:04d}.bmp'

        # Read the next frame file
        frame = cv2.imread(frameFileName)

    # make sure we cleanup the windows, otherwise we might end up with a mess
    cv2.destroyAllWindows()


def convert_to_grayscale():
    # initialize frame count
    count = 0

    # get the next frame file name
    inFileName = f'{outputDir}/frame_{count:04d}.bmp'


    # load the next file
    inputFrame = cv2.imread(inFileName, cv2.IMREAD_COLOR)

    while inputFrame is not None and count < 72:
        print(f'Converting frame {count}')

        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)
    
        # generate output file name
        outFileName = f'{outputDir}/grayscale_{count:04d}.bmp'

        # write output file
        cv2.imwrite(outFileName, grayscaleFrame)

        count += 1

        # generate input file name for the next frame
        inFileName = f'{outputDir}/frame_{count:04d}.bmp'
    
        # load the next frame
        inputFrame = cv2.imread(inFileName, cv2.IMREAD_COLOR)


def extract_frames():
    # initialize frame count
    count = 0

    # open the video clip
    vidcap = cv2.VideoCapture(clipFileName)
    
    # create the output directory if it doesn't exist
    if not os.path.exists(outputDir):
        print(f"Output directory {outputDir} didn't exist, creating")
        os.makedirs(outputDir)
        
    # read one frame
    success,image = vidcap.read()
        
    print(f'Reading frame {count} {success}')
    while success and count < 72:
        
        # write the current frame out as a jpeg image
        cv2.imwrite(f"{outputDir}/frame_{count:04d}.bmp", image)   
        
        success,image = vidcap.read()
        print(f'Reading frame {count}')
        count += 1
