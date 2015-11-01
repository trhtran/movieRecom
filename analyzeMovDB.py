#!/usr/bin/python 
###############################################################################
#  Data: Movielens
#    http://grouplens.org/datasets/movielens/
#      1 million ratings, 6000 users on 4000 movies
#      released 2/2003
#
#    suggested by:
#      http://www.analyticsvidhya.com/blog/2014/11/data-science-projects-learn/
#
#  Example of analyses inspired from
#    http://www.gregreda.com/2013/10/26/using-pandas-on-the-movielens-dataset/
#    /!\ Data formats are different
#
###############################################################################
import os, sys, os.path 
 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ggplot import *

#-----------------------------------------------------------------------
from UserClass import *
from MovieClass import *
from IO import *

#-----------------------------------------------------------------------
allGenres = []

def getAllGenres(_data) :
   cols = _data['Genres']
   fGenres = open('userDB/genres.txt','w')
   for col in cols :
      genresOneMovie = col.split('|')
      NG = len(genresOneMovie)
      for ig in range(0,NG) :
         if (not genresOneMovie[ig] in allGenres) :
            allGenres.append(genresOneMovie[ig])
            fGenres.write('%s\n'%(genresOneMovie[ig]))
   fGenres.close()



###############################################################################
#--- analyzing ---
#TODO 
# average rating mean by year & by gender & by age
# define new column: year
# rating by timestamp
            
def analyzeRatings(_data) :
   print '*'*80,'\n Analyzing rating data\n','*'*80
   plt.figure()
   _data.TimeStamp.hist(bins=30)
   plt.title('Rating time since the epoch')
   plt.xlabel('time [sec]')
   plt.savefig('plots/rating.time.eps',format='EPS')
   
def analyzeUsers(_data) :
 
   cmap = plt.get_cmap('Set3')
   colors = [cmap(i/5.) for i in range(5)]

   print '*'*80,'\n Analyzing user data\n','*'*80
   plt.figure(0)
   _data.Age.hist(color=colors[1],bins=[0,18,25,35,45,50,56,70],alpha=0.7,linewidth=0.5)
   _data[_data.Gender=='M'].Age.hist(color=colors[4],bins=[0,18,25,35,45,50,56,70],alpha=0.4,linewidth=0.5)
   _data[_data.Gender=='F'].Age.hist(color=colors[2],bins=[0,18,25,35,45,50,56,70],alpha=0.4,linewidth=0.5)
   plt.title("Users' ages distribution")
   plt.xlabel('Age [year]')
   plt.ylabel('Nb of users')
   plt.tight_layout(h_pad=9.0)
#   plt.show()
   plt.savefig('plots/user.age.eps', format='EPS')


def analyzeMovies(_data) :
   print '*'*80,'\n Analyzing movie data\n','*'*80
#   most_rated = _data.groupby('Title').size().order(ascending=False)[:25]
   most_rated = _data.groupby('Title').size().sort_values(ascending=False)[:25]
   print 'Most rated movies:', most_rated

# 50 most rated movies
#   most_50 = _data.groupby('MId').size().order(ascending=False)[:50]
   most_50 = _data.groupby('MId').size().sort_values(ascending=False)[:50]

   print '\nHighly rated movies (by nb of ratings):'
   movie_stats = _data.groupby('Title').agg({'Rating': [np.size, np.mean]})
   print movie_stats.head(10)

   print '\nSort by highest average score'
#deprecated   print movie_stats.sort([('Rating','mean')], ascending=False).head()
   rated_mov_stats = movie_stats.sort_values(by=[('Rating','mean')], ascending=False).head()
   print rated_mov_stats


   print '\nHighest average score with more than 100 ratings: TOP 15'
   atleast100 = movie_stats['Rating']['size'] >= 100
#deprecated   sortedAtleast100 = movie_stats[atleast100].sort([('Rating','mean')], ascending=False)[:15]
   sortedAtleast100 = movie_stats[atleast100].sort_values(by=[('Rating','mean')], ascending=False)[:15]
   sortedAtleast100All = movie_stats[atleast100].sort_values(by=[('Rating','mean')], ascending=False)
   print sortedAtleast100
   sortedAtleast100.to_csv('userDB/highest.rating.txt',sep='|',header=False)


   print '\nRating by age'
   MeanByAge = _data.groupby('Age').agg({'Rating':[np.size, np.mean, np.std]})
   print MeanByAge

   print '\nRating by age by movie'
   MeanByAgeByMov = _data.ix[most_50.index].groupby(['Title','Age'])
   print MeanByAgeByMov.Rating.mean().head(15)

   print '_'*60,'\ngroup by GENRE','.'*60,'\n'

   _data.reset_index('MId',inplace=True)
   pivoted = _data.pivot_table(index=['MId','Title'], columns=['Gender'],values='Rating',fill_value=0)
   print pivoted.head(20)

   print '\nDifference rating Female/Male'
   pivoted['diff'] = pivoted.M - pivoted.F
   print pivoted.head()

   pivoted.reset_index('MId',inplace=True)
   diffMF = pivoted[pivoted.MId.isin(most_50.index)]['diff']
   plt.figure(2)
   diffMF.order().plot(kind='barh',figsize=[15,15])
   plt.title('Male vs. Female Avg. Ratings\n(Difference > 0 = Favored by Men)')
   plt.ylabel('Title')
   plt.xlabel('Average Rating Difference')
   plt.savefig('plots/diff.Female.Male.eps',format='EPS')
#plt.tight_layout(h_pad=0.1)
   plt.autoscale(True,'both',tight=None)


   byTitle = _data.groupby('Title')
   print byTitle.head(100)


#   for group_name, _data in _data.groupby('Title') :
#      newdf = process(df)
#      with open('all.txt','a') as f :
#         df.to_csv(f)

#   with open('all.txt','w',encoding='utf-8') as outfile :
#      print (byTitle, file=outfile)
#byTitle.to_csv('all.bytitle.txt',sep='|')

#   print '_'*80,'\n'
#   ratings_count = _data.groupby('Title').size()
#   print 'RATINGS COUNT: ',len(ratings_count.index[ratings_count>250])
#   mean_ratings = _data.pivot_table('Rating',index=['Genres'],columns='Gender',aggfunc='mean')
#   for genre in allGenres :
#      print '_'*10,'\nGENRE:', genre, '\n','-'*10
#      ratingInGenre = _data.groupby(by=[lambda genre: genre in _data.Genres])
#      print ratingInGenre.head(10)
#
#   print 'MEAN RATING: '
#   print mean_ratings.head(100)
#
#   sys.exit()
#
#   temp=_data.pivot_table('Rating',index=['Title'],columns='Gender',aggfunc='count')
#   topGenre = mean_ratings[ratings_count>100].sort_index(by='Animation',ascending=False)[:10]
#
#   print topGenre


#   print '\nHighest rated by female'
#   highRating_F = sortedAtleast100.sort_values(by='F',ascending=False)
#   print highRating_F[:10]

###############################################################################
#--- MAIN FUNCTION ---
###############################################################################
def main() :
   print 'Movie analyzer'

   nargs = len(sys.argv) - 1
# default dataset: 1M ratings
   _DataTag = '1m'
   if (nargs > 0) :
      _DataTag = sys.argv[1]


   DataDir = 'ml-%s' % (_DataTag)
   print 'Directory for data: ', DataDir

#===================
#   readFiles(DataDir)
   userData   = readUserData  (DataDir)
   movieData  = readMovieData (DataDir)
   ratingData = readRatingData(DataDir)
   MovRat  = pd.merge(movieData, ratingData)
   allData = pd.merge(MovRat, userData)

#===================

   getAllGenres(movieData)

   analyzeRatings(ratingData)
   analyzeUsers(userData)
   analyzeMovies(allData)



#   CurrentUser = inputUserInfo()
# #--suppose that user already exists in database----
#    currentUserID = -1
#    currentUserID = int(raw_input('Please enter your user ID: ')) #FIXME : control User Id
# 
#    print 'Your user information:'
#    print userData[userData.UId == currentUserID].head()

#   print 'GENRES: ', allGenres

if __name__=="__main__": 
 main() 
    
