# -*- coding: utf-8 -*-
# author: itimor

a = '''cing elit
3. Integer molestie lorem at massa


1. You can use sequential numbers...
1. ...or keep all the numbers as `1.`
'''


def finding_nemo(String, Substr, times):
    String_list = String.split(Substr, times)
    nemo = len(String) - len(String_list[-1]) - 1
    return nemo


b = finding_nemo(a, '\n', 3)
print(b)