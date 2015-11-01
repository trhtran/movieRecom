class Movie :
   MId    = -1
   Title  = ''
   Genres = ''
   Year   = -1
   def __init__(self, _id, _title, _genre, _year) :
      self.MId    = _id
      self.Title  = _title
      self.Genres = _genre.split('|')
      self.Year   = _year


