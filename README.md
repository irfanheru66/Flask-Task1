# Flask-Task1

This program receive an concrete image 

![source](readmeAssets/source.png)

and will classify it with three diferent edge detections method.

<p float="left">
  <img src="readmeAssets/Sobel.png" width="400" />
  <img src="readmeAssets/prewitt.png" width="400" /> 
  <img src="readmeAssets/Canny.png" width="400" /> 
</p>

# Run this app via Docker
## `nodeflux_task1:1.0`

# Docker Pull
```
docker pull irfanheru66/nodeflux_task1:2.0
```
# Docker Run
```
docker run -p 5000:5000 irfanheru66/nodeflux_task1:2.0
```
on your local browser clik localhost:5000