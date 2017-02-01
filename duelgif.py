import plistlib
import images2gif
import argparse
from PIL import Image

def anims_list(source):
    """
    Read source+'.plist' file to find unique animation keys.

    :param str source: file name without '.plist' extension.
    :return: list of strings for animations.
    """
    anims = []
    plist = plistlib.readPlist(source+'.plist')

    for frame in plist.frames.keys():
        frame_split = frame[len(source):].split('_')
        if frame_split[-2] in anims:
            continue
        anims.append(frame_split[-2])
    return anims

def create_anim_gif(source, anim):
    """
    Create a gif image from the source+'.png' file for the specified animation.  Output gif file
    will be saved to same directory in format source+'_'+anim+'.gif' such that if source provided
    is 'neutral_koi' and anim is 'idle' the file 'neutral_koi_idle.gif' will be created.

    :param str source: source png file without '.png' extension.
    :param str anim: animation to create gif image for.
    :return: None
    """
	

    plist = plistlib.readPlist(source+'.plist')

    key = '{0}_{1}'.format(source, anim)
    len_key = len(key)

    frames = {}
    for frame in plist.frames.keys():
        if frame[0:len_key] == key:
            f = frame.replace('.png', '').replace(key+'_', '')
            frames[int(f)] = plist.frames[frame]

    pil_frames = []

    img = Image.open(source+'.png')
    for f in frames:
        coords = [int(c) for c in frames[f].frame.replace('{', '').replace('}', '').split(',')]
        coords[2] += coords[0]
        coords[3] += coords[1]
        cropped_img = img.crop((coords))
        pil_frames.append(cropped_img)

    images2gif.writeGif('{0}_{1}.gif'.format(source, anim), pil_frames, subRectangles=False)

def create_anims(source):
    """
    Given a source name, identify the animations and create each animated gif from source png.

    :param str source: source for png and plist without the '.png' or '.plist' extension.
    :return: None
    """
    anims = anims_list(source)

    for anim in anims:
        create_anim_gif(source, anim)
        # try:
            # create_anim_gif(source, anim)
        # except Exception as exception:
            # # TODO: This is some palette error with the gif creation script. Can probably fix later.
            # print(exception)
            # print 'Error when attempting to create "{0}" animation for {1}.'.format(anim, source)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create gifs from Duelyst png and plist files. :P')
    parser.add_argument('source', type=str,
                        help='String name of file to process (neutral_koi for neutral_koi.png).')
    args = parser.parse_args()
    create_anims(args.source)
