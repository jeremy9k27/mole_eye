# mole_eye

Real-Time No-Cost Baseball Pitch Classifier


Examples below.
A green ping pong ball was used in the examples so that it could safely be thrown indoors.

Fastball:

https://github.com/jeremy9k27/mole_eye/assets/118779230/efcd5f73-02e2-4b61-af31-e4280a34cb5a


Curveball:

https://github.com/jeremy9k27/mole_eye/assets/118779230/3cbc3c86-eb40-4060-b2fe-a48529985c5c

Mole-Eye is inspired by Hawk-Eye, the company that the MLB works with for all computer vision and tracking data work. This includes their pitch classifier, in which they use 12 high speed cameras to observe the balls movement, velocity, spin rate, and spin axis. 

The breakdown of the algorithm (full code can be found in main_code branch) is as follows:
 
Ball Detection:
While Mole-Eye runs, the iPhone camera continuously sends image frames to the computer. In each of these frames, the ball is detected based on its color. Because the green ping pong ball used for development is small, moving, and getting even smaller as it moves away from the camera, the iPhone camera (which of course also isn't high quality) doesn't see the exact shade of green the whole time. Therefore, a range of green must be used, and all pixels that are a shade in that range are picked up on as the ball. A wider range of green increases the signal captured, meaning that more of the ball will be detected for longer time. However, it also increases the chances that objects that are not the ball get picked up by the algorithm. This signal and noise tradeoff poses the main challenge of this project. 

One of the biggest obstacles is that even a still video is noisy. That is, even with a still camera and nothing moving in the frame, the HSV color of a singular pixel varies quite widely from one from to the next. This means that pixels of objects that are only vaguely green still sometimes register as being in the ball's color range. With there being so many pixels in each frame and so many frames per second, there is overall a lot of pixels that get picked up as the ball even though they are not. These pixels are referred to as hallucinations. Even with the minimum color range that can see the ball until it hits the backstop, there is usually at least a few hallucination pixels in each frame. We must accept that it's impossible to stop the algorithm from seeing these hallucinations, so they be dealt with mathematically.

Centroid Calculation and Recomputation

Pitch Identification

Smoothing and Classifying Pitch Types

- next steps. ML Classiieer
