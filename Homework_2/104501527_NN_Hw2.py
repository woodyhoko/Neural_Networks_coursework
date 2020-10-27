
# coding: utf-8

# In[4]:

import matplotlib.pyplot as plt
from tkinter import *
import os
import random
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time
import math

class SN:
    random.seed(time.time())
    def __init__(self,n):
        self.odw=[0 for i in range(n)]
        self.w=[random.random()*2-1 for i in range(n)]
    def ww(self,n,sw):
        self.w[n]=sw
    def dd(self,d):
        self.d=d
    def yy(self,y):
        self.y=y
    def odwodw(self,n,odw):
        self.odw[n]=odw

def getnum(a,sl,info,time):
    for n in range(sl[0]):
        a[0][n].yy(info[time][n])
    for n in range(len(sl)-1):
        for m in range(sl[n+1]):
            a[n+1][m].yy((1/(1+math.exp(-sum(a[n][x].y*a[n+1][m].w[x+1] for x in range(sl[n]))+(a[n+1][m].w[0])))))

def getarea(a,sl,an):
    areacheck=[0]*len(an)
    rarea=0
    for n in range(sl[-1]):
        bestan=3
        besta=0
        for m in range(len(an)):
            if bestan>abs(a[-1][n].y-(m*(1/(len(an)-1)))):
                bestan=abs(a[-1][n].y-(m*(1/(len(an)-1))))
                beata=m
        areacheck[beata]+=1
    for n in range(len(an)):
        if areacheck[n]==max(areacheck):
            rarea=n/(len(an)-1)
    return rarea

def calculate(a,sl,info,time):
    print(info[time])
    getnum(a,sl,info,time)
    for n in range(sl[-1]):
        a[-1][n].dd((info[time][sl[0]]-a[len(sl)-1][n].y)*a[len(sl)-1][n].y*(1-a[len(sl)-1][n].y))
    for n in range(len(sl)-2):
        for m in range(sl[-n-2]):
            a[-n-2][m].dd(a[-n-2][m].y*(1-a[-n-2][m].y)*sum(a[-n-1][x].w[m+1]*a[-n-1][x].d for x in range(sl[-n-1])))

def change(a,sl,lr,mo):
    for n in range(len(sl)-1):
        for m in range(sl[-n-1]):
            for p in range(sl[-n-2]+1):
                if p==0:
                    a[-n-1][m].ww(p,a[-n-1][m].w[p]+lr*a[-n-1][m].d*(-1)+mo*a[-n-1][m].odw[p])
                    a[-n-1][m].odwodw(p,lr*a[-n-1][m].d*(-1)+mo*a[-n-1][m].odw[p])
                else:
                    a[-n-1][m].ww(p,a[-n-1][m].w[p]+lr*a[-n-1][m].d*a[-n-2][p-1].y+mo*a[-n-1][m].odw[p])
                    a[-n-1][m].odwodw(p,lr*a[-n-1][m].d*a[-n-2][p-1].y+mo*a[-n-1][m].odw[p])

def checkrate(a,sl,info,an):
    cr=0
    statis=0
    for datanum in range(len(info)):
        getnum(a,sl,info,datanum)
        if getarea(a,sl,an)==info[datanum][-1]:
            statis+=1
    cr=statis/len(info)
    return cr

def makefig(a,sl,info,uinfo,tinfo,an,num,cr,sd,picnum):
    cs='bgcmyk'
    if len(uinfo[0])==3:
        for aaa,c in zip(an,cs):
            udata=list(filter(lambda point: point[2]==aaa,uinfo))
            xs=[point[0] for point in udata]
            ys=[point[1] for point in udata]
            plt.scatter(xs,ys,c=c,marker='o')
        for aaa,c in zip(an,cs):
            tdata=list(filter(lambda point: point[2]==aaa,tinfo))
            xs=[point[0] for point in tdata]
            ys=[point[1] for point in tdata]
            plt.scatter(xs,ys,c=c,marker='^')
        for aaa in range(len(info)):
            getnum(a,sl,info,aaa)
            if getarea(a,sl,an)!=info[aaa][-1]:
                plt.scatter(info[aaa][0],info[aaa][1],c='r',marker='x')
        plt.axhline(0,color='g',linestyle='--')
        plt.axvline(0,color='g',linestyle='--')
        plt.suptitle('Iteration : '+str(num), fontsize=12)
        plt.figtext(0.4,-0.05,'correct rate = '+ "%.3f"% cr)
        plt.savefig(sd+'/'+str(picnum)+'.png',bbox_inches='tight',pad_inches=0.3)
        plt.close('all')
    elif len(uinfo[0])==4:
        fig = plt.figure()
        aa=fig.add_subplot(111,projection='3d')
        for aaa,c in zip(an,cs):
            udata=list(filter(lambda point: point[3]==aaa,uinfo))
            xs=[point[0] for point in udata]
            ys=[point[1] for point in udata]
            zs=[point[2] for point in udata]
            aa.scatter(xs,ys,zs,c=c,marker='o')
        for aaa,c in zip(an,cs):
            tdata=list(filter(lambda point: point[3]==aaa,tinfo))
            xs=[point[0] for point in tdata]
            ys=[point[1] for point in tdata]
            zs=[point[2] for point in tdata]
            aa.scatter(xs,ys,zs,c=c,marker='^')
        for aaa in range(len(info)):
            getnum(a,sl,info,aaa)
            if getarea(a,sl,an)!=info[aaa][-1]:
                aa.scatter(info[aaa][0],info[aaa][1],info[aaa][2],c='r',marker='x')
        plt.suptitle('Iteration : '+str(num), fontsize=12)
        plt.figtext(0.4,-0.05,'correct rate = '+ "%.3f"% cr)
        plt.savefig(sd+'/'+str(picnum)+'.png',bbox_inches='tight',pad_inches=0.3)
        plt.close('all')

def numpic(a,sl,info,noise,an,sd):
    f,axarr=plt.subplots(4,4)
    statis=0
    for i in range(4):
        for k in range(4):
            temp=random.sample(range(25),noise)
            tempinfo=['']*2
            tempinfo[0]=info[i][:]
            for n in range(25):
                if n in temp:
                    tempinfo[0][n]=1-tempinfo[0][n]
            for n in range(5):
                for m in range(5):
                    if tempinfo[0][n*5+m]==1:
                        axarr[i,k].scatter(m,5-n,c='b',s=15,marker='s')
                    print(tempinfo)
                    getnum(a,sl,tempinfo,0)
                    axarr[i,k].set_title(str(int(getarea(a,sl,an)*3.1)))
            axarr[i][k].axis('off')
            if getarea(a,sl,an)==tempinfo[0][-1]:
                statis+=1
    statis=statis/16
    plt.suptitle('Noise level : '+str(noise), fontsize=12)
    plt.figtext(0.4,-0.05,'correct rate = '+ "%.3f"% statis)
    plt.savefig(sd+'/noiselevel_'+str(noise)+'.png',bbox_inches='tight',pad_inches=0.3)
    plt.close('all')
    return statis

def read():
    filename=e[0].get()
    f=open(filename,'r')
    data=f.readlines()
    if filename!="數字辨識.txt":
        random.shuffle(data)
    data=[list(map(float,line.split())) for line in data]
    dimension=len(data[0])-1

    Label(master,text="Learning rate : ").grid(row=3)
    Label(master,text="Learning time : ").grid(row=4)
    Label(master,text="Learn data rate : ").grid(row=5)
    Label(master,text="Accept correct rate : ").grid(row=6)
    Label(master,text="The number of neuron in each layers : ").grid(row=7)
    Label(master,text="Momentum value : ").grid(row=8)
    Label(master,text="tau(τ) :").grid(row=9)

    e[2]=Entry(master)
    e[3]=Entry(master)
    e[4]=Entry(master)
    e[5]=Entry(master)
    e[6]=Entry(master)
    e[7]=Entry(master)
    e[8]=Entry(master)

    e[2].grid(row=3,column=1)
    e[3].grid(row=4,column=1)
    e[4].grid(row=5,column=1)
    e[5].grid(row=6,column=1)
    e[6].grid(row=7,column=1)
    e[7].grid(row=8,column=1)
    e[8].grid(row=9,column=1)

    Button(master,text='Start',command=lambda:realstart(dimension,data)).grid(row=50,column=1, sticky=W,pady=4)
    
def realstart(dimension,data):
    
    areas=sorted(list(map(int,list(set([point[dimension] for point in data])))))
    
    for n in range(len(data)):
        for m in range(len(areas)):
            if areas[m]==data[n][dimension]:
                data[n][dimension]=(m/(len(areas)-1))
    areas=sorted(list(map(float,list(set([point[dimension] for point in data])))))
    
    fn=e[0].get()
    savedir=e[1].get()
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    learningrate=float(e[2].get())
    time=int(e[3].get())
    ldr=float(e[4].get())
    acceptrate=float(e[5].get())
    setuplayer=(e[6].get())
    setuplayer=list(map(int,setuplayer.split()))
    setuplayer=[dimension]+setuplayer
    momentum=float(e[7].get())
    tau=float(e[8].get())
    print(data)
    
    
    testdata=data[int(len(data)*ldr+1):-1:]
    usedata=data[0:int(len(data)*ldr):]
    
    mlp=['']*len(setuplayer)
    bestw=['']*(len(setuplayer)-1)
    for n in range(len(setuplayer)-1):
        mlp[n+1]=[SN(setuplayer[n]+1) for i in range(setuplayer[n+1])]
        bestw[n]=[SN(setuplayer[n]+1) for i in range(setuplayer[n+1])]
    mlp[0]=[SN(0) for i in range(setuplayer[0])]
    print(setuplayer)
    print(mlp)
    stime=0
    pic=0
    leastI=0
    raterecord=[0]*(time+1)
    writefile=open(savedir+'/record.txt','w+')
    writefile.write('data name : '+fn+'\n')
    writefile.write('learning rate : '+str(learningrate)+'\n')
    writefile.write('max time : '+str(time)+'\n')
    writefile.write('learn data rate : '+str(ldr)+'\n')
    writefile.write('accept rate : '+str(acceptrate)+'\n')
    writefile.write('setup layer : '+str(setuplayer)+'\n')
    writefile.write('momentum : '+str(momentum)+'\n')
    writefile.write('tau : '+str(tau)+'\n')
    writefile.write('______________________________\n\n')
    

    calculate(mlp,setuplayer,usedata,stime%len(usedata))
    if len(testdata)!=0:
        currentrate=checkrate(mlp,setuplayer,testdata,areas)
    else:
        currentrate=checkrate(mlp,setuplayer,usedata,areas)
    raterecord[stime]=currentrate
    bestscore=currentrate
    for n in range(len(setuplayer)-1):
        bestw[n]=mlp[n+1]
    print(stime,currentrate)
    writefile.write('no : '+str(stime)+'\n')
    writefile.write('current correct rate : '+str(currentrate)+'\n\n')
    for n in range(len(setuplayer)-1):
        writefile.write('layer : '+str(n+1)+'\n')
        for m in range(setuplayer[n+1]):
                writefile.write(str(mlp[n+1][m].w))
        writefile.write('\n')
    writefile.write('______________________________\n\n')
    makefig(mlp,setuplayer,data,usedata,testdata,areas,stime,currentrate,savedir,pic)
    calculate(mlp,setuplayer,usedata,stime%len(usedata))
    while(stime<=time-1 and currentrate<acceptrate):
        change(mlp,setuplayer,learningrate/(1+(stime/tau)),momentum)
        temp=currentrate
        if len(testdata)!=0:
            currentrate=checkrate(mlp,setuplayer,testdata,areas)
        else:
            currentrate=checkrate(mlp,setuplayer,usedata,areas)
        stime+=1
        raterecord[stime]=currentrate
        writefile.write('no.'+str(stime)+'\n')
        writefile.write('current correct rate : '+str(currentrate)+'\n\n')
        for n in range(len(setuplayer)-1):
            writefile.write('layer : '+str(n+1)+'\n')
            for m in range(setuplayer[n+1]):
                    writefile.write(str(mlp[n+1][m].w)+'\n')
            writefile.write('\n')
        writefile.write('______________________________\n\n')
        if temp!=currentrate:
            pic+=1
            makefig(mlp,setuplayer,data,usedata,testdata,areas,stime,currentrate,savedir,pic)
        if currentrate>bestscore:
            leastI=stime
            bestscore=currentrate
            for n in range(len(setuplayer)-1):
                bestw[n]=mlp[n+1]
        
        print(stime,currentrate)
        calculate(mlp,setuplayer,usedata,stime%len(usedata))
    plt.suptitle('Learning progress',fontsize=12)
    for chc in range(stime):
        plt.plot([chc,chc+1],[raterecord[chc],raterecord[chc+1]],color='b')
    plt.figtext(0.4,-0.05,'best rate = '+ "%.3f"% bestscore)
    plt.figtext(0.4,-0.1,'least iteration : '+ str(leastI))
    plt.axis([0,stime,0,1])
    plt.savefig(savedir+'/record.png',bbox_inches='tight', pad_inches=0.3)
    plt.close('all')
    writefile.write('best rate : '+str(bestscore)+'\n')
    writefile.write('least iteration : '+str(leastI)+'\n\n')
    for n in range(len(setuplayer)-1):
        writefile.write('layer : '+str(n+1)+'\n')
        for m in range(setuplayer[n+1]):
                writefile.write(str(bestw[n][m].w)+'\n')
        writefile.write('\n')
    writefile.write('______________________________')
    writefile.close()
    if dimension==25:
        statisrecord=[0]*11
        for n in range(11):
            statisrecord[n]=numpic(mlp,setuplayer,data,n,areas,savedir)
        plt.suptitle('Number recognition rate',fontsize=12)
        for chc in range(10):
            plt.plot([chc,chc+1],[statisrecord[chc],statisrecord[chc+1]],color='b')
        plt.axis([0,10,0,1])
        plt.savefig(savedir+'/noise_correct_rate_record.png',bbox_inches='tight', pad_inches=0.3)
        plt.close('all')

master = Tk()
master.title("Hw 2")
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

