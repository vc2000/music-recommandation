users = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
          "Ben": {"Taylor Swift": 5, "PSY": 2},
          "Clara": {"PSY": 3.5, "Whitney Houston": 4},
          "Daisy": {"Taylor Swift": 5, "Whitney Houston": 3}}

class recommender:

   def __init__(self, data="", n=5):
      """ initialize recommender
      currently, if data is dictionary the recommender is initialized
      to it.
      For all other data types of data, no initialization occurs
      n is the maximum number of recommendations to make"""
      self.n = n
      self.username2id = {}
      self.userid2name = {}
      self.productid2name = {}
      #
      # The following two variables are used for Slope One
      #
      self.frequencies = {}
      self.deviations = {}

      # if data is dictionary set recommender data to it
      #
      if type(data).__name__ == 'dict':
         self.data = data

   def convertProductID2name(self, id):
      """Given product id number return product name"""
      if id in self.productid2name:
         return self.productid2name[id]
      else:
         return id


   def userRatings(self, id, n):
      """Return n top ratings for user with id"""
      #print ("Ratings for " + self.userid2name[id])
      ratings = self.data[id]
      print(len(ratings))
      ratings = list(ratings.items())[:n]
      ratings = [(self.convertProductID2name(k), v)
                 for (k, v) in ratings]
      # finally sort and return
      ratings.sort(key=lambda artistTuple: artistTuple[1],
                   reverse = True)
      for rating in ratings:
         print("%s\t%i" % (rating[0], rating[1]))


   def showUserTopItems(self, user, n):
      """ show top n items for user"""
      items = list(self.data[user].items())
      items.sort(key=lambda itemTuple: itemTuple[1], reverse=True)
      for i in range(n):
         print("%s\t%i" % (self.convertProductID2name(items[i][0]),
                           items[i][1]))

   def computeDeviations(self):
      # for each person in the data:
      #    get their ratings
      i = 0
      for ratings in self.data.values():
         # for each item & rating in that set of ratings:
         i += 1
         for (item, rating) in ratings.items():
            self.frequencies.setdefault(item, {})
            self.deviations.setdefault(item, {})
            # for each item2 & rating2 in that set of ratings:
            for (item2, rating2) in ratings.items():
               if item != item2:
                  # add the difference between the ratings to our
                  # computation
                  self.frequencies[item].setdefault(item2, 0)
                  self.deviations[item].setdefault(item2, 0.0)
                  self.frequencies[item][item2] += 1
                  self.deviations[item][item2] += rating - rating2
      for (item, ratings) in self.deviations.items():
         for item2 in ratings:
            ratings[item2] /= self.frequencies[item][item2]


   def slopeOneRecommendations(self, userRatings):
      recommendations = {}
      frequencies = {}
      # for every item and rating in the user's recommendations
      for (userItem, userRating) in userRatings.items():
         # for every item in our dataset that the user didn't rate
         for (diffItem, diffRatings) in self.deviations.items():
            if diffItem not in userRatings and \
               userItem in self.deviations[diffItem]:
               freq = self.frequencies[diffItem][userItem]
               recommendations.setdefault(diffItem, 0.0)
               frequencies.setdefault(diffItem, 0)
               # add to the running sum representing the numerator
               # of the formula
               recommendations[diffItem] += (diffRatings[userItem] +
                                             userRating) * freq
               # keep a running sum of the frequency of diffitem
               frequencies[diffItem] += freq
      recommendations =  [(self.convertProductID2name(k),
                           v / frequencies[k])
                          for (k, v) in recommendations.items()]
      # finally sort and return
      recommendations.sort(key=lambda artistTuple: artistTuple[1],
                           reverse = True)
      # I am only going to return the first 50 recommendations
      return recommendations[:50]
