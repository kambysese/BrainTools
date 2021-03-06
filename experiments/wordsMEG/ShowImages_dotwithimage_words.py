"""
==========================
Display images for MEG
==========================
"""
import numpy as np
from expyfun import visual, ExperimentController
from PIL import Image
import os
import glob

# background color
bgcolor = [127/255., 127/255., 127/255., 1]
# These should be inputs
#basedir = '/home/jyeatman/projects/MEG/images/'
basedir = os.path.join('/home', 'jyeatman', 'git', 'wmdevo', 'megtools', 'stim', 'readingD')
basedir = os.path.join('/home', 'jyeatman', 'git', 'wmdevo', 'megtools', 'stim','wordStim')
#imagedirs = ['faces_localizer', 'limb_localizer', 'objects_localizer', 'place_localizer']
imagedirs = ['stim001', 'stim007', 'stim008', 'stim009', 'stim014', 'stim015', 'stim016']
imagedirs = ['word_c254_p20', 'word_c254_p50', 'word_c254_p80','word_c133_p20','word_c137_p20','word_c141_p20','nonword_c254_p20', 'nonword_c254_p50','nonword_c133_p20','nonword_c137_p20','nonword_c141_p20']

nimages = 50  # number  'stim003',of images for each category
isis = np.arange(.25,.44,.02)  # ISIs to be used. Must divide evenly into nimages
isis = [.8]
imduration = .3
s = .7  # Image scale

# Create a vector of ISIs in a random order. One ISI for each image
ISI = np.repeat(isis, (nimages/len(isis))*len(imagedirs))
np.random.shuffle(ISI)

# Create a vector that will denote times to change the color of the fixation
# dot. This vector denotes the point within the ISI to change the dot color.
# I bounded this at .2 and .8 because I don't want dot changes occuring
# immediately before or after image presentation
dotchange = np.random.uniform(.2, .8, len(ISI))
# Creat a vector of dot colors for each ISI
c = ['r', 'g', 'b', 'y', 'c']
dcolor = np.tile(c, len(ISI)/len(c))
np.random.shuffle(dcolor)
# Create a vector denoting when to display each image
imorder = np.arange(nimages*len(imagedirs))
# Create a vector marking the category of each image
imtype = []
for i in range(1, len(imagedirs)+1):
    imtype.extend(np.tile(i, nimages))

# Shuffle the image order
rng = np.random.RandomState(0)  # note to make this random based on time input if no argument
ind_shuf = range(len(imtype))
rng.shuffle(ind_shuf)
imorder_shuf = []
imtype_shuf = []
for i in ind_shuf:
    imorder_shuf.append(imorder[i])
    imtype_shuf.append(imtype[i])

# Build the path structure to each image in each image directory. Each image
# category is an entry into the list
imagelist = []
for imname in imagedirs:
    # Temporary variable with image names in order
    tmp = sorted(glob.glob(os.path.join(basedir, imname, '*')))
    # Randomly grab nimages from the list
    n = rng.randint(0, len(tmp), nimages)
    tmp2 = []
    for i in n: tmp2.append(tmp[i])  # This line is slow... Python must have a faster way to index
    # Add the random image list to an entry in imagelist
    imagelist.extend(tmp2)
    assert len(imagelist[-1]) > 0

# Start instance of the experiment controller
#with ExperimentController('ReadingExperiment') as ec:
#with ExperimentController('ShowImages', full_screen=False, window_size=[800, 800]) as ec:
with ExperimentController('ShowImages', full_screen=True) as ec:
    fr = 1/ec.estimate_screen_fs()  # Estimate frame rate    
    adj = fr/2  # Adjustment factor for accurate flip
    # Wait to fill the screen
    ec.set_visible(False)
    # Set the background color to gray
    ec.set_background_color(bgcolor)

    # load up the image stack
    img = []
    for im in imagelist:
        #img_buffer = np.array(Image.open(os.path.join(imagedir,im)))/255.
        #img.append(visual.RawImage(ec, img_buffer, scale=1.))
        img_buffer = np.array(Image.open(im), np.uint8)
        if img_buffer.ndim == 2:
            img_buffer = np.tile(img_buffer[:, :, np.newaxis], [1, 1, 3])
        img.append(visual.RawImage(ec, img_buffer, scale=s))
        ec.check_force_quit()

    # make a blank image
    blank = visual.RawImage(ec, np.tile(bgcolor[0], np.multiply([s, s, 1],img_buffer.shape)))
    # Calculate stimulus size
    d_pix = -np.diff(ec._convert_units([[3., 0.], [3., 0.]], 'deg', 'pix'), axis=-1)

    # do the drawing, then flip
    ec.set_visible(True)
    frametimes = []
    buttons = []
    ec.listen_presses()
    last_flip = -1
    # Initiate a counter
    c = -1

    # Create a fixation dot
    fix = visual.FixationDot(ec, colors=('k', 'k'))

    # Show images
    for trial in imorder_shuf:
        # Insert a blank after waiting the desired image duration
        #blank.draw(), fix.draw()

        #last_flip = ec.flip(last_flip+imduration)
        # Draw a fixation dot of a random color a random portion of the time
        # through the ISI
        fix.set_colors(colors=(dcolor[trial], dcolor[trial]))
        # Stamp a trigger when the image goes on
        ec.call_on_next_flip(ec.stamp_triggers, imtype_shuf[trial], check='int4')
        # Draw the image
        img[trial].draw(), fix.draw()
        # The image is flipped ISI milliseconds after the blank
        last_flip = ec.flip(last_flip+ISI[trial]-adj)
        frametimes.append(last_flip)
        ec.check_force_quit()

    pressed = ec.get_presses()  # relative_to=0.0
