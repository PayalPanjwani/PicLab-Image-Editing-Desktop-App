from tkinter import *
from PIL import ImageTk, Image, ImageGrab, ImageFilter, ImageEnhance
from tkinter import filedialog
import os
from tkinter.messagebox import showinfo

global original_img_open
global original_img
global saved_img
global open_img
global original_img_prev
global undo_img
global redo_img
undo_img=[]
redo_img=[]
root = Tk()
r=IntVar()
r.set("1")
root.title("PicLab - Photo Editor")

def displayImage(img):
    dispImage = ImageTk.PhotoImage(img)
    imagelabel = Label(root, image=dispImage, anchor="center")
    imagelabel.configure(image=dispImage)
    imagelabel.image = dispImage
    imagelabel.grid(row=0, column=0, rowspan=11, padx=10, pady=10, sticky="nsew")
   
def open_file():
    global open_img
    global original_img_open
    global original_img
    global imagelabel
    global undo_img
    open_img = filedialog.askopenfilename(title='Open Image')
    #filetypes=(("Png files","8.png"),("Jpg files","*.jpg"),("Jpeg files","*.jpeg"))

    if open_img:
        root.title(os.path.basename(open_img) + "-PicLab")
        original_img_open = Image.open(open_img)
        undo_img.append(original_img_open)
        w=original_img_open.size[0]
        original_img_open = original_img_open.resize((get_max(w,0), 650))
        displayImage(original_img_open)

def save_file():
    global saved_img
    global original_img
    saved_img = filedialog.asksaveasfilename(title="Save As")

    if saved_img:
        original_img_open.save(saved_img)
        displayImage(original_img_open)


def saveas_file():
    global saved_img
    global original_img_open
    saved_img = filedialog.asksaveasfilename(title="Save As")

    if saved_img:
        original_img_open.save(saved_img)
        displayImage(original_img_open)

def rotate_image():
    global original_img_open
    global undo_img

    undo_img.append(original_img_open) 
    #rotate_img = rotate_img.resize((1000, 650))
    rotate_img = original_img_open.rotate(90)
    original_img_open = rotate_img.copy()
    #original_img_open = original_img_open.resize((1000, 800))
    displayImage(original_img_open)

def undo():
        global original_img_open
        global undo_img
        global redo_img
        if undo_img :
            original_img_open=undo_img.pop()
            redo_img.append(original_img_open)
            displayImage(original_img_open)
        
def redo():
        global original_img_open
        global undo_img
        global redo_img
        if r.get() == 1:
         redo_img.pop()
         r.set("2")
        if redo_img:
            original_img_open=redo_img.pop()
            displayImage(original_img_open)
    
def flip(c):
    global original_img_open
    global undo_img
    undo_img.append(original_img_open)
    if(c==0):
        flip_img = original_img_open.transpose(Image.FLIP_LEFT_RIGHT)
    elif(c==1):
        flip_img = original_img_open.transpose(Image.FLIP_TOP_BOTTOM)

    original_img_open = flip_img.copy()
    displayImage(original_img_open)

def preview_brightness():
    global original_img_prev
    original_img_prev = original_img_open.copy()
    enhancer = ImageEnhance.Brightness(original_img_prev)
    original_img_prev=enhancer.enhance(brightnessslider.get())
    displayImage(original_img_prev)

def apply_brightness():
    global original_img_open
    global undo_img
    undo_img.append(original_img_open)
    enhancer = ImageEnhance.Brightness(original_img_open)
    original_img_open=enhancer.enhance(brightnessslider.get())
    displayImage(original_img_open)

def preview_contrast():
    global original_img_prev
    
    original_img_prev = original_img_open.copy()
    enhancer = ImageEnhance.Contrast(original_img_prev)
    original_img_prev=enhancer.enhance(contrastslider.get())
    displayImage(original_img_prev)

def apply_contrast():
    global original_img_open
    global undo_img
    undo_img.append(original_img_open)
    enhancer = ImageEnhance.Contrast(original_img_open)
    original_img_open=enhancer.enhance(contrastslider.get())
    displayImage(original_img_open)

def preview_sharpness():
    global original_img_prev
    original_img_prev = original_img_open.copy()
    enhancer = ImageEnhance.Sharpness(original_img_prev)
    original_img_prev=enhancer.enhance(sharpnessslider.get())
    displayImage(original_img_prev)

def apply_sharpness():
    global original_img_open
    global undo_img
    undo_img.append(original_img_open)
    enhancer = ImageEnhance.Sharpness(original_img_open)
    original_img_open=enhancer.enhance(sharpnessslider.get())
    displayImage(original_img_open)

def get_max(value,c):
    if c==0:
        if value > 1100 :
            return 1100
    elif c==1 :
        if value > 255:
            return 255

    return int(value)

def get_sepia_pixel(red, green, blue, alpha):
    nR = get_max((0.759 * red) + (0.398 * green) + (0.194 * blue),1)
    nG = get_max((0.676 * red) + (0.354 * green) + (0.173 * blue),1)
    nB = get_max((0.524 * red) + (0.277 * green) + (0.136 * blue),1)
   
    return nR, nG, nB, alpha

def convert_sepia(image):
    width, height = image.size

    new = Image.new("RGB", (width, height), "white")
    pixels = new.load()

    for i in range(0, width, 1):
        for j in range(0, height, 1):
            p = image.getpixel((i, j))
            pixels[i, j] = get_sepia_pixel(p[0], p[1], p[2], 255)

    # Return new image
    return new

def filters(c):
    global original_img_prev
    global original_img_open
    global undo_img
    undo_img.append(original_img_open)


    if(c==0):
        original_img_prev=original_img_open.convert('L')
        displayImage(original_img_prev)
    elif(c==1):
        original_img_prev = original_img_open.filter(ImageFilter.CONTOUR)
        displayImage(original_img_prev)
    elif(c==2):
        original_img_prev = original_img_open.filter(ImageFilter.DETAIL)
        displayImage(original_img_prev)
    elif(c==3):
        original_img_prev = original_img_open.filter(ImageFilter.EDGE_ENHANCE_MORE)
        displayImage(original_img_prev)
    elif(c==4):
        original_img_prev = original_img_open.filter(ImageFilter.EMBOSS)
        displayImage(original_img_prev)
    elif(c==5):
        original_img_prev = original_img_open.filter(ImageFilter.FIND_EDGES)
        displayImage(original_img_prev)
    elif(c==6):
        original_img_prev = original_img_open.filter(ImageFilter.SMOOTH)
        displayImage(original_img_prev)
    elif(c==7):
        original_img_prev = convert_sepia(original_img_open)
        displayImage(original_img_prev)
    elif(c==8):
        original_img_prev = original_img_open.filter(ImageFilter.BLUR)
        displayImage(original_img_prev)
    elif(c==9):
        original_img_open = original_img_prev.copy()
        displayImage(original_img_open)
    elif(c==10):
        displayImage(original_img_open)


def ratio(c):
    global original_img_open
    global undo_img
    undo_img.append(original_img_open)
    
    w,h=original_img_open.size
    r=w/h
    if(c==1):
       n_w=640
       n_h=480
    elif(c==2):
       n_w=480
       n_h=640
    elif(c==3):
       n_w=640
       n_h=360
    elif(c==4):
        n_w=360
        n_h=640
    elif(c==5):
        n_w=640
        n_h=426
    n_r=n_w/n_h
    
    if n_r > r :
        original_img_open= original_img_open.resize((w, round(w * n_h / n_w)),Image.ANTIALIAS)
        #box = (0, round((h - n_h) / 2), w, round((h + n_h) / 2))
        box=(0,0,w,n_h)
        original_img_open = original_img_open.crop(box)
    elif n_r < r :
        original_img_open = original_img_open.resize((round(h * n_w /n_h), h), Image.ANTIALIAS)
        #box = (round((w - n_w) / 2), 0, round((w + n_w) / 2), h)
        box=(0,0,w,n_h)
        original_img_open=original_img_open.crop(box)
    else:
        original_img_open=original_img_open.resize(n_w,n_h,Image.ANTIALIAS)
    displayImage(original_img_open)

def about():
    showinfo("PicLab" ,'''PicLab - The Photo Editing App allows you to enhance, brighten and sharpen your images as you like. It allows you to apply some amazing filters, resize your images and even undo and redo your edits.
Photoshop your pictures with PicLab and prepare your own lab of Pics!''')
    
def quitApp():
    root.destroy()



# mainmenu
mainmenu = Menu(root, font=("Times New Roman", 10))

# submenu
filemenu = Menu(mainmenu, tearoff=0, font=("Times New Roman", 10))
editmenu = Menu(mainmenu, tearoff=0, font=("Times New Roman", 10))
filtermenu = Menu(mainmenu, tearoff=0, font=("Times New Roman", 10))
scalemenu= Menu(mainmenu, tearoff=0, font=("Times New Roman", 10))
helpmenu = Menu(mainmenu, tearoff=0, font=("Times New Roman", 10))

# filemenu
filemenu.add_command(label="Open", command=open_file)
filemenu.add_command(label="Save", command=save_file)
filemenu.add_command(label="Save As", command=saveas_file)
filemenu.add_command(label="Exit",command=quitApp)

# editmenu
editmenu.add_command(label="Undo",command=undo)
editmenu.add_command(label="Redo",command=redo)

# filtermenu
filtermenu.add_command(label="B&W" ,command=lambda:filters(0))
filtermenu.add_command(label="Contour" ,command=lambda:filters(1))
filtermenu.add_command(label="Detail" ,command=lambda:filters(2))
filtermenu.add_command(label="Edge Enhance" ,command=lambda:filters(3))
filtermenu.add_command(label="Emboss" ,command=lambda:filters(4))
filtermenu.add_command(label="Find edges" ,command=lambda:filters(5))
filtermenu.add_command(label="Smooth" ,command=lambda:filters(6))
filtermenu.add_command(label="Sepia" ,command=lambda:filters(7))
filtermenu.add_command(label="Blur" ,command=lambda:filters(8))
filtermenu.add_command(label="Save filter" ,command=lambda:filters(9))
filtermenu.add_command(label="Cancel filter" ,command=lambda:filters(10))

# scalemenu
scalemenu.add_command(label="3:4",command=lambda:ratio(1))
scalemenu.add_command(label="4:3",command=lambda:ratio(2))
scalemenu.add_command(label="16:9",command=lambda:ratio(3))
scalemenu.add_command(label="9:16",command=lambda:ratio(4))
scalemenu.add_command(label="2:3",command=lambda:ratio(5))

mainmenu.add_cascade(label="File", menu=filemenu)
mainmenu.add_cascade(label="Edit", menu=editmenu)
mainmenu.add_cascade(label="Scale", menu=scalemenu)
mainmenu.add_cascade(label="Filters", menu=filtermenu)
mainmenu.add_cascade(label="Help", menu=helpmenu)

helpmenu.add_command(label="About",command=about)

root.config(menu=mainmenu)

# default image
original_img_open = Image.open("PicLab.png")
original_img = ImageTk.PhotoImage(original_img_open)

imagelabel = Label(root, image=original_img, anchor="center")
imagelabel.grid(row=0, column=0, rowspan=11, padx=20, pady=50, sticky="nsew")

# rotate button
rotate=Image.open("rotate.png")
rotate=rotate.resize((40,40))
rotate=ImageTk.PhotoImage(rotate)
rotatebutton = Button(root, image=rotate, command=rotate_image,borderwidth=0,relief="flat")
rotatebutton.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# flip button
flip_left_right = Image.open("flip1.jpg")
flip_left_right=flip_left_right.resize((40,40))
flip_left_right = ImageTk.PhotoImage(flip_left_right)
flipbutton1 = Button(root, image=flip_left_right, command=lambda:flip(0),borderwidth=0,relief="flat")
flipbutton1.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

# brightness
flip_top_bottom = Image.open("flip2.jpg")
flip_top_bottom=flip_top_bottom.resize((40,40))
flip_top_bottom = ImageTk.PhotoImage(flip_top_bottom)
flipbutton2 = Button(root, image=flip_top_bottom, command=lambda:flip(1),borderwidth=0,relief="flat")
flipbutton2.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")


brightnesslabel = Label(root, text="Brightness",height=1, font=("Times New Roman", 10))
brightnesslabel.grid(row=2, column=1, padx=10, pady=10, columnspan=3, sticky="nsew")

brightnessslider = Scale(root, orient=HORIZONTAL, from_=0,to=10, font=("Times New Roman", 10))
brightnessslider.grid(row=3, column=1, padx=10, pady=10, columnspan=3, sticky="nsew")

brightnesspreview = Button(root, text="Preview",height=1, font=("Times New Roman", 10), command=preview_brightness)
brightnesspreview.grid(row=4,column=1,padx=10,pady=10, sticky="nsew")

brightnessapply = Button(root, text="Apply", height=1,font=("Times New Roman", 10), command=apply_brightness)
brightnessapply.grid(row=4,column=2,padx=10,pady=10,sticky="nsew")

# contrast
contrastlabel = Label(root, text="Contrast",font=("Times New Roman", 10))
contrastlabel.grid(row=5, column=1, padx=10, pady=10, columnspan=3, sticky="nsew")

contrastslider = Scale(root, orient=HORIZONTAL, from_=-10,to=10, font=("Times New Roman", 10))
contrastslider.grid(row=6, column=1, padx=10, pady=10, columnspan=3,sticky="nsew")

contrastpreview = Button(root, text="Preview", font=("Times New Roman", 10), command=preview_contrast)
contrastpreview.grid(row=7,column=1,padx=10,pady=10,sticky="nsew")

contrastapply = Button(root, text="Apply", font=("Times New Roman", 10), command=apply_contrast)
contrastapply.grid(row=7,column=2,padx=10,pady=10,sticky="nsew")

# sharpness
sharpnesslabel = Label(root, text="Sharpness",font=("Times New Roman", 10))
sharpnesslabel.grid(row=8, column=1, padx=10, pady=10,  columnspan=3,sticky="nsew")

sharpnessslider = Scale(root, orient=HORIZONTAL, from_=-10,to=10, font=("Times New Roman", 10))
sharpnessslider.grid(row=9, column=1, padx=10, pady=10, columnspan=3,sticky="nsew")

sharpnesspreview = Button(root, text="Preview", font=("Times New Roman", 10), command=preview_sharpness)
sharpnesspreview.grid(row=10,column=1,padx=10,pady=10,sticky="nsew")

sharpnessapply = Button(root, text="Apply", font=("Times New Roman", 10), command=apply_sharpness)
sharpnessapply.grid(row=10,column=2,padx=10,pady=10,sticky="nsew")


root.mainloop()
