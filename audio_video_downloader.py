from tkinter import *
from tkinter.ttk import Progressbar
import threading
import pafy
from tkinter import filedialog

root = Tk()
root.title("Audio video downloader")
root.geometry("900x550")
root.resizable(0,0)
root.configure(bg="yellow")

################################################## functions
def video_url():
    downloadinglabeltimeleft.configure(text ='')
    downloadingtextbarlabel.configure(text ='')
    downloadingsizelabelresult.configure(text ='')
    downloadinglabelresult.configure(text ='')
    getdetail = threading.Thread(target=getvideo)
    getdetail.start()

def getvideo():
    listb.delete(0,END)
    global streams
    url = urltext.get()
    data = pafy.new(url)
    streams = data.allstreams
    index = 0
    for i in streams:
        du ='{:0.1f}'.format(i.get_filesize()//(1024*1024))
        datas = str(index)+'.'.ljust(5," ")+str(i.quality).ljust(15," ")+str(i.extension).ljust(10," ")+str(i.mediatype)+"  "+ du.rjust(10," ")+ "MB"
        listb.insert(END,datas)
        index += 1
downloadindex = 0

def selectcursor(evt):
    global downloadindex
    listboxdata = listb.get(listb.curselection())
    downloadstream = listboxdata[:3]
    print(listboxdata)
    downloadindex = int(''.join(x for x in downloadstream if x.isdigit()))
   
def downloadvideo():
    getdata = threading.Thread(target=downloadvideodata)
    getdata.start()

def downloadvideodata():
    global downloadindex
    fgr = filedialog.askdirectory()
    downloadingtextbarlabel.configure(text ='downloading....')

    def mycallback(total,recvd,ratio,rate,eta):
        global total1
        total1 = float('{:.5}'.format(total/(1024*1024)))
        downloadingprogressbar.configure(maximum=total1)
        recieved1 = '{:.5}mb'.format(recvd/(1024*1024))
        eta1 = '{:.2f} sec'.format(eta)
        downloadingsizelabelresult.configure(text = total1)
        downloadinglabelresult.configure(text =recieved1)
        downloadinglabeltimeleft.configure(text=eta1)
        downloadingprogressbar['value']=recvd/(1024*1024)

    streams[downloadindex].download(filepath=fgr,quiet=True,callback=mycallback)
    downloadingtextbarlabel.configure(text ='downloaded')

###########################################################################  scrollbar
scrollbar = Scrollbar(root)
scrollbar.place(x=527,y=200,height=245,width=25)

########################################################################### labels

introlabel = Label(root,text ="welcome to youtube video downloader",fg = "white",bg="green",
font =('calibri',30,'italic bold'),width=35,relief = 'groove',bd=5,height=1)
introlabel.place(x= 10,y=10)

listb = Listbox(root,width= 55,height=12,font=('arial',12,'bold'),relief='groove',
yscrollcommand = scrollbar.set)
listb.place(x=30,y=200)
listb.bind('ListboxSelect',selectcursor)

downloadingsizelabel = Label(root,text = 'Total size : ',font = ('calibri',15,'bold'),bg='yellow')
downloadingsizelabel.place(x = 600,y= 200)

downloadinglabel = Label(root,text = 'Recieved size : ',font = ('calibri',15,'bold'),bg='yellow')
downloadinglabel.place(x = 600,y= 240)

downloadingtime = Label(root,text = 'Time left : ',font = ('calibri',15,'bold'),bg='yellow')
downloadingtime.place(x = 600,y= 280)

downloadingsizelabelresult = Label(root,text = '',font = ('calibri',15,'bold'),bg='yellow')
downloadingsizelabelresult.place(x = 750,y= 200)

downloadinglabelresult = Label(root,text = '',font = ('calibri',15,'bold'),bg='yellow')
downloadinglabelresult.place(x = 750,y= 240)

downloadinglabeltimeleft = Label(root,text = '',font = ('calibri',15,'bold'),bg='yellow')
downloadinglabeltimeleft.place(x = 750,y= 280)

downloadingtextbarlabel = Label(root,text='Downloading bar',width=36,font =('calibri',20,'bold'),
fg = 'red',bg = 'yellow')
downloadingtextbarlabel.place(x=500,y=500)

downloadprogressbarlabel = Label(root,text='',width=40,font=('calibri',20,'bold'),fg ='red',bg='yellow',
relief='groove')
downloadprogressbarlabel.place(x=25,y=500)
total1= 0

downloadingprogressbar = Progressbar(downloadprogressbarlabel,orient = HORIZONTAL,value=0,length=100,maximum=total1)
downloadingprogressbar.grid(row=0,column=0,ipady=9,ipadx=250)

#######################################################################################  entry
urltext = StringVar()
urlentry  = Entry(root,textvariable = urltext,font = ('calibri',20,'bold'),width = 38,
relief ='groove',bd=5)
urlentry.place(x = 25,y=120)

############################################################################################  button

clickbutton = Button(root,text ='Enter url and Click',font =('calibri',14,'bold'),width=20,fg ='white',
bg='blue',relief ='groove',bd=5,activebackground='green',command=video_url)
clickbutton.place(x= 600,y=120)

downloadbutton = Button(root,text = 'Download',font =('calibri',15,'bold'),width=25,fg='white',bg='sea green',
relief = 'groove',bd =5,activebackground='green',command=downloadvideo)
downloadbutton.place(x=600,y=350)

root.mainloop()