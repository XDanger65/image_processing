import threading
import queue
import cv2  # OpenCV for image processing
from PIL import Image
import numpy as np

class WorkerThread(threading.Thread):
    def _init_(self, task_queue):
        threading.Thread._init_(self)
        self.task_queue = task_queue
        self.processed_images = []  # Initialize processed_images list

    def run(self):
        while True:
            task = self.task_queue.get()
            if task is None:
                break
            images, operation = task
            results = [self.process_image(image, operation) for image in images]
            self.processed_images.extend(results)  # Extend processed_images list

    def process_image(self, image, operation):
        img = cv2.imread(image)
        if operation == 'edge_detection':
            result = cv2.Canny(img, 100, 200)
        elif operation == 'color_inversion':
            result = cv2.bitwise_not(img)
        return result

def select_images():
    print("Enter the paths of the images separated by commas:")
    file_paths_input = input()
    file_paths = file_paths_input.split(',')
    return file_paths

def process_images(images, operation):
    task_queue.put((images, operation))
    start_worker_threads(len(images))

def start_worker_threads(num_threads):
    global worker_threads
    worker_threads = [WorkerThread(task_queue) for _ in range(num_threads)]
    for thread in worker_threads:
        thread.start()

def display_image(image):
    image = Image.fromarray(image)
    image.show()

def save_image(image, file_path):
    cv2.imwrite(file_path, image)
    print("Image saved successfully.")

task_queue = queue.Queue()
worker_threads = []

print("Welcome to Image Processing Terminal App!")
print("Available operations: edge_detection, color_inversion")

while True:
    print("\nSelect operation:")
    operation = input().strip()
    if operation not in ['edge_detection', 'color_inversion']:
        print("Invalid operation. Please choose again.")
        continue

    print("\nSelect images:")
    images = select_images()
    
    if not images:
        print("No images selected. Exiting...")
        break
    
    process_images(images, operation)

    for thread in worker_threads:
        thread.join()

    print("\nProcessing completed!")
    
    for image in task_queue.queue[0].processed_images:
        display_image(image)

    print("\nDo you want to save the processed images? (yes/no)")
    save_option = input().strip().lower()
    if save_option == 'yes':
        for idx, image in enumerate(task_queue.queue[0].processed_images):
            save_image(image, f"processed_image_{idx + 1}.png")

    print("\nDo you want to perform another operation? (yes/no)")
    continue_option = input().strip().lower()
    if continue_option != 'yes':
        break

print("Thank you for using the Image Processing Terminal App!")