#!/usr/bin/python 

import os, sys, os.path 
 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#-----------------------------------------------------------------------
from UserClass import *
from MovieClass import *
from IO import *

#-----------------------------------------------------------------------

def getHiRatMovList() :
   hiRaMovies = []
   print 'Getting highest rating movie list'
   hiratFile = open('userDB/highestrating.txt','r')
   freadl = hiratFile.readlines()
   for line in freadl :
      mName, nRat, score = decodeHighestRating(line)
      hiRaMovies.append(mName)
#      print ' add movie ', mName
   return hiRaMovies


def RateMovies(_movList, _userRatFname, _newUser) :
   print '='*30,'\nNow rate some movies ;-)\n','-'*25
   _movieEntryNames = ['MId', 'Title', 'Genres']
   _fullFileName = 'ml-1m/movies.dat'
   print 'reading movie data file: ', _fullFileName
   _movieData = pd.read_csv(_fullFileName, sep='::', names=_movieEntryNames, engine='python', header=None)
   movieDict = _movieData.set_index('Title')['MId'].to_dict()


#TODO check existance
   fRating = open(_userRatFname,'w')



   _ratedMIds = []
   _ratedMScs = []

   for mov in _movList :
      print '*** ', mov
      ok = False
      while not ok :
         answer = raw_input(' --> Your score ([1 to 5], 0 if no answer) ? ')
         _score = -1
         if answer.isdigit() : _score = int(answer)
         if ( _score < 0 or _score > 5 ) :
            print 'answer not valid'
         else :
            ok = True
            fRating.write('%s|%i\n' % (mov,_score))
            _ratedMIds.append(movieDict[mov])
            _ratedMScs.append(_score)
   fRating.close()
   newExtUser = ExtendedUser(_newUser.UserId, _newUser.Gender, _newUser.Age,
                              _newUser.Occupation, _newUser.Zipcode,_ratedMIds,_ratedMScs)
   return newExtUser


if __name__ == "__main__" :

   moviesToRate = getHiRatMovList()

   OVERWRITE = True
   
#FIXME there are already 6040 user in database
   CurrentUserID = 6041

   if (userExists(CurrentUserID)) :
      CONT = raw_input('Overwrite? (Y/N)')
#FIXME login? NO. :-)
      if ( not CONT.upper() == 'Y') :
         print 'Alright. Bye!'
         sys.exit(1)

   CurrentUser = inputUserInfo(CurrentUserID)

   writeUserInfo(CurrentUser,OVERWRITE)
#updateDataBase(CurrentUser)

   userRatingFname = 'userDB/%i/rating.txt' % (CurrentUserID)
   newExtUser = RateMovies(moviesToRate,userRatingFname,CurrentUser)

   updateDataBase(newExtUser)




