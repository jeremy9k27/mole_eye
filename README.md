# mole_eye

Real-Time No-Cost Baseball Pitch Classifier


Examples below.
A green ping pong ball was used in the examples so that it could safely be thrown indoors.

Fastball:

https://github.com/jeremy9k27/mole_eye/assets/118779230/efcd5f73-02e2-4b61-af31-e4280a34cb5a


Curveball:

https://github.com/jeremy9k27/mole_eye/assets/118779230/3cbc3c86-eb40-4060-b2fe-a48529985c5c


**Abstract**
Mole-Eye is inspired by Hawk-Eye, the company that the MLB works with for all computer vision and tracking data work. This includes their pitch classifier, in which they use 12 high speed cameras to observe the balls movement, velocity, spin rate, and spin axis. Mole_Eye is a python code that uses the CV2 library. The computer continuously recieves frames from the iPhone camera and runs algorithms as it recieves the frames.



The detailed breakdown of the algorithm (full code can be found in main_code branch) is as follows:
 

***Ball Detection:***
While Mole-Eye runs, the iPhone camera continuously sends image frames to the computer. In each of these frames, the ball is detected based on its color. Because the green ping pong ball used for development is small, moving, and getting even smaller as it moves away from the camera, the iPhone camera (which of course also isn't high quality) doesn't see the exact shade of green the whole time. Therefore, a range of green must be used, and all pixels that are a shade in that range are picked up on as the ball. A wider range of green increases the signal captured, meaning that more of the ball will be detected for longer time. However, it also increases the chances that objects that are not the ball get picked up by the algorithm. This signal and noise tradeoff poses the main challenge of this project. 

One of the biggest obstacles is that even a still video is noisy. That is, even with a still camera and nothing moving in the frame, the HSV color of a singular pixel varies quite widely from one from to the next. This means that pixels of objects that are only vaguely green still sometimes register as being in the ball's color range. With there being so many pixels in each frame and so many frames per second, there is overall a lot of pixels that get picked up as the ball even though they are not. These pixels are referred to as hallucinations. Even with the minimum color range that can see the ball until it hits the backstop, there is usually at least a few hallucination pixels in each frame. We accept that it's impossible to stop the algorithm from seeing these hallucinations, so they must be dealt with mathematically.

***Centroid Calculation and Recalculation***
We seek to represent the ball as a single coordinate in each frame. This is done by finding the weighted centroid of the x coordinates and y coordinates of all the pixels that are within the green range, with the weights being the amount of "greeness" of each pixel. In many of the frames, these pixels include hallucinations that make the resulting Cx and Cy inaccurate. Fortunately, there are more almost always more signal pixels than hallucination pixels, which means innaccurate centroids are still close to the actual ball, allowing us to easily remove the hallucinations. We utilize CV2's circle function for this: we create a circle of radius 10 pixels around the centroid, and any points not inside the circle are removed from the set of pixels inside the green range. This removes almost all hallucinations. If there are still hallucination pixels inside the circle, those hallucinations aren't throwing off the centroid significantly, so it's fine to ignore them. With our new set of pixels with hallucinations removed, we compute the new Cx and Cy.

***Pitch Identification***
As the program is continuously running and recieving frames, it needs to be able to know that a pitch is being thrown without user input. We make use of the hallucinations to accomplish this. When no pitch is in frame, the centroid is entirely determined by the hallucinations. Due to their random nature, this means the centroid jumps widely from frame to frame. However, when the ball is in frame, the centroid follows the ball and does not move widely from one frame to the next. This stability is our trigger that a pitch is being thrown. To implement this in code, we make an array of each centroids' coordiantes, with a new Cx and Cy appended each frame. Once the frame has three centroids, we set a pitch_started condition based on how big the jumps between centroids are. If the jumps are big, then no pitch is being thrown, and when the new Cx and Cy are added, the first Cx and Cy in the array are deleted, keeping it at size three. However, if the jumps are small and a pitch is being thrown, then the first Cx and Cy are not deleted. The array keeps appending new centroids without deleting any of the initial centroids until the jumps become significantly large again (meaning the pithc ended and the ball is not in frame anymore. 

When the pitch is over, our centroid array - containing the coordinates of the ball's centroid in each frame - is moved along into the next part of the algorithm. However, we observe through testing that sometimes the algorithm thinks a pitch has started even when the ball isn't in frame. This is again due to the randomness of the hallucinations, as sometimes through chance, three hallucinations in a row happen to be near each other. We implement two new methods to prevent this. We first improve the pre-pitch processes by making the pitch_started condition more strict by observing that the pitch will always start in the same rough location. In the camera setup from the example, the pitch always starts in the top right quadrant. Thus, we add to the condition that all three points are in that quadrant. We can also improve post-pitch processing by setting a minimum length of the centroid array. If the array has length less than say 10, then it wasn't actually a pitch, and the algorithm goes back to looking for a pitch.

***Dislaying and Classifying Pitch Types***

With the centroid coordinates we are now ready for the exciting outputs of the algorithm: displaying the pitch and classifying it. If we were to display the centroid coordinates as is, we would observe that the path of the ball is rather jagged. Knowing that the actual flight of the ball is smooth (and that our centroid coordinates contain both signal and noise), we apply a simple smoothing algorithm to the coordinates - replacing each coordinate with the average of itself and its neighboring coordinates. The new processed centroid array is then displayed using cv2.imshow to overlay it over the frame. 

We also used the processed centroid array to classify the pitch. Through observation, the last parts of the pitch is what is most informative about the pitch type. Because we can only see movement and not velocity our spin, we will have use four pitch types to choose from based on the slope of the last part of each pitch. Fastballs have minimal movement, curveballs move down, sweeper sliders move glove side, and sinkers move arm side. The exact slope thresholds for each pitch are bit tricky due to the way we are using 2d coodinates to represent a 3d situation. Still, the model seems to classify the pitches accurately, although a larger dataset is needed for more rigourous testing.

***Future Developments***
Another benefit of a larger dataset is it opens the possibility of more advanced classificaiton techniques. One promsiing possibility is k-means clusters. A bigger modification (but one that slightly goes against the low-scale nature of the project) is to use two cameras. Two cameras would allow us to represent each centroid not just as Cx and Cy, but also with Cz, giving us a dimension of depth that we currently do not have. This would also open a new realm of possibilities because velocity could also be measured. (For example, a pitch moving downward could be split into curveballs and gyro sliders.)



Note to author - what's causing the decaying accuracy? (like the fixating after a few pitches). is it the number of pitches? or time elapsed?
