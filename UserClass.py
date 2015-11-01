import os, sys, os.path 
###########################################################################
class User : 
   #UserID::Gender::Age::Occupation::Zip-code
   UserId     = -1
   Gender     = ' '
   Age        = -1
   Occupation = ' '
   Zipcode    = -1

   def __init__ (self, _id, _gender, _age, _occ, _zip) :
      self.UserId     = int(_id)
      self.Gender     = _gender
      self.Age        = int(_age)
      self.Occupation = int(_occ)
      self.Zipcode    = int(_zip)


class ExtendedUser :
# --- ajouter la liste des films que l'utilisateur a 
   UserId     = -1
   Gender     = ' '
   Age        = -1
   Occupation = ' '
   Zipcode    = -1
   ratedMIds  = []
   ratedMScs  = []

   def __init__ (self) :
      self.UserId     = -1
      self.Gender     = ' '
      self.Age        = -1
      self.Occupation = ' '
      self.Zipcode    = -1
      self.ratedMIds  = []
      self.ratedMScs  = []

   def __init__ (self, _id, _gender, _age, _occ, _zip, _ratedMIds, _ratedMScs) :
      self.UserId     = int(_id)
      self.Gender     = _gender
      self.Age        = int(_age)
      self.Occupation = int(_occ)
      self.Zipcode    = int(_zip)
      self.ratedMIds  = _ratedMIds
      self.ratedMScs  = _ratedMScs


#def inputUserByID(
      

def inputUserInfo(_id_) :
# used only if user does not exist in database
   print 'User information\n'
   print 'Age range: '
   print '''  *  1:  "Under 18"
  * 18:  "18-24"
  * 25:  "25-34"
  * 35:  "35-44"
  * 45:  "45-49"
  * 50:  "50-55"
  * 56:  "56+"
   '''
   _age_ = raw_input('Your age range? ')


   _gender_ = raw_input('Your gender? [F/M] ')


   print '''\n Occupation: 
  *  0:  "other" or not specified
  *  1:  "academic/educator"
  *  2:  "artist"
  *  3:  "clerical/admin"
  *  4:  "college/grad student"
  *  5:  "customer service"
  *  6:  "doctor/health care"
  *  7:  "executive/managerial"
  *  8:  "farmer"
  *  9:  "homemaker"
  * 10:  "K-12 student"
  * 11:  "lawyer"
  * 12:  "programmer"
  * 13:  "retired"
  * 14:  "sales/marketing"
  * 15:  "scientist"
  * 16:  "self-employed"
  * 17:  "technician/engineer"
  * 18:  "tradesman/craftsman"
  * 19:  "unemployed"
  * 20:  "writer"
'''
   _occ_ = raw_input('What is your occupation? ')


   _zip_ = 99
   _zip_ = int(raw_input('Where do you live? (enter your zip code) '))

   a_user = User(_id_, _gender_, _age_, _occ_, int(_zip_) )
   return a_user



