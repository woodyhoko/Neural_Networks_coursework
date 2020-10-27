
import matplotlib.pyplot as plt
from tkinter import *
import os
import random
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def read():

    filename=e[0].get()

    f=open(filename,'r')
    data=f.readlines()
    random.shuffle(data)

    data=[list(map(float,line.split())) for line in data]

    dimension=len(data[0])-1

    Label(master,text="Learning rate : ").grid(row=3)
    Label(master,text="Learning time : ").grid(row=4)
    Label(master,text="Learn data rate : ").grid(row=5)
    Label(master,text="Accept correct rate : ").grid(row=6)
    Label(master,text="initialize").grid(row=7)
    Label(master,text=("Dimension : "+str(dimension))).grid(row=7,column=1)
    Label(master,text="Threshold : ").grid(row=8)
    di=0
    
    i=[Entry]*(dimension+1)
    for di in range(dimension):
        Label(master,text=("wieght","of","x"+str(di+1),":")).grid(row=di+9)
        i[di+1]=Entry(master)
        i[di+1].grid(row=di+9,column=1)
    e[2]=Entry(master)
    e[3]=Entry(master)
    e[4]=Entry(master)
    e[5]=Entry(master)
    i[0]=Entry(master)

    e[2].grid(row=3,column=1)
    e[3].grid(row=4,column=1)
    e[4].grid(row=5,column=1)
    e[5].grid(row=6,column=1)
    i[0].grid(row=8,column=1)

    Button(master,text='Start',command=lambda:realstart(dimension,data,i)).grid(row=50,column=1, sticky=W,pady=4)

def realstart(dimension,data,i):
    
    areas=sorted(list(map(int,list(set([point[dimension] for point in data])))))
    
    print(areas)
    
    cs='brgcmyk'
    
    smartlineinfo=[[int]*2 for _ in range(sum(k for k in range(len(areas))))]
    ax=ay=0
    for aa in range(sum(k for k in range(len(areas)))):
        ay+=1
        if ay>=len(areas):
            ax+=1
            ay=ax+1
        smartlineinfo[aa][0]=areas[ax]
        smartlineinfo[aa][1]=areas[ay]
    
    
    savedir=e[1].get()
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    learningrate=float(e[2].get())
    ldr=float(e[4].get())
    print(data)

    largest=[float]*(dimension+1)
    smallest=[float]*(dimension+1)

    for k in range(dimension+1):
        largest[k]=smallest[k]=data[0][k]

    for k in range(len(data)):
        for w in range(dimension):
            if largest[w]<data[k][w]:
                largest[w]=data[k][w]
            elif smallest[w]>data[k][w]:
                smallest[w]=data[k][w]
    
    smartline=[[float]*(dimension+1) for _ in range(sum(k for k in range(len(areas))))]
    
    bestsmartline=[[float]*(dimension+1) for _ in range(sum(k for k in range(len(areas))))]
    bestrate=0
    
    for aa in range(sum(k for k in range(len(areas)))):
        thres=float(i[0].get())
        smartline[aa][0]=thres
        for k in range(dimension):
            smartline[aa][k+1]=float(i[k+1].get())

        for aa in range(sum(k for k in range(len(areas)))):
            print(', '.join(str(x) for x in smartline[aa]))

    n=int(e[3].get())
    acceptrate=float(e[5].get())

    raterecord=[float]*(n+1)

    for aa in range(sum(k for k in range(len(areas)))):
        for bb in range(dimension+1):
            if smartline[aa][bb]==0:
                smartline[aa][bb]+=0.000000001
    
    r=0
    currentrate=0
    correctnum=0
    if r<len(data)-int(len(data)*ldr)!=0:
        while(r<len(data)-int(len(data)*ldr)):
            counting=[0]*(sum(k for k in range(len(areas)))+2)
            besta=0
            for aa in range(sum(k for k in range(len(areas)))):
                if (-smartline[aa][0]+sum(smartline[aa][k+1]*data[(int(len(data)*ldr)+r)][k] for k in range(dimension)))>((smartlineinfo[aa][0]+smartlineinfo[aa][1])/2):
                    counting[smartlineinfo[aa][1]]+=1
                else:
                    counting[smartlineinfo[aa][0]]+=1
            for aa in range(sum(k for k in range(len(areas)))+2):
                if counting[aa]>counting[besta]:
                    besta=aa
            if besta==int(data[(int(len(data)*ldr)+r)][dimension]):
                correctnum+=1
            r+=1
        currentrate=correctnum/(len(data)-int(len(data)*ldr))
    else:
        while(r<len(data)):
            counting=[0]*(sum(k for k in range(len(areas)))+2)
            besta=0
            for aa in range(sum(k for k in range(len(areas)))):
                if (-smartline[aa][0]+sum(smartline[aa][k+1]*data[r][k] for k in range(dimension)))>((smartlineinfo[aa][0]+smartlineinfo[aa][1])/2):
                    counting[smartlineinfo[aa][1]]+=1
                else:
                    counting[smartlineinfo[aa][0]]+=1
            for aa in range(sum(k for k in range(len(areas)))+2):
                if counting[aa]>counting[besta]:
                    besta=aa
            if besta==int(data[r][dimension]):
                correctnum+=1
            r+=1
        currentrate=correctnum/(len(data))
    
    raterecord[0]=currentrate
    
    print(currentrate)
    
    pic=0
    t=0
    
    if(dimension==2):
        for area, c in zip(areas, cs):
            fdata=list(filter(lambda point: point[2]==area, data[:int(len(data)*ldr-1):]))
            xs=[point[0] for point in fdata]
            ys=[point[1] for point in fdata]
            plt.scatter(xs, ys, c=c, marker='o')

        for area, c in zip(areas, cs):
            fdata=list(filter(lambda point: point[2]==area, data[int(len(data)*ldr):]))
            xs=[point[0] for point in fdata]
            ys=[point[1] for point in fdata]
            plt.scatter(xs, ys, c=c, marker='^')
        plt.axhline(0,color='g', linestyle='--')
        plt.axvline(0,color='g', linestyle='--')
        
        for aa in range(sum(k for k in range(len(areas)))):
            plt.plot([smallest[0]-1,largest[0]+1],[(smartline[aa][0]-smartline[aa][1]*(smallest[0]-1))/smartline[aa][2],(smartline[aa][0]-smartline[aa][1]*(largest[1]+1))/smartline[aa][2]],color=cs[aa])
            parastr=['{:.3f}'.format(x) for x in smartline[aa]]
            plt.figtext(0.25,-0.05-0.05*aa,'Parameter'+str(aa)+' = '+'{ '+', '.join(x for x in parastr)+' }')
        plt.figtext(0.4,-0.05-0.05*(sum(k for k in range(len(areas)))),'correct rate = '+ "%.3f"% currentrate)
        plt.axis([smallest[0]-1,largest[0]+1,smallest[1]-1,largest[1]+1])
        plt.suptitle('Initialized status ', fontsize=12)
        plt.savefig(savedir+'/'+str(pic)+'.png',bbox_inches='tight', pad_inches=0.3)
        plt.close('all')
        
    elif(dimension==3):
        fig = plt.figure()
        aaa = fig.add_subplot(111, projection='3d')
        for area, c in zip(areas, cs):
            fdata=list(filter(lambda point: point[3]==area, data[:int(len(data)*ldr-1):]))
            xs=[point[0] for point in fdata]
            ys=[point[1] for point in fdata]
            zs=[point[2] for point in fdata]
            aaa.scatter(xs, ys, zs, c=c, marker='o')
        for area, c in zip(areas, cs):
            fdata=list(filter(lambda point: point[3]==area, data[int(len(data)*ldr):]))
            xs=[point[0] for point in fdata]
            ys=[point[1] for point in fdata]
            zs=[point[2] for point in fdata]
            aaa.scatter(xs, ys, zs, c=c, marker='^')
        X=np.arange(smallest[0]-1,largest[0]+1,(-smallest[0]+largest[0])/10)
        Y=np.arange(smallest[1]-1,largest[1]+1,(-smallest[1]+largest[1])/10)
        X,Y=np.meshgrid(X,Y)
        for aa in range(sum(k for k in range(len(areas)))):
            Z=(((smartlineinfo[aa][0]+smartlineinfo[aa][1])/2)+smartline[aa][0]-smartline[aa][1]*X-smartline[aa][2]*Y)/smartline[aa][3]
            aaa.plot_wireframe(X,Y,Z,color=cs[aa])
            parastr=['{:.3f}'.format(x) for x in smartline[aa]]
            plt.figtext(0.25,-0.05-0.05*aa,'Parameter'+str(aa+1)+' = '+'{ '+', '.join(x for x in parastr)+' }')
        aaa.set_zlim3d(smallest[2]-1,largest[2]+1)
        plt.figtext(0.4,-0.05-0.05*(sum(k for k in range(len(areas)))),'correct rate = '+ "%.3f"% currentrate)
        plt.suptitle('Iteration '+str(t), fontsize=12)
        plt.axis([smallest[0]-1,largest[0]+1,smallest[1]-1,largest[1]+1])
        plt.savefig(savedir+'/'+str(pic)+'.png',bbox_inches='tight', pad_inches=0.3)
        plt.close('all')
        
    else:
        for aa in range(sum(k for k in range(len(areas)))):
            parastr=['{:.3f}'.format(x) for x in smartline[aa]]
            plt.figtext(0.25,-0.05-0.05*aa,'Parameter'+str(aa+1)+' = '+'{ '+', '.join(x for x in parastr)+' }')
        plt.suptitle('Iteration '+str(t), fontsize=12)
        plt.figtext(0.4,-0.05-0.05*(sum(k for k in range(len(areas)))),'correct rate = '+ "%.3f"% currentrate)
        plt.savefig(savedir+'/'+str(pic)+'.png',bbox_inches='tight', pad_inches=0.3)
        plt.close('all')
        
    
    while(t<n and currentrate<acceptrate):
        
        check=0
        
        for aa in range(sum(k for k in range(len(areas)))):
            if (-smartline[aa][0]+sum(smartline[aa][k+1]*data[t%int(len(data)*ldr)][k] for k in range(dimension))>=(smartlineinfo[aa][0]+smartlineinfo[aa][1])/2) and (data[t%int(len(data)*ldr)][dimension]<(smartlineinfo[aa][0]+smartlineinfo[aa][1])/2):
                smartline[aa][0]-=-learningrate
                for k in range(dimension):
                    smartline[aa][k+1]-=learningrate*data[t%int(len(data)*ldr)][k]
                check=1
            elif (-smartline[aa][0]+sum(smartline[aa][k+1]*data[t%int(len(data)*ldr)][k] for k in range(dimension))<=(smartlineinfo[aa][0]+smartlineinfo[aa][1])/2) and (data[t%int(len(data)*ldr)][dimension]>(smartlineinfo[aa][0]+smartlineinfo[aa][1])/2):
                smartline[aa][0]+=-learningrate
                for k in range(dimension):
                    smartline[aa][k+1]+=learningrate*data[t%int(len(data)*ldr)][k]
                check=1

        for aa in range(sum(k for k in range(len(areas)))):
            for bb in range(dimension+1):
                if smartline[aa][bb]==0:
                    smartline[aa][bb]+=0.000000001
        
        correctnum=0
        r=0
        if r<len(data)-int(len(data)*ldr)!=0:
            while(r<len(data)-int(len(data)*ldr)):
                counting=[0]*(sum(k for k in range(len(areas)))+2)
                besta=0
                for aa in range(sum(k for k in range(len(areas)))):
                    if (-smartline[aa][0]+sum(smartline[aa][k+1]*data[(int(len(data)*ldr)+r)][k] for k in range(dimension)))>((smartlineinfo[aa][0]+smartlineinfo[aa][1])/2):
                        counting[smartlineinfo[aa][1]]+=1
                    else:
                        counting[smartlineinfo[aa][0]]+=1
                for aa in range(sum(k for k in range(len(areas)))+2):
                    if counting[aa]>counting[besta]:
                        besta=aa
                if besta==int(data[(int(len(data)*ldr)+r)][dimension]):
                    correctnum+=1
                r+=1
            currentrate=correctnum/(len(data)-int(len(data)*ldr))
        else:
            while(r<len(data)):
                counting=[0]*(sum(k for k in range(len(areas)))+2)
                besta=0
                for aa in range(sum(k for k in range(len(areas)))):
                    if (-smartline[aa][0]+sum(smartline[aa][k+1]*data[r][k] for k in range(dimension)))>((smartlineinfo[aa][0]+smartlineinfo[aa][1])/2):
                        counting[smartlineinfo[aa][1]]+=1
                    else:
                        counting[smartlineinfo[aa][0]]+=1
                for aa in range(sum(k for k in range(len(areas)))+2):
                    if counting[aa]>counting[besta]:
                        besta=aa
                if besta==int(data[r][dimension]):
                    correctnum+=1
                r+=1
            currentrate=correctnum/(len(data))
        
        t+=1
        
        if check!=0:
            pic+=1
            print(t)
            for aa in range(sum(k for k in range(len(areas)))):
                print("neuron"+str(aa+1)+" : "+', '.join(str(x) for x in smartline[aa]))
            print(currentrate)
            
            if(dimension==2):
                for area, c in zip(areas, cs):
                    fdata=list(filter(lambda point: point[2]==area, data[:int(len(data)*ldr-1):]))
                    xs=[point[0] for point in fdata]
                    ys=[point[1] for point in fdata]
                    plt.scatter(xs, ys, c=c, marker='o')
                
                for area, c in zip(areas, cs):
                    fdata=list(filter(lambda point: point[2]==area, data[int(len(data)*ldr):]))
                    xs=[point[0] for point in fdata]
                    ys=[point[1] for point in fdata]
                    plt.scatter(xs, ys, c=c, marker='^')
                plt.axhline(0,color='g', linestyle='--')
                plt.axvline(0,color='g', linestyle='--')
                
                for aa in range(sum(k for k in range(len(areas)))):
                    plt.plot([smallest[0]-1,largest[0]+1],[(smartline[aa][0]+((smartlineinfo[aa][0]+smartlineinfo[aa][1])/2)-smartline[aa][1]*(smallest[0]-1))/smartline[aa][2],(smartline[aa][0]+((smartlineinfo[aa][0]+smartlineinfo[aa][1])/2)-smartline[aa][1]*(largest[0]+1))/smartline[aa][2]],color=cs[aa])
                    parastr=['{:.3f}'.format(x) for x in smartline[aa]]
                    plt.figtext(0.25,-0.05-0.05*aa,'Parameter'+str(aa+1)+' = '+'{ '+', '.join(x for x in parastr)+' }')
                plt.figtext(0.4,-0.05-0.05*(sum(k for k in range(len(areas)))),'correct rate = '+ "%.3f"% currentrate)
                plt.suptitle('Iteration '+str(t), fontsize=12)
                plt.axis([smallest[0]-1,largest[0]+1,smallest[1]-1,largest[1]+1])
                plt.savefig(savedir+'/'+str(pic)+'.png',bbox_inches='tight', pad_inches=0.3)
                plt.close('all')
                
            elif(dimension==3):
                fig = plt.figure()
                aaa = fig.add_subplot(111, projection='3d')
                for area, c in zip(areas, cs):
                    fdata=list(filter(lambda point: point[3]==area, data[:int(len(data)*ldr-1):]))
                    xs=[point[0] for point in fdata]
                    ys=[point[1] for point in fdata]
                    zs=[point[2] for point in fdata]
                    aaa.scatter(xs, ys, zs, c=c, marker='o')
                for area, c in zip(areas, cs):
                    fdata=list(filter(lambda point: point[3]==area, data[int(len(data)*ldr):]))
                    xs=[point[0] for point in fdata]
                    ys=[point[1] for point in fdata]
                    zs=[point[2] for point in fdata]
                    aaa.scatter(xs, ys, zs, c=c, marker='^')
                X=np.arange(smallest[0]-1,largest[0]+1,(-smallest[0]+largest[0])/10)
                Y=np.arange(smallest[1]-1,largest[1]+1,(-smallest[1]+largest[1])/10)
                X,Y=np.meshgrid(X,Y)
                for aa in range(sum(k for k in range(len(areas)))):
                    Z=(((smartlineinfo[aa][0]+smartlineinfo[aa][1])/2)+smartline[aa][0]-smartline[aa][1]*X-smartline[aa][2]*Y)/smartline[aa][3]
                    aaa.plot_wireframe(X,Y,Z,color=cs[aa])
                    parastr=['{:.3f}'.format(x) for x in smartline[aa]]
                    plt.figtext(0.25,-0.05-0.05*aa,'Parameter'+str(aa+1)+' = '+'{ '+', '.join(x for x in parastr)+' }')
                aaa.set_zlim3d(smallest[2]-1,largest[2]+1)
                plt.figtext(0.4,-0.05-0.05*(sum(k for k in range(len(areas)))),'correct rate = '+ "%.3f"% currentrate)
                plt.suptitle('Iteration '+str(t), fontsize=12)
                plt.axis([smallest[0]-1,largest[0]+1,smallest[1]-1,largest[1]+1])
                plt.savefig(savedir+'/'+str(pic)+'.png',bbox_inches='tight', pad_inches=0.3)
                plt.close('all')
            else:
                for aa in range(sum(k for k in range(len(areas)))):
                    parastr=['{:.3f}'.format(x) for x in smartline[aa]]
                    plt.figtext(0.25,-0.05-0.05*aa,'Parameter'+str(aa+1)+' = '+'{ '+', '.join(x for x in parastr)+' }')
                plt.suptitle('Iteration '+str(t), fontsize=12)
                plt.figtext(0.4,-0.05-0.05*(sum(k for k in range(len(areas)))),'correct rate = '+ "%.3f"% currentrate)
                plt.savefig(savedir+'/'+str(pic)+'.png',bbox_inches='tight', pad_inches=0.3)
                plt.close('all')
                
        raterecord[t]=currentrate
        if currentrate>bestrate:
            bestsmartline=smartline
            bestrate=currentrate
            
    plt.suptitle('Learning progress',fontsize=12)
    for chc in range(n):
        plt.plot([chc,chc+1],[raterecord[chc],raterecord[chc+1]],color='b')
    for aa in range(sum(k for k in range(len(areas)))):
        parastr=['{:.3f}'.format(x) for x in bestsmartline[aa]]
        plt.figtext(0.25,-0.05-0.05*aa,'Parameter'+str(aa+1)+' = '+'{ '+', '.join(x for x in parastr)+' }')
    plt.figtext(0.4,-0.05-0.05*(sum(k for k in range(len(areas)))),'best rate = '+ "%.3f"% bestrate)
    plt.savefig(savedir+'/record.png',bbox_inches='tight', pad_inches=0.3)
    plt.close('all')

master = Tk()
master.title("Hw 1")


Label(master,text="Data File name : ").grid(row=0)
Label(master,text="Save folder name : ").grid(row=1)
Button(master,text='Read',command=read).grid(row=2,column=1, sticky=W,pady=4)

e=[Entry]*6

e[0]=Entry(master)
e[1]=Entry(master)

e[0].grid(row=0,column=1)
e[1].grid(row=1,column=1)

Button(master,text='Quit',command=master.quit,fg="red").grid(row=100,column=1,sticky=W,pady=4)

mainloop()

