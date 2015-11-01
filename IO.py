#!/usr/bin/python 

import os, sys, os.path 
import shutil

import numpy as np
import pandas as pd

###############################################################################
#--- Input ---
#    CSV format
def readUserData(_dir) :
   _userEntryNames = ['UId', 'Gender', 'Age', 'Occ', 'Zip']
   _fullFileName = '%s/users.dat' % (_dir)

   print 'reading user data file: ', _fullFileName
   _userData = pd.read_csv(_fullFileName, sep='::', names=_userEntryNames, engine='python')
   return _userData
def getUserEntryByID(_UId, _allUsers) :
   print _allUsers[_UId]

#-----------------------------------------------------------------------
def readMovieData(_dir) :
   _movieEntryNames = ['MId', 'Title', 'Genres']
   _fullFileName = '%s/movies.dat' % (_dir)
   print 'reading movie data file: ', _fullFileName
   _movieData = pd.read_csv(_fullFileName, sep='::', names=_movieEntryNames, engine='python')
   return _movieData

#-----------------------------------------------------------------------
def readRatingData(_dir) :
   _ratingEntryNames = ['UId', 'MId', 'Rating', 'TimeStamp']
   _fullFileName = '%s/ratings.dat' % (_dir)
   print 'reading rating data file: ', _fullFileName
   _ratingData = pd.read_csv(_fullFileName, sep='::', names=_ratingEntryNames, engine='python')
   return _ratingData

#-----------------------------------------------------------------------
def writeUserInfo(_user, _overwrite) :
#   UserId     = -1
#   Gender     = ' '
#   Age        = -1
#   Occupation = ' '
#   Zipcode    = -1
   
   _userDir = 'userDB/%i' % (_user.UserId)

   _fullFileName = '%s/UInfo.txt' % (_userDir)
   if (os.path.isdir(_userDir) and not _overwrite) :
      print 'User already exists. Bye!'
#      sys.exit(1)
      return 0
   if (not os.path.isdir(_userDir)) :
      os.makedirs(_userDir)

   if (os.path.exists(_fullFileName) and not _overwrite) :
      print 'User data already exists. Bye!'
      return 0

   _file = open(_fullFileName,'w')
   Uinfo = '%i::%s::%i::%i::%i' % \
           (_user.UserId, _user.Gender,_user.Age, _user.Occupation,\
            int(_user.Zipcode) )
   _file.write(Uinfo)
   _file.close()

   return 1


#-----------------------------------------------------------------------
def updateDataBase(_user) :
#  + copy files (users.dat, movies.dat, ratings.dat)
#    to new directory (userDB)
#  + add new user's (6041) information

   shutil.copy2('ml-1m/users.dat','userDB')

   u_file = open('userDB/users.dat','a')
   Uinfo = '%i::%s::%i::%i::%i\n' % \
           (_user.UserId, _user.Gender,_user.Age, _user.Occupation,\
            int(_user.Zipcode) )
   u_file.write(Uinfo)
   u_file.close()

   shutil.copy2('ml-1m/movies.dat','userDB')

   shutil.copy2('ml-1m/ratings.dat','userDB')
   r_file = open('userDB/ratings.dat','a')

   _ratedMIds = _user.ratedMIds
   _ratedMScs = _user.ratedMScs
   ii = -1
   for _iMovId in _ratedMIds :
      ii = ii + 1
      _iMovSc = _ratedMScs[ii]
      newLine = '%i::%i::%i::999999999\n' % (_user.UserId,_iMovId,_iMovSc)
      r_file.write(newLine)
   r_file.close()




def userExists(_id) :
   _userDir = 'userDB/%i' % (_id)
   if (os.path.isdir(_userDir)) :
      print 'User already exists.'
      return 1
   else :
      return 0

###############################################################################

def decodeRating(_line,_sep) :
#  UId::MId::Rating::TimeStamp
   linesp = _line.strip().split(_sep)
   return int(linesp[0]), int(linesp[1]), int(linesp[2]), long(linesp[3])

def decodeMovie(_line,_sep) :
#  MId::Title
   linesp = _line.strip().split(_sep)
   return int(linesp[0]), linesp[1]


def decodeUser(_line,_sep) :
   print 'decode::User'
   linesp = _line.strip().split(_sep)
   return int(linesp[0]), linesp[1], int(linesp[2]), int(linesp[3]), int(linesp[4])


def decodeHighestRating(_line,_sep='|') :
   linesp = _line.strip().split(_sep)
   return linesp[0], int(linesp[1]), float(linesp[2])


