#!/usr/bin/env python

import sys
import os
from subprocess import *

if len(sys.argv) <= 1:
  print('Usage: {0} training_file [testing_file]'.format(sys.argv[0]))
  raise SystemExit

# svm, grid, and gnuplot executable files

is_win32 = (sys.platform == 'win32')
if not is_win32:
  svmscale_exe = "/Users/sun/prog/libsvm/svm-scale"
#  svmtrain_exe = "svm-train"
#  svmpredict_exe = "svm-predict"
  svmtrain_exe = "/Users/sun/prog/libsvm/binary-train"
  svmpredict_exe = "/Users/sun/prog/libsvm/binary-predict"
#  binarytrain_exe = "binary-train"
#  binarypredict_exe = "binary-predict"
  grid_py = "/Users/sun/prog/libsvm/tools/grid.py"
  gnuplot_exe = "/opt/local/bin/gnuplot"
else:
        # example for windows
  svmscale_exe = r"..\windows\svm-scale.exe"
  svmtrain_exe = r"..\windows\svm-train.exe"
  svmpredict_exe = r"..\windows\svm-predict.exe"
  gnuplot_exe = r"c:\tmp\gnuplot\bin\pgnuplot.exe"
  grid_py = r".\grid.py"

assert os.path.exists(svmscale_exe),"svm-scale executable not found"
assert os.path.exists(svmtrain_exe),"svm-train executable not found"
assert os.path.exists(svmpredict_exe),"svm-predict executable not found"
assert os.path.exists(gnuplot_exe),"gnuplot executable not found"
assert os.path.exists(grid_py),"grid.py not found"

train_pathname = sys.argv[1]
assert os.path.exists(train_pathname),"training file not found"
file_name = os.path.split(train_pathname)[1]
scaled_file = file_name
model_file = file_name + ".model"
range_file = file_name + ".range"
predict_train_file = file_name + ".predict"

if len(sys.argv) > 2:
  test_pathname = sys.argv[2]
  file_name = os.path.split(test_pathname)[1]
  assert os.path.exists(test_pathname),"testing file not found"
  scaled_test_file = file_name
  predict_test_file = file_name + ".predict"

#cmd = '{0} -l 0 -u 1 -s "{1}" "{2}" > "{3}"'.format(svmscale_exe, range_file, train_pathname, scaled_file)
#print( cmd )
#print('Scaling training data...')
#Popen(cmd, shell = True, stdout = PIPE).communicate() 

#cmd = '{0} -s 0 -t 5 -m 2000 -log2g 0,1,1 -svmtrain "{1}" -gnuplot "{2}" "{3}"'.format(grid_py, svmtrain_exe, gnuplot_exe, scaled_file)
cmd = '{0} -s 0 -t 5 -m 2000 -log2c -5,9,2 -log2g 1,1,1 -svmtrain "{1}" -gnuplot "{2}" "{3}"'.format(grid_py, svmtrain_exe, gnuplot_exe, scaled_file)
print( cmd )
print('Cross validation...')
f = Popen(cmd, shell = True, stdout = PIPE).stdout
  
line = ''
while True:
  last_line = line
  line = f.readline()
  print( line )
  if not line: break
c,g,rate = map(float,last_line.split())

print('Best c={0}, g={1} CV rate={2}'.format(c,g,rate))

#predict training file with 5-fold cross validation
cmd = '{0} -v 5 -s 0 -t 5 -w1 15 -w-1 1 -m 2000 -c {1} -g {2} "{3}" "{4}"'.format(svmtrain_exe,c,g,scaled_file,model_file)
print( cmd )
print('Cross validation...~/binary_class_cross_valdation.dat')
g=Popen(cmd, shell = True, stdout = PIPE).communicate()
print( g )

# model training
cmd = '{0} -s 0 -t 5 -w1 15 -w-1 1 -m 2000 -c {1} -g {2} "{3}" "{4}"'.format(svmtrain_exe,c,g,scaled_file,model_file)
print( cmd )
print('Training...')
g=Popen(cmd, shell = True, stdout = PIPE).communicate()
print( g )
print('Output model: {0}'.format(model_file))

#cmd = '{0} "{1}" "{2}" "{3}"'.format(binarypredict_exe, scaled_file, model_file, predict_train_file)
#print( cmd )
#print('Testing training file...')
#Popen(cmd, shell = True).communicate()  
#print('Output prediction: {0}'.format(predict_train_file))

#if len(sys.argv) > 2:
#  cmd = '{0} -r "{1}" "{2}" > "{3}"'.format(svmscale_exe, range_file, test_pathname, scaled_test_file)
#  print( cmd )
#  print('Scaling testing data...')
#  Popen(cmd, shell = True, stdout = PIPE).communicate() 

#  cmd = '{0} "{1}" "{2}" "{3}"'.format(svmpredict_exe, scaled_test_file, model_file, predict_test_file)
#  cmd = '{0} "{1}" "{2}" "{3}"'.format(binarypredict_exe, scaled_test_file, model_file, predict_test_file)
#  print( cmd )
#  print('Testing...')
#  Popen(cmd, shell = True).communicate()  

#  print('Output prediction: {0}'.format(predict_test_file))
