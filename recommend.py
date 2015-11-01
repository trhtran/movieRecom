#!/usr/bin/python 

import os, sys, os.path 
 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from ggplot import *

import argparse

#-----------------------------------------------------------------------
from UserClass import *
from MovieClass import *
from IO import *

OFFLINE = 0
ONLINE = 1

#####################
def get_error(Q, X, Y, W) :
   return np.sum((W * (Q - np.dot(X, Y)))**2)


def readNewUserInfo(_UId,_movieDict) :
   print 'readNewUserInfo, Id:%i' %(_UId)
   UInfoFname = 'userDB/%i/UInfo.txt' % (_UId)
   UInfoFile = open(UInfoFname,'r')
   UInfoLine = UInfoFile.readline()
   print UInfoLine

   _UId,_gender,_age,_occ,_zip = decodeUser(UInfoLine,'::')

   URatingFname = 'userDB/%i/rating.txt' % (_UId)
   URatingFile = open(URatingFname,'r')
   fRdl = URatingFile.readlines()

   _ratedMIds = []
   _ratedMScs = []

   for line in fRdl :
#      print line
      linesp=line.strip().split('|')
      _currMovieTitle = linesp[0]
      _currMovieScore = linesp[1]
      _currMovieId = _movieDict[_currMovieTitle]
      print 'MOVIE ID: ', _currMovieId
      _ratedMIds.append(_currMovieId)
      _ratedMScs.append(_currMovieScore)

   newUser = ExtendedUser(_UId,_gender,_age,_occ,_zip,_ratedMIds,_ratedMScs)
   return newUser


def print_recommendations_All(W, Q, Q_hat, movie_titles,m):
# --- m = nb of users
    #Q_hat -= np.min(Q_hat)
    #Q_hat[Q_hat < 1] *= 5
    Q_hat -= np.min(Q_hat)
    Q_hat *= float(5) / np.max(Q_hat)
    movie_ids = np.argmax(Q_hat - 5 * W, axis=1)
    for jj, movie_id in zip(range(m), movie_ids):
        #if Q_hat[jj, movie_id] < 0.1: continue
        print('User {} liked {}\n'.format(jj + 1, ', '.join([movie_titles[ii] for ii, qq in enumerate(Q[jj]) if qq > 3])))
        print('User {} did not like {}\n'.format(jj + 1, ', '.join([movie_titles[ii] for ii, qq in enumerate(Q[jj]) if qq < 3 and qq != 0])))
        print('\n User {} recommended movie is {} - with predicted rating: {}'.format(
                    jj + 1, movie_titles[movie_id], Q_hat[jj, movie_id]))
        print('\n' + 100 *  '-' + '\n')

#####################
def print_recommendations_newUser(W, Q, Q_hat, movie_titles,newUser):
    #Q_hat -= np.min(Q_hat)
    #Q_hat[Q_hat < 1] *= 5
    Q_hat -= np.min(Q_hat)
    Q_hat *= float(5) / np.max(Q_hat)
    movie_ids = np.argmax(Q_hat - 5 * W, axis=1)
    print 'movie_ids: ', movie_ids
    jj = newUser.UserId-1
#    for jj, movie_id in zip(range(m), movie_ids):
    for movie_id in movie_ids:
        #if Q_hat[jj, movie_id] < 0.1: continue
        print('User {} liked {}\n'.format(jj + 1, ', '.join([movie_titles[ii] for ii, qq in enumerate(Q[jj]) if qq > 3])))
        print('User {} did not like {}\n'.format(jj + 1, ', '.join([movie_titles[ii] for ii, qq in enumerate(Q[jj]) if qq < 3 and qq != 0])))
        print('\n User {} recommended movie is {} - with predicted rating: {}'.format(
                    jj + 1, movie_titles[movie_id], Q_hat[jj, movie_id]))
        print('\n' + 100 *  '-' + '\n')

#####################

def main() :

   _DataTag = '1m'
   _recommendMode = OFFLINE

   parser = argparse.ArgumentParser(description='input variables: nb ratings, mode for recommendation: online/offline')
   parser.add_argument('-t', '--tags', nargs='?', type=str, required=False,help='Nb of ratings')
   parser.add_argument('-m', '--mode', nargs='?', type=int, required=False,help='Recommendation mode [0/1]')

   try :
      _optList = vars(parser.parse_args())
   except :
      error(1, 'option argument error')
   if (_optList['tags'] ) :
      _DataTag = _optList['tags']
   if (_optList['mode'] ) :
      _recommendMode = _optList['mode']


   print '_DataTag: ', _DataTag
   print '_recommendMode: ', _recommendMode


   DataDir = 'ml-%s' % (_DataTag)
   if _recommendMode == ONLINE :
      DataDir = 'userDB'
   print 'Directory for data: ', DataDir

#------------- end of argument processing -----------

#--- now input files --------
   _userEntryNames = ['UId', 'Gender', 'Age', 'Occ', 'Zip']
   _fullFileName = '%s/users.dat' % (DataDir)
   print 'reading user data file: ', _fullFileName
   _userData = pd.read_csv(_fullFileName, sep='::', names=_userEntryNames, engine='python', header=None)

   print 'USERDATA:\n', _userData, '\n </USERDATA>'


   _movieEntryNames = ['MId', 'Title', 'Genres']
   _fullFileName = '%s/movies.dat' % (DataDir)
   print 'reading movie data file: ', _fullFileName
   _movieData = pd.read_csv(_fullFileName, sep='::', names=_movieEntryNames, engine='python', header=None)


   _ratingEntryNames = ['UId', 'MId', 'Rating', 'TimeStamp']
   _fullFileName = '%s/ratings.dat' % (DataDir)
   print 'reading rating data file: ', _fullFileName
   _ratingData = pd.read_csv(_fullFileName, sep='::', names=_ratingEntryNames, engine='python', header=None)

   movieTitles = _movieData.Title.tolist()
   movieIds = _movieData.MId.tolist()

#   movieDict = _movieData.set_index('MId')['Title'].to_dict()
   movieDict = _movieData.set_index('Title')['MId'].to_dict()
   print movieDict
   print '_'*200

#   newUser = ExtendedUser()
   if _recommendMode == ONLINE :
      newUser = readNewUserInfo(6041,movieDict)




   print _movieData.head()
   print _movieData
#   print movieTitles

#   MR = _movieData.join(_ratingData, on=['MId'],rsuffix='_r')
#   UMR = MR.join(_userData, on=['UId'],rsuffix='_t')
#    del UMR['MId_r']
#    del UMR['UId_t']
# #   del UMR['MId_t']
# #   del UMR['TimeStamp_t']

   MR = _movieData.merge(_ratingData)
   UMR = MR.merge(_userData)

   print 'MR:\n',MR

   print 'UMR:::::::::::::::::\n',UMR
   print UMR.head()


#   pivoted = UMR.pivot_table(cols='MId',rows='UId',values='Rating')
   pivoted = UMR.pivot_table(index='UId',columns='MId',values='Rating')
   print pivoted.head(20)


   pivoted = pivoted.fillna(0)
   print pivoted.head()

   Q = pivoted.values
   print Q
   print Q.shape

   W = Q>0.5
   W[W == True ] = 1
   W[W == False] = 0
   W = W.astype(np.float64, copy=False)
   print '-'*20,'\n Printing W\n',W,'\n','-'*20


   lambda_ = 0.1
   n_factors = 5 #100
   m, n = Q.shape #XXX m: nb of users, n: nb of movies

   n_iterations = 10

   X = 5 * np.random.rand(m, n_factors)
   Y = 5 * np.random.rand(n_factors, n)

   errors = []
   for ii in range(n_iterations) :
      X = np.linalg.solve(np.dot(Y, Y.T) + lambda_ * np.eye(n_factors),
            np.dot(Y, Q.T)).T
      Y = np.linalg.solve(np.dot(X.T, X) + lambda_ * np.eye(n_factors),
            np.dot(X.T, Q))
      if (ii % 5 == 0) :
         print '%ith iteration done.' % (ii)
      errors.append(get_error(Q, X, Y, W))
   Q_hat = np.dot(X, Y)
   print 'Error of rated movies' % (get_error(Q, X, Y, W))
   print('Error of rated movies: {}'.format(get_error(Q, X, Y, W)))


   plt.figure(0)
   plt.plot(errors)
   plt.ylim([0, 20000])
   plt.savefig('plots/errors.eps',format='EPS')

   if _recommendMode == OFFLINE :
      print_recommendations_All(W,Q,Q_hat,movieTitles,m)
   else :
      print_recommendations_newUser(W,Q,Q_hat,movieTitles,newUser)




#===  weighted errors  ===
   print '='*30,'\nUSING WEIGHTED ERRORS\n','='*30,'\n'
   plt.figure(1)
   weighted_errors = []
   for ii in range(n_iterations):
      print 'ii: ', ii
      for u, Wu in enumerate(W):
         print 'u, Wu: ', u, ' ', Wu
         X[u] = np.linalg.solve(np.dot(Y, np.dot(np.diag(Wu), Y.T)) + lambda_ * np.eye(n_factors),
               np.dot(Y, np.dot(np.diag(Wu), Q[u].T))).T
      for i, Wi in enumerate(W.T):
         Y[:,i] = np.linalg.solve(np.dot(X.T, np.dot(np.diag(Wi), X)) + lambda_ * np.eye(n_factors),
               np.dot(X.T, np.dot(np.diag(Wi), Q[:, i])))
      weighted_errors.append(get_error(Q, X, Y, W))
      print('{}th iteration is completed'.format(ii))
   weighted_Q_hat = np.dot(X,Y)

   plt.plot(weighted_errors)
   plt.savefig('plots/errors.weighted.eps',format='EPS')

#   print_recommendations_All(W,Q,weighted_Q_hat,movieTitles,m)
   if _recommendMode == OFFLINE :
      print_recommendations_All(W,Q,weighted_Q_hat,movieTitles,m)
   else :
      print_recommendations_newUser(W,Q,weighted_Q_hat,movieTitles,newUser)



#   ExtUser = ExtendedUser()



#####################
if __name__=="__main__": 
    main() 
 
