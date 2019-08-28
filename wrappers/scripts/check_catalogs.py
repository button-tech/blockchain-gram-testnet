#!/usr/bin/env python3
import os
import sys 

os.chdir(sys.argv[1])

catalogs = os.listdir()

j = 0

bad_catalogs = []

for i in catalogs:
           if i == ".DS_Store":
               continue
           os.chdir(i)
           inside = os.listdir()
           if(len(inside)) != 3:
               print(i)
               bad_catalogs.append(i)
               j+=1 
           os.chdir("../")

print(f'Bad catalogs:{len(bad_catalogs)}')

if len(bad_catalogs) > 0:
# clean catalogs
        for i in bad_catalogs:
            os.system(f"rm -r {i}")
        print("clean all!")
else:
    print("In all catalogs 3 files")        