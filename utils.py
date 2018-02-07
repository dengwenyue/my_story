# -*- coding:utf-8 -*-
import os


def convert(path):
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            num = filename.split(".")[0]
            if num.isdigit():
                new_filename = "第%s章.txt" % num
                os.rename(os.path.join(path, filename), os.path.join(path, new_filename))


def convert_content(path):
    for i in range(1, 1001):
        filename = "第%s章.txt" % i
        filepath = os.path.join(path, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                cont = f.readlines()
                new_cont = cont[1].replace("<br/>", "\n")
            with open(filepath, "w") as f:
                f.write(new_cont)
