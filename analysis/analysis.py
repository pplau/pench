# coding: utf-8

import sys
sys.path.append('/root/pench')

import paramiko
import threading
import os
import re


class Analysis :

	def __init__(self, conf):
		#self.data_path = conf['data_path']
		self.node_list = conf['node_list']
		self.osd_device = conf['osd_device']
		self.io_openfile_list = []
		self.vm_openfile_list = []
		self.__prepare_data__()


	def __prepare_data__(self):	
		#os.system('cd /root/pench/data')
		for node in self.node_list:
			path = '/root/data/'
			os.system('mkdir '+path)

			t = paramiko.Transport(sock=(node, 22))
			t.connect(username="root", password="admin123")
			sftp = paramiko.SFTPClient.from_transport(t)
			sftp.get("/root/iostat.out", path+node+".out")
			#sftp.get("/root/vmstat.out", path)
			t.close()

			iofile = open(path+node+".out")
			self.io_openfile_list.append(iofile)
			#vmfile = open(path+'vmstat.out')
			#self.io_openfile_list.append(vmfile)


	def __clean__(self):
		for f in self.io_openfile_list:
			f.close()



	def iostat_analysis(self):
		iostat_res = {}
		iostat_res['read_num_count'] = 0
		iostat_res['write_num_count'] = 0
		iostat_res['read_kb_count'] = 0
		iostat_res['write_kb_count'] = 0
		r_wait = []
		w_wait = []

		for f in self.io_openfile_list:
			r_num = 0
			w_num = 0
			r_kb = 0
			w_kb = 0
			for line in f.readlines():
				value_list = re.split(r'\s+', line)
				if value_list[0] == self.osd_device:
					r_num = round(r_num+float(value_list[3]), 2)
					w_num = round(w_num+float(value_list[4]), 2)
					r_kb = round(r_kb+float(value_list[5]) ,2)
					w_kb = round(w_kb+float(value_list[6]), 2)
					#r_wait.append(float(value_list[10]))
					#w_wait.append(float(value_list[11]))
					#iostat_res['read_wait'] = round(sum(r_wait)/len(r_wait), 2)
					#iostat_res['wirte_wait'] = round(sum(w_wait)/len(w_wait), 2)	
			iostat_res['read_num_count'] = iostat_res['read_num_count']+r_num
			iostat_res['write_num_count'] = iostat_res['write_num_count']+w_num
			iostat_res['read_kb_count'] = iostat_res['read_kb_count']+r_kb
			iostat_res['write_kb_count'] = iostat_res['write_kb_count']+w_kb
			
		iostat_res['read_num_count'] = round(iostat_res['read_num_count']/len(self.node_list), 2)
		iostat_res['write_num_count'] = round(iostat_res['write_num_count']/len(self.node_list), 2)
		iostat_res['read_kb_count'] = round(iostat_res['read_kb_count']/len(self.node_list), 2)
		iostat_res['write_kb_count'] = round(iostat_res['write_kb_count']/len(self.node_list), 2)
		return iostat_res

			

	def mem_util(self):
		pass


	def mem_ip(self):
		pass


	def mem_op(self):
		pass








