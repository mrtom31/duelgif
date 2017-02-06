# -*- coding: iso8859-1 -*- 
import Tkinter, Tkconstants, tkFileDialog, tkMessageBox
import os
import duelgif

class TkFileDialogExample(Tkinter.Frame):

    def __init__(self, root):

        Tkinter.Frame.__init__(self, root)

        # options for buttons
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

        # define buttons
        Tkinter.Button(self, text='select PNG or PLIST', command=self.askopenfilename).pack(**button_opt)

        self.label = Tkinter.Label(self, text='')
        self.label.pack()
        
        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = '.gif'
        options['filetypes'] = [('PLIST', ('*.png','*.plist')),('All types', '*.*')]
        options['initialdir'] = '.'
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root
        options['title'] = 'Open plist or png with same name'

        # This is only available on the Macintosh, and only when Navigation Services are installed.
        #options['message'] = 'message'

        # if you use the multiple file version of the module functions this option is set automatically.
        #options['multiple'] = 1

        # defining options for opening a directory
        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'Duel Gificator'
        
        self.filename = None
        self.path = None

    def askopenfile(self):

        """Returns an opened file in read mode."""

        return tkFileDialog.askopenfile(mode='r', **self.file_opt)

        
    def askopenfilename(self):

        """Returns an opened file in read mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """

        # get filename
        file_path = tkFileDialog.askopenfilename(**self.file_opt)
        
        if file_path is None:
            return
            
        file_path = file_path.replace('.png', '').replace('.plist', '')
        if not (os.path.isfile(file_path + '.png') and os.path.isfile(file_path + '.plist')):
            tkMessageBox.showwarning('File missing', 'Either plist or png file is missing !')
            return

        self.path, self.filename = os.path.split(file_path)
        self.label.config(text = self.filename)
        duelgif.create_anims(self.filename, self.path)
        tkMessageBox.showinfo('Gif complete', 'Gifs saved under ' + self.path)

        

def on_closing():
    global root
    root.destroy()


if __name__=='__main__':
    root = Tkinter.Tk()
    TkFileDialogExample(root).pack()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()