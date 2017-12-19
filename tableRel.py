import string;
import os;

ofile=open("E:\\s_dwd_xsvip_recom_qw_operate_d.sql",encoding="utf8")

for i in ofile.readlines():
    if i.__contains__("insert") or i.__contains__("from") or i.__contains__("join") :
        print(i)