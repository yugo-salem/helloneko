#!/usr/bin/env python
# encoding: utf-8


BLINK = '\x1b[5m'
BOLD = '\x1b[1m'
BG_DARK = '\x1b[100m'
WHITE = '\x1b[97m'
MAGENTA = '\x1b[35m'
LIGHT_MAGENTA = '\x1b[105m'
NORMAL = '\x1b[0m\x1b[39m\x1b[49m'
NAME = 'nekochan777'

def convtohex(val):
    tmpval=ord(val)
    tmpstr="%02X "%tmpval
    return tmpstr


def tstfunc2(val,val2=3,*bbb):
    print("tstfunc_b")
    print(val)
    print(val2)
    if len(bbb)>0:
        print(bbb[0])
    print("tstfunc_e")
    return

def main():
    tstfunc2(1)
    tstfunc2(1,2)
    tstfunc2(1,2,3)
    print(''.join([BG_DARK, BOLD, WHITE,
                   'Hello', ' ', BLINK,
                   MAGENTA, NAME, NORMAL]))


    print(''.join([LIGHT_MAGENTA, WHITE, BOLD,
                   ' nekochan + yugo-salem = love <3  NYA!',
                   NORMAL]))

    print(''.join([LIGHT_MAGENTA, WHITE, BOLD,
                   'i wanna be cute nekogirl for my boyfriend yugo-salem !',
                   NORMAL]))

    print('test print')
    print('test print2')

    bbb='teststring'

    print(bbb[1:][:3])

    nnn=0x1a
    mmm=4
    ggg=nnn<<mmm
    str1="%03X" % ggg
    print(str1)

    arr=(6,5,4,3,2,1)
    print(arr[0])

    if mmm==4:
        print("tada!")
    else:
        print("bada!")

    i=0
    while i<5:
        print("i=%03d"%i)
        i=i+1

    for i in range(2,6):
        print(i)



    tmpf=open("aaa","w");
    tmpf.write("testhex\n")

    tmpf2=open(".gitignore","rb");
    while True:
        tmpbuf=tmpf2.read(16);
        buflen=len(tmpbuf)
        if buflen==0:
            break
        tmpstr3=""
        i=0
        while i<buflen:
            #fgh=ord(tmpbuf[i])
            #tmpstr2="%02X "%fgh
            tmpstr2=convtohex(tmpbuf[i])
            tmpstr3=tmpstr3+tmpstr2
            #print("buf[%d]="%i+tmpstr2)
            i=i+1
        tmpstr4="len=%d  "%buflen+tmpstr3
        #print(tmpstr4)
        tmpf.write(tmpstr4+"\n")
    tmpf2.close()
    tmpf.close()


if __name__ == '__main__':
    main()
