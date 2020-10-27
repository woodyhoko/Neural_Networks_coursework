
# coding: utf-8

# In[2]:

import matplotlib.pyplot as plt
from tkinter import *
import os
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import time
import math

class SN:
    random.seed(time.time())
    def __init__(self,n):
        self.w=[random.random() for i in range(n)]
    def ww(self,n,sw):
            self.w[n]=sw

class info:
    def __init__(self,record,data,nx1,nx2):
        self.root = Tk()
        self.root.title("info")
        self._job = None
        self.slider = Scale(self.root,orient=HORIZONTAL,length=1000,width=20,sliderlength=20,from_=0,to=10000,tickinterval=10000//20,command=self.updateValue(record,data,nx1,nx2))
        self.slider.pack()
        self.label=Label(self.root,text="Graph")
        self.label.pack()
        
        self.f = Figure(figsize=(5, 4), dpi=100)
        self.a = self.f.add_subplot(111)

        xs=[a[0] for a in data]
        ys=[a[1] for a in data]
        self.a.scatter(xs,ys,marker='o')
        for n in range(nx1):
            for m in range(nx2):
                if n!=nx1-1:
                    self.a.plot([record[0][n][m].w[0],record[0][n+1][m].w[0]],[record[0][n][m].w[1],record[0][n+1][m].w[1]],color='b'if record[0][n][m].w[2]==0 or record[0][n+1][m].w[2]==0 else 'r')
                if m!=nx2-1:
                    self.a.plot([record[0][n][m].w[0],record[0][n][m+1].w[0]],[record[0][n][m].w[1],record[0][n][m+1].w[1]],color='b'if record[0][n][m].w[2]==0 or record[0][n][m+1].w[2]==0 else 'r')
        self.a.axhline(0,color='g',linestyle='--')
        self.a.axvline(0,color='g',linestyle='--')

        self.a.set_title('Tk embedding')
        self.a.set_xlabel('X axis label')
        self.a.set_ylabel('Y label')
        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(f,self.root)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        self.container=Frame(self.root)
        self.container.pack(side="top", fill="both", expand = True)
        self.sbutton=Button(self.root,text="Start",command=self.startrun)
        self.sbutton.pack(side=TOP)
        self.qbutton=Button(self.root,text="Quit",command=sys.exit)
        self.qbutton.pack(side=BOTTOM)
        self.root.mainloop()
    def startrun(self):
        self.slider.set(self.slider.get()+1)
        
    def updateValue(self,record,data,nx1,nx2):
        if self._job:
            self.root.after_cancel(self._job)
        self._job = self.root.after(50, self._do_something(record,data,nx1,nx2))
    def _do_something(self,record,data,nx1,nx2):
        self._job = None

        self.f.clf()
        self.f = Figure(figsize=(5, 4), dpi=100)
        self.a = self.f.add_subplot(111)

        xs=[a[0] for a in data]
        ys=[a[1] for a in data]
        self.a.scatter(xs,ys,marker='o')
        t=int(self.slider.get())
        for n in range(nx1):
            for m in range(nx2):
                if n!=nx1-1:
                    self.a.plot([record[t][n][m].w[0],record[t][n+1][m].w[0]],[record[t][n][m].w[1],record[t][n+1][m].w[1]],color='b'if record[t][n][m].w[2]==0 or record[t][n+1][m].w[2]==0 else 'r')
                if m!=nx2-1:
                    plt.plot([record[t][n][m].w[0],record[t][n][m+1].w[0]],[record[t][n][m].w[1],record[t][n][m+1].w[1]],color='b'if record[t][n][m].w[2]==0 or record[t][n][m+1].w[2]==0 else 'r')
        self.a.axhline(0,color='g',linestyle='--')
        self.a.axvline(0,color='g',linestyle='--')
        self.a.set_title('Tk embedding')
        self.a.set_xlabel('X axis label')
        self.a.set_ylabel('Y label')
        # a tk.DrawingArea

        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

def somlearn(x,a,ttt,lr0,record,nx1,nx2,tau):
    minx=0
    miny=0
    minlen=(a[0][0].w[0]-x[0])**2+(a[0][0].w[1]-x[1])**2
    for n in range(nx1):
        for m in range(nx2):
            if (a[n][m].w[0]-x[0])**2+(a[n][m].w[1]-x[1])**2<minlen:
                minlen=(a[n][m].w[0]-x[0])**2+(a[n][m].w[1]-x[1])**2
                minx=n
                miny=m
    for n in range(nx1):
        for m in range(nx2):
            temp=lr0*math.exp(-ttt/tau)*math.exp(-((minx-n)**2+(miny-m)**2)/2/((1*math.exp(-ttt/tau))**2))
            a[n][m].w[0]+=temp*(x[0]-a[n][m].w[0])
            a[n][m].w[1]+=temp*(x[1]-a[n][m].w[1])
            record[ttt][n][m].w[0]=a[n][m].w[0]
            record[ttt][n][m].w[1]=a[n][m].w[1]
            if abs(temp*(x[0]-a[n][m].w[0]))>0.01 or abs(temp*(x[1]-a[n][m].w[1])>0.01) or (n==minx and m==miny):
                record[ttt][n][m].w[2]=1
            else:
                record[ttt][n][m].w[2]=0

def makefig(t,record,data,nx1,nx2):
    xs=[a[0] for a in data]
    ys=[a[1] for a in data]
    plt.scatter(xs,ys,marker='o')
    for n in range(nx1):
        for m in range(nx2):
            if n!=nx1-1:
                plt.plot([record[t][n][m].w[0],record[t][n+1][m].w[0]],[record[t][n][m].w[1],record[t][n+1][m].w[1]],color='b'if record[t][n][m].w[2]==0 or record[t][n+1][m].w[2]==0 else 'r')
            if m!=nx2-1:
                plt.plot([record[t][n][m].w[0],record[t][n][m+1].w[0]],[record[t][n][m].w[1],record[t][n][m+1].w[1]],color='b'if record[t][n][m].w[2]==0 or record[t][n][m+1].w[2]==0 else 'r')
    plt.axhline(0,color='g',linestyle='--')
    plt.axvline(0,color='g',linestyle='--')
    plt.show()

def read():
    filename=e[0].get()
    f=open(filename,'r')
    data=f.readlines()
    data=[list(map(float,line.split())) for line in data]
    dimension=len(data[0])-1

    Label(master,text="Learning rate : ").grid(row=3)
    Label(master,text="Learning time : ").grid(row=4)
    Label(master,text="Net's x1 axis : ").grid(row=5)
    Label(master,text="Net's x2 axis : ").grid(row=6)
    Label(master,text="tau(τ) :").grid(row=7)

    e[2]=Entry(master)
    e[3]=Entry(master)
    e[4]=Entry(master)
    e[5]=Entry(master)
    e[8]=Entry(master)

    e[2].grid(row=3,column=1)
    e[3].grid(row=4,column=1)
    e[4].grid(row=5,column=1)
    e[5].grid(row=6,column=1)
    e[8].grid(row=7,column=1)

    Button(master,text='Start',command=lambda:realstart(dimension,data)).grid(row=50,column=1, sticky=W,pady=4)

def realstart(dimension,data):
    
#     areas=sorted(list(map(int,list(set([point[dimension] for point in data])))))
    
#     for n in range(len(data)):
#         for m in range(len(areas)):
#             if areas[m]==data[n][dimension]:
#                 data[n][dimension]=(m/(len(areas)-1))
#     areas=sorted(list(map(float,list(set([point[dimension] for point in data])))))
    
    fn=e[0].get()
    savedir=e[1].get()
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    learningrate=float(e[2].get())
    time=int(e[3].get())
    netx1=int(e[4].get())
    netx2=int(e[5].get())
    tau=float(e[8].get())
    print(data)

#     data=[[random.random()for i in range(2)]for i in range(time)]

    somn=[[SN(2) for i in range(netx1)]for i in range(netx2)]
    recordsomn=[[[SN(3)for i in range(netx1)]for i in range(netx2)]for i in range(time+1)]

    for n in range(netx1):
        for m in range(netx2):
            recordsomn[0][n][m].w[0]=somn[n][m].w[0]
            recordsomn[0][n][m].w[1]=somn[n][m].w[1]

    for ttt  in range(time):
        if ttt%len(data)==0:
            random.shuffle(data)
        somlearn(data[ttt%len(data)],somn,ttt+1,learningrate,recordsomn,netx1,netx2,tau)
    ut=0
    while(ut!=-1):
        ut=int(input())
        makefig(ut,recordsomn,data,netx1,netx2)

    #recordinfo=info(recordsomn,data,netx1,netx2)
    #recordinfo.mainloop()

master = Tk()
master.title("Hw 3")
Label(master,text="Data File name : ").grid(row=0)
Label(master,text="Save folder name : ").grid(row=1)
Button(master,text='Read',command=read).grid(row=2,column=1, sticky=W,pady=4)

e=[Entry]*9

e[0]=Entry(master)
e[1]=Entry(master)

e[0].grid(row=0,column=1)
e[1].grid(row=1,column=1)

Button(master,text='Quit',command=master.quit,fg="red").grid(row=100,column=1,sticky=W,pady=4)

mainloop()

