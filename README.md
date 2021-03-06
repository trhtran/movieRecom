#Movie recommendation

Package content
===============

Basic input/output functions and classes
----------------------------------------
 * IO.py
 * MovieClass.py
 * RatingClass.py
 * UserClass.py

Executables
-----------
* analyzeMovDB.py
    + analyses based on existing movies/rating/users
    + extract some interesting information such as
        - users' gender and corresponding rating
        - users' age
        - etc.
    + get highest score movies (with more than 100 ratings)
* rateMovies.py
    + for a new user, ask to rate some movies (highest score)
    + store rating & user information to new files
* recommend.py
    + use a specific user's rating and global database
    + choose the best model possible
    + recommend suitable movies for the user. Two modes possible:
         - "OFFLINE" mode: recommend for all users
         - "ONLINE" mode: recommend for user with Id 6041 (newly added)

Recommendation method
=====================
Using (Weighted) Alternating Least Squares

Data & analysis idea
====================

  Data: Movielens
    http://grouplens.org/datasets/movielens/
      1 million ratings, 6000 users on 4000 movies. Released 2/2003.

    suggested by:
      http://www.analyticsvidhya.com/blog/2014/11/data-science-projects-learn/

  Example of analyses inspired from
    http://bugra.github.io/work/notes/2014-04-19/alternating-least-squares-method-for-collaborative-filtering/
    /!\ Data formats are different.

--------
