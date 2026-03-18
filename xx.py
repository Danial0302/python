import os

print(os.getcwd())          # where we are
os.mkdir("new_folder")      # create folder
print(os.listdir())         # check contents
os.chdir("new_folder")      # go inside
print(os.getcwd())          # new location
os.chdir("..")              # go back
os.rmdir("new_folder")      # delete it