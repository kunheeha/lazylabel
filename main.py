''' 
Author: Adam de Haro
github.com/adzcodez

'''

import argparse
import tkinter
import os
import pathlib
from PIL import Image, ImageTk
import speech_recognition as sr
import time
import threading

def parse_args(): 
    '''
    Parses arguments from the namespace object to pass to the main function. 
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument('--image_dir', help='The folder to label. ', default='/Users/kunheeha/Desktop/AdamCode/lazylabel/images')

    return parser.parse_args()

def get_images(config):
    '''
    Returns a list of paths to images which require labelling. 
    '''
    images = []
    for image in os.listdir(config.image_dir):
        img = config.image_dir + '/' + image # Isn't there a more elegant way to do this? 
        _, ext = os.path.splitext(img)
        if ext in extensions:
            images.append(img)
    
    return images

def tk_image(path):
    img = Image.open(path)
    storeobj = ImageTk.PhotoImage(img)

    return storeobj

class PictureWindow(tkinter.Canvas):
    '''
    Basing this off https://www.bitforestinfo.com/2017/02/how-to-create-image-viewer-using-python.html
    '''
    def __init__(self, *args, **kwargs):
        tkinter.Canvas.__init__(self, *args, **kwargs)
        self.imagelist = get_images(config)
        self.imagelist_p = []
        self.listen = self.all_function_trigger()
        thread = threading.Thread(target=self.perform_command)    # Threading needed to be able to delete image and listen at the same time
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()
        thread.start()                                            # https://stackoverflow.com/a/36340748

    def show_image(self, path):
        img = tk_image(path)
        self.delete(self.find_withtag("bacl"))
        self.allready = self.create_image(self.winfo_screenwidth()/2,self.winfo_screenheight()/2,image=img, anchor='center', tag="bacl")

        self.image = img
        print(self.find_withtag("bacl"))
        self.master.title(f"Image Viewer ({path})")
        return
    
    def previous_image(self):
        try:
            pop = self.imagelist_p.pop()
            self.show_image(pop)
            self.imagelist.append(pop)
        except:
            pass
        return
    
    def next_image(self):
        try:
            pop = self.imagelist.pop()

            self.show_image(pop)
            self.imagelist_p.append(pop)
        except EOFError:
            pass
        return

    def all_function_trigger(self):
        listen = self.create_buttons()
        self.window_settings()
        return listen

    def create_buttons(self):
        tkinter.Button(self, text=" > ", command=self.next_image).place(x=(self.winfo_screenwidth()/1.1),y=(self.winfo_screenheight()/2))
        tkinter.Button(self, text=" < ", command=self.previous_image).place(x=20,y=(self.winfo_screenheight()/2))
        listen = tkinter.Button(self, text=" Listen ", command=self.perform_command)
        listen.place(x=20,y=(self.winfo_screenheight()/3))

        self['bg']="white"
        return listen
    
    def window_settings(self):
        self['width'] = self.winfo_screenwidth()
        self['height'] = self.winfo_screenheight()

    def recognise_speech(self):
        '''
        https://dev.to/mshrish/making-a-simple-voice-controlled-personal-assistant-interface-using-python-5ce1
        '''
        # r = sr.Recognizer()
        # mic = sr.Microphone()

        with self.mic as s:
            audio = self.r.listen(s)
            self.r.adjust_for_ambient_noise(s)
        
        try:
            speech = self.r.recognize_google(audio)
            return speech

        except sr.UnknownValueError:
            print("Please try again. ")

    def perform_command(self):
        '''
        This function should take the recognised speech and then perform the command. 
        '''
        print(f"Keep or delete? ")
        speech = str(self.recognise_speech()).lower()
        print(f"{speech}")

        keep = ["keep", "keith", "key", "kip", "kate", "one", "want", "teeth", "none", "peace", "deep"] # These are the words it keeps thinking I'm saying
        delete = ["delete", "two", "poo", "who", "elite", "belize", "deli", "denise", "did he", "elise", "dolese"]

        if speech in keep:
            self.next_image()
            self.perform_command()

        elif speech in delete:
            path = self.imagelist_p.pop()
            self.next_image()
            self.delete_image(path)  
            self.perform_command()  

        else:
            print("Command not understood")
            # time.sleep(3) 
            self.perform_command()

    def delete_image(self, path):
        print(f"deleting image {path}")
        os.remove(path)


def main(config):

    root = tkinter.Tk(className=" Image Viewer ")

    PictureWindow(root).pack(expand="yes", fill="both")

    root.resizable(width=0, height=0)

    root.mainloop()

    return

if __name__ == '__main__':
    config = parse_args()
    extensions = ['.png', '.jpg']

    main(config)