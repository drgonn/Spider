#!/usr/bin/env python3
# -*- coding=UTF-8 -*-

import codecs
#这种方法可以指定一个编码打开文件，使用这个方法打开的文件读取返回的将是unicode。写入时，如果参数是unicode，则使用open()时指定的编码进行编码后写入；如果是str，则先根据源代码文件声明的字符编码，解码成unicode后再进行前述操作。相对内置的open()来说，这个方法比较不容易在编码上出现问题。
import time


class DataOutput(object):
    def __init__(self):
        self.filepath = 'baike_%s.html'%(time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime()))
        self.output_head(self.filepath)
        self.datas=[]
    def store_data(self,data):
        if data is None:
            return
        self.datas.append(data)
        if len(self.datas)>10:
            self.output_html(self.filepath)

    def output_head(self,path):
        fout=codecs.open(path,'w',encoding='utf-8')
        fout.write('<html>')
        fout.write('<head><meta charset="UTF-8"></head>')
        fout.write('<body>')
        fout.write('<table>')
        fout.close()

    def output_html(self,path):
        fout=codecs.open('baike.html','a',encoding='utf-8')
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>"%data['url'])
            fout.write("<td>%s</td>"%data['title'])
            fout.write("<td>%s</td>"%data['summary'])
            fout.write("</tr>")
            self.datas.remove(data)
        fout.close()

    def output_end(self,path):
        fout=codecs.open(path,'a',encoding='utf-8')
        fout.write('</table>')
        fout.write('</body>')
        fout.write('</html>')
        fout.close()