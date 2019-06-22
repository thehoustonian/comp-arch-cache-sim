#!/usr/bin/python
import sys, os, string, re;
import shutil;


tests = ['-l1-usize 1024 -l1-ubsize 32 -l1-uassoc 1 -l1-uwalloc n  -l1-urepl f ',
		 '-l1-usize 1024 -l1-ubsize 32 -l1-uassoc 4 -l1-uwalloc n  -l1-urepl f ',
		 '-l1-usize 1024 -l1-ubsize 32 -l1-uassoc 32 -l1-uwalloc n  -l1-urepl f ',
		 '-l1-usize 1024 -l1-ubsize 32 -l1-uassoc 1 -l1-uwalloc a  -l1-urepl f ',
		 '-l1-usize 1024 -l1-ubsize 32 -l1-uassoc 4 -l1-uwalloc a  -l1-urepl f ',
		 '-l1-usize 1024 -l1-ubsize 32 -l1-uassoc 32 -l1-uwalloc a  -l1-urepl f ',
		 '-l1-usize 1024 -l1-ubsize 32 -l1-uassoc 1 -l1-uwalloc n  -l1-urepl l ',
		 '-l1-usize 1024 -l1-ubsize 32 -l1-uassoc 4 -l1-uwalloc n  -l1-urepl l ',
		 '-l1-usize 1024 -l1-ubsize 32 -l1-uassoc 32 -l1-uwalloc n  -l1-urepl l ',
		 '-l1-usize 1024 -l1-ubsize 32 -l1-uassoc 1 -l1-uwalloc a  -l1-urepl l ',
		 '-l1-usize 1024 -l1-ubsize 32 -l1-uassoc 4 -l1-uwalloc a  -l1-urepl l ',
		 '-l1-usize 1024 -l1-ubsize 32 -l1-uassoc 32 -l1-uwalloc a  -l1-urepl l ']

def doCmd(command):
	print command
	sys.stdout.flush()
	status = os.system(command)
	if (status != 0):
		print "Error, command failed: ",command,"\n"
		sys.exit(-1)
		
	
def parseMisses(logfile):
	try:
		infile = open(logfile,'r')
	except:
		print "Cannot open file: ",logfile
		return 0
	
	misses = 0
	for line in infile.readlines():
		words = line.split()
		if (len(words) < 2):
			continue
		if (words[1] == 'Misses'):
			misses = int(words[2])
			break
	
	infile.close()
	return misses
	
def copyLog(src,dst,count):
	try:
		infile = open(src,'r')
	except:
		print "Cannot open file: ",src
		return 0
	try:
		if (count == 0):
			outfile = open(dst,'w')
		else:
			outfile = open(dst,'a')
	except:
		print "Cannot open file: ",dst
		return 0
	for line in infile.readlines():
		outfile.write(line)
	infile.close()
	outfile.close()
	return


if (len (sys.argv) < 4):
	print "Usage: sys.argv[0] goldProgram yourProgram  trace_file"
	sys.exit(-1)
	

goldPgm = sys.argv[1]
yourPgm = sys.argv[2]
trace_file = sys.argv[3]

results = []
logfile = 'run.log'

logall = 'goldAll.log'

fails = 0
count = 0
for test in tests:
	if (goldPgm == 'dineroIV'):
		cmd = goldPgm + ' ' + test + '-informat d < ' + trace_file + ' > ' + logfile
	else:
		cmd = goldPgm + ' ' + trace_file + ' '+ test + ' > ' + logfile
	doCmd(cmd)
	goldMisses = parseMisses(logfile)
	copyLog(logfile,logall,count)
	
	cmd = yourPgm + ' ' + trace_file + ' '+ test + ' > ' + logfile
	doCmd(cmd)
	yourMisses = parseMisses(logfile)
	if (goldMisses != yourMisses):
		fails += 1
		result = 'Gold Misses: %d, Your Misses: %d, Test: %s' % (goldMisses, yourMisses, test)
		results.append(result)
	count += 1

if (fails == 0):
	print "All tests passed!!"
else:
	print "There were ",fails, " failures"
	print "The following tests failed:"
	for test in results:
		print test
		
	
	
