# How to use my Ishihara-color-plate-generator

Just go ahead and change some of the settings, you will figure it out.🙂

Maybe my comments will help you, but they probably wont.

Pygame is the only library you will need to install, datetime and time can be commented out.

Also i have a more User-"friendly" Website: https://imagetocircle.pythonanywhere.com/

# What are the Differences in the versions?
Version 1: when drawing a new Circle, the Distance to every other Circle on the Canvas is measured, the maximum radius will then be adjusted
Version 3: Comparing with every draw Circle is suuuuper inefficient, that's why I have split the Canvas in a "D Array of List which contain all the Circles drawn on this Field. This means the Algorithm can look around in a close Neighborhood of near Circles, making the whole Process faster (from 10 seconds to 2 seconds).
