# GestureVolumControl

This application uses hand gestures to control the volume of our system.
Using Mediapipe's handtracker(pre-trained model) which was trained on ~30K real-world images with 21 3D coordinates, we take Z-value from image depth map, if it exists per corresponding coordinate. To better cover the possible hand poses and provide additional supervision on the nature of hand geometry, we also render a high-quality synthetic hand model over various backgrounds and map it to the corresponding 3D coordinates.

Image source for better visualization:[hand_landmarks]: https://user-images.githubusercontent.com/54777383/114330395-3fa84200-9b07-11eb-87c8-65a7aff5b37e.png

Using the above implementation of handtracking module which marks 21 point on the palm, i have used Thumb(4 point) and indec finger(1 point) in order to build my application.
- I calculated the distance between the tip of thumb and tip of index finger
- Based on the Maximum distance and min distacne, i scaled down distance between fingers and volume of computer by linearly interpolating those values(Numpy is OP).
- For audio control i used the pythons's pycaw, which made controlling the volume of my pc very efficient. 

Sources:
https://github.com/murtazahassan
https://google.github.io/mediapipe/solutions/hands.html
https://github.com/AndreMiras/pycaw

