# Measuring size of object using rectangle marker
This method implement for Object detection and measuring on multi perspective using rectangle marker for defining default size

  ![git_pic2](https://user-images.githubusercontent.com/39212833/43760808-60e8da46-9a4d-11e8-9401-a72eb44a5d57.jpg)
  ![git_pic](https://user-images.githubusercontent.com/39212833/43752821-eaf16fa8-9a2c-11e8-9c6e-c0dbe5aa0096.jpg)
  
## Dependencies
Python3, numpy, opencv 3.

**Algorithms:**
  1. Convert to grayscale and blur to smooth.
  2. Find the contours in the edged image, keeping only the largest ones, and initialize the screen contour.
  3. Get approximate contour of marker.
  4. Get Perspective Transformation of marker.
  5. Find the contours in output result of Perspective Transformation.
  6. Extract every information of contours object.


