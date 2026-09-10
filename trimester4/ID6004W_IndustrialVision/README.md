# ID6004W Industrial Vision

Faculty: Prof Vinkle Srivastav

## Lecture 1: Intro

Interpret light as meaning:
* Geometric: shape, depth, pose, motion
* Semantic: objects, materials, actions

3 Rs : 
* Recognition (semantic)
* Reconstruction (2d projection -> back to 3d; ill-posed as it requires assumptions about 3d)
* Reorganization (eg. semantic segmentation)

4 fields are related to Computer Vision:
* Biological Vision
* Computer Graphics (maps 3d to 2d; in Computer Vision opposite, we map 2d projection to 3d meaning)
* Image Processing
* Machine Learning

Challenges due to which Computer Vision is an *ill-posed inverse problem*:
* Perspective Illusion: one view may not be enough to examine the scene
* View Point Variation: same object can look completely different from different views
* Illumination: eg. in a black & white pic, same object can look black or white depending on lighting
* Motion: world & camera are both in motion
* Perception compared with measurement: we can perceive surfaces, edges even when image doesn't have one explicitly!
* Local ambiguities: small image patch cannot be interpreted taken out of context
* Variation within a class: eg. a "chair" can have many many types of images

Perspectograph : seeing an object behind a sheet of glass