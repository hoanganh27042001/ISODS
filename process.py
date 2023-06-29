import os

import cv2
import random

import numpy as np
from skimage.util import random_noise


def process_frame(frame, frame_count, output_dir):
    # Convert frame to grayscale
    grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Flip frame horizontally
    flipped_frame = cv2.flip(grayscale_frame, 1)

    # Rotate frame by a random degree (between -30 and 30)
    angle = random.randint(-30, 30)
    rows, cols = flipped_frame.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    rotated_frame = cv2.warpAffine(flipped_frame, rotation_matrix, (cols, rows))

    # Add random noise to the frame
    noise = np.random.normal(0, 10, rotated_frame.shape).astype(np.uint8)
    noisy_frame = cv2.add(rotated_frame, noise)

    # Save the frame as a JPG file.
    filename = os.path.join(output_dir,f'frame_{frame_count:04d}.jpg')
    cv2.imwrite(filename, noisy_frame)

if __name__ == "__main__":
    output_dir = 'processed_frames'
    os.makedirs(output_dir, exist_ok=True)
    # Load the input clip.
    cap = cv2.VideoCapture("Intersection.mp4")
    frame_count = 0

    # Process each frame in the clip.
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        process_frame(frame, frame_count, output_dir)
        frame_count += 1

    print('Finish ', frame_count)
    # Release the video object and close the output directory
    cap.release()
    cv2.destroyAllWindows()
