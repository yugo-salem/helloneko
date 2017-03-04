#!/usr/bin/env python
# encoding: utf-8


str="teststring123"

str2="";
strlen=len(str)
print(strlen)
i=0;
while i<strlen:
    str2=str2+str[strlen-1-i]
    i=i+1

print(str)
print(str2)
