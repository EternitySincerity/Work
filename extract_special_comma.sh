#!/bin/bash
date_desc=$1
date1_desc=`date -d "$date_desc -1 day" +%Y%m%d`
date7_desc=`date -d "$date_desc -7 day" +%Y%m%d`
base_dir="/group/user/tools/meta/hive-temp-table/tools.db"

file_pre="/ftp_samba/72/lxc/video_title_"
file_diff="/ftp_samba/72/lxc/video_title_diff_$date_desc"

if [ ! -f "$file_pre$date1_desc" ];
then
	echo '' >"$file_pre$date1_desc";
fi;

if [ ! -f "$file_diff" ];
then
	echo '' >"$file_diff";
fi;

if [ -f "$file_pre$date7_desc" ];
then
	rm -rf "$file_pre$date7_desc"
fi;

tar_file="/ftp_samba/72/lxc/tar_file_${date_desc}.txt"

tmp_tar_file="/ftp_samba/72/lxc/tar_file_${date_desc}.tmp"
echo ''>"$tmp_tar_file"
echo ''>"$file_pre$date_desc"
for v_i in `seq 1 3`
do
	if [ "$v_i" == "1" ];
	then
		source_table="src_swmedia_new_video_source_d"
		hadoop fs -cat $base_dir/$source_table/pt=$date_desc/* | awk -F "\t" '{print "1",$5}' | grep -Evi "^1 $" >"$file_pre$date_desc"
		
	elif [ "$v_i" == "2" ];
	then
		source_table="src_swmedia_new_video_d"
		hadoop fs -cat $base_dir/$source_table/pt=$date_desc/* | awk -F "\t" '{print "2",$4}' | grep -Evi "^2 $" >>"$file_pre$date_desc" 
		hadoop fs -cat $base_dir/$source_table/pt=$date_desc/* | awk -F "\t" '{print "1",$5}' | grep -Evi "^1 $" >>"$file_pre$date_desc"
	elif [ "$v_i" == "3" ];
	then
		source_table="dwd_spider_video_info_doban_d"
		hadoop fs -cat $base_dir/$source_table/pt=$date_desc/* | awk -F "\t" '{print "2",$12}' | grep -Evi "^2 $" >>"$file_pre$date_desc"	
	fi;
done;

diff "$file_pre$date_desc" "$file_pre$date1_desc" |grep -E "^<"|sed "s/< //"|sed "s/(/（/" |sed "s/)/）/" >$file_diff

for v_loop_seg in `seq 1 6`
do
	if [ $v_loop_seg == "1" ];
	then
		v_b_seg="《";
		v_e_seg="》";
		v_b_sed=$v_b_seg
		v_e_sed=$v_e_seg
		cat $file_diff|grep -Eo "${v_b_seg}[^${v_e_seg}]*${v_e_seg}" | sed "s/${v_b_sed}//"|sed "s/${v_e_sed}//" |awk '{print toupper($0)}' >>$tmp_tar_file;
	elif [ $v_loop_seg == "2" ];
	then
		v_b_seg="【";
		v_e_seg="】";
		v_b_sed=$v_b_seg
		v_e_sed=$v_e_seg
		cat $file_diff|grep -Eo "[$v_b_seg$v_e_seg]"|grep -Eo "^[^$v_b_seg$v_e_seg]*" | sed "s/${v_b_sed}//"|sed "s/${v_e_sed}//" |awk '{print toupper($0)}' >>$tmp_tar_file;
	elif [ $v_loop_seg == "3" ];
	then
		v_b_seg="“";
		v_e_seg="”";
		v_b_sed=$v_b_seg
		v_e_sed=$v_e_seg
		cat $file_diff|grep -Eo "^1 .*$"|grep -Eo "${v_b_seg}[^${v_e_seg}]*${v_e_seg}" | sed "s/${v_b_sed}//"|sed "s/${v_e_sed}//" |awk '{print toupper($0)}' >>$tmp_tar_file;
	elif [ $v_loop_seg == "4" ];
	then
		v_b_seg="（";
		v_e_seg="）";
		v_b_sed=$v_b_seg
		v_e_sed=$v_e_seg
		cat $file_diff|grep -Eo "${v_b_seg}[^${v_e_seg}]*${v_e_seg}" | sed "s/${v_b_sed}//"|sed "s/${v_e_sed}//"| grep -Eo ".*饰\s?$" |awk '{print toupper($0)}' >>$tmp_tar_file;
	elif [ $v_loop_seg == "5" ];
	then
		v_b_seg="\\(";
		v_e_seg="\\)";
		v_b_sed="(";
		v_e_sed=")";
		cat $file_diff|grep -Eo "${v_b_seg}[^${v_e_seg}]*${v_e_seg}" | sed "s/${v_b_sed}//"|sed "s/${v_e_sed}//"| grep -Eo ".*饰\s?$" |awk '{print toupper($0)}' >>$tmp_tar_file;
	elif [ $v_loop_seg == "6" ];
	then
		v_b_seg="\\[";
		v_e_seg="\\]";
		v_b_sed=$v_b_seg
		v_e_sed=$v_e_seg
		cat $file_diff|grep -Eo "${v_b_seg}[^${v_e_seg}]*${v_e_seg}" | sed "s/${v_b_sed}//"|sed "s/${v_e_sed}//" |awk '{print toupper($0)}' >>$tmp_tar_file;
	fi;
	
done;

for v_loop_seg in `seq 1 1` 
do
	v_filter="0"
	if [ $v_loop_seg == "1" ];
	then
		v_seg="#";
		v_filter="1"
	elif [ $v_loop_seg == "2" ];
	then
		v_seg="\\\"";
		v_filter="1"
	elif [ $v_loop_seg == "3" ];
	then
		v_seg="&";		
		v_filter="1"
	elif [ $v_loop_seg == "4" ];
	then
		v_seg="\$";		
		v_filter="1"
	fi;
	
	v_seg_reg=$v_seg
	if [ $v_loop_seg == "4" ];
	then
		v_seg_reg="\\\\\\\$";
	elif [ $v_loop_seg == "2" ];
	then
		v_seg_reg="\\\\\\\"";
	fi;
	
	cat $file_diff|grep -Eo "^1 .*$"|awk -F"${v_seg}" '{if(NF%2==1) print toupper($0)}'|awk -F"${v_seg}" -vOFS= '{for(i=0;i<=NF;i+=2) print $i}'|grep -Eo "^${v_seg_reg}+|(${v_seg_reg})[^${v_seg}]*${v_seg_reg}"| sed "s/${v_seg_reg}//g">>$tmp_tar_file;
	
done;

cat $tmp_tar_file| sort -k1| uniq >$tar_file

