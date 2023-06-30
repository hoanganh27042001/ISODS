This repository contains a series of scripts used to perform Computer Vision task.

    .
    ├── process.py          # decompose the input clip into individual frames and perform image processing operations on each frame
    ├── detection.py        # Utilize a pre-trained object detection model YOLO-v3 to detect objects in the input clip 
    ├── scrape.py           # a tool to scrape and download images from www.freepik.com/ into 2 categories: true images and ai generated images

## Usage
To run this project: 
- first clone it to your computer.
- intall requirements: pip install -r requirements.txt

1. To perform image processing on each frame from the given input clip. The output images are stored in *processd_frames* folder.
```
python process.py 
``` 
2. To detect objects on every frame from the given input clip.
The detected information of objects (FrameID, Object’s class, Object’s bounding box, Confidence) into *detections.json* file.

*Note*: Make sure the configuration *yolo3.cfg*, *yolov3.weights* and *coco.names* are under the same directory.
```
python detections.py
```
3. To scrape and download images from [Freepik](https://www.freepik.com/).
- Scrape and download 1000 true car images. The downloaded images are saved in *real_images* folder.
```
python scrape.py -c real --keyword car --limit 1000
```
- Scrape and download 1000 true car images. The downloaded images are saved in *ai_images* folder.
```
python scrape.py -c ai --keyword car --limit 1000
```

*Note:* If keyword argument is skipped, then the tool will automatically download images corresponding to 80 class name in coco 
dataset. 

In this repository, the retrieved images under *real_images* and *ai_images* are images folder corresponding to 80 class 
name in coco dataset. Each sub folder has 20 images. Thus, there are 1600 real images and 1600 ai generated images scraped. 
