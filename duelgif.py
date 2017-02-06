# -*- coding: iso8859-1 -*- 
from plistlib import readPlist
from images2gif import writeGif
import os
from PIL import Image, ImageFont, ImageDraw


def anims_list(source, path):
    """
    Read source+'.plist' file to find unique animation keys.

    :param str source: file name without '.plist' extension.
    :return: list of strings for animations.
    """    
    anims = []
    plist = readPlist(os.path.join(path, source+'.plist'))
    
    for frame in plist.frames.keys():
        frame_split = frame[len(source):].split('_')
        if frame_split[-2] in anims:
            continue
        anims.append(frame_split[-2])
    return anims

def create_anim_gif(source, anim, path):
    """
    Create a gif image from the source+'.png' file for the specified animation.  Output gif file
    will be saved to same directory in format source+'_'+anim+'.gif' such that if source provided
    is 'neutral_koi' and anim is 'idle' the file 'neutral_koi_idle.gif' will be created.

    :param str source: source png file without '.png' extension.
    :param str anim: animation to create gif image for.
    :return: None
    """

    plist = readPlist(os.path.join(path, source+'.plist'))
    
    key = '{0}_{1}'.format(source, anim)
    key_splited = key.split('_')[0:3]

    frames = {}
    for frame in plist.frames.keys():
        if frame.split('_')[0:3] == key_splited:
            f = frame.replace('.png', '').replace(key+'_', '')
            frames[int(f)] = plist.frames[frame]

    pil_frames = []

    img = Image.open(os.path.join(path, source+'.png'))
    img.putalpha(20)
    string = "DO NOT MEME !!"
    cmpt = 0
    colors = ['black', 'green', 'blue', 'red']
    
    for f in frames:
        cmpt+=1
        coords = [int(c) for c in frames[f].frame.replace('{', '').replace('}', '').split(',')]
        coords[2] += coords[0]
        coords[3] += coords[1]
        cropped_img = img.crop((coords))
        
        dynamic_string = string[0:int((cmpt*len(string))/len(frames))]
        #draw_text(cropped_img, dynamic_string, color_rectangle=colors[cmpt%4])
        
        pil_frames.append(cropped_img)
    

    writeGif('{0}_{1}.gif'.format(source, anim), pil_frames, subRectangles=False)

def create_anims(source, path):
    """
    Given a source name, identify the animations and create each animated gif from source png.

    :param str source: source for png and plist without the '.png' or '.plist' extension.
    :return: None
    """
    
    anims = anims_list(source, path)

    for anim in anims:
        create_anim_gif(source, anim, path)
        # try:
            # create_anim_gif(source, anim)
        # except Exception as exception:
            # # TODO: This is some palette error with the gif creation script. Can probably fix later.
            # print(exception)
            # print 'Error when attempting to create "{0}" animation for {1}.'.format(anim, source)
            
    

            
def draw_text(img, string, color_rectangle='black'):
    # Back to repo directory for the fonts
    #os.chdir(repo_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/OpenSans-Bold.ttf", 14)
    size = draw.textsize(string, font=font)
    offset = font.getoffset(string)
    draw.rectangle([0, 0 , size[0]+offset[0], size[1]+offset[1]], fill=color_rectangle)
    draw.text((0, 0), string, font=font, fill= (255,255,255,0))
           
    return        

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Create gifs from Duelyst png and plist files. :P')
    parser.add_argument('source', type=str,
                        help='String name of file to process (neutral_koi for neutral_koi.png).')
    args = parser.parse_args()
    create_anims(args.source)
