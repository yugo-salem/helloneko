#!/usr/bin/env python
# encoding: utf-8


str="teststring123"

str2="";
strlen=len(str)
print(strlen)

#i=0;
#while i<strlen:
#    str2=str2+str[strlen-1-i]
#    i=i+1

#for i in range(strlen):
#    str2=str2+str[strlen-1-i]

#for le in str[::-1]:
#    str2=str2+le

li1=list(str)

li2=li1[::-1]

str2=''.join(li2)

print(str)
print(str2)
