

#inputs on variables such as age, gender, height, weight, activity level
import json
import math
import requests
import pandas as pd

class Calorie:
  '''
   Class to fetch and calculate Calorie and BMI.
  '''

  # Initializing all variables.
  def __init__(self, userInput):   
    self.input_dictionary = userInput           #Dictionary to store user input
    self.bmi = 0.0                              #Variable to store BMI from API.
    self.calorie_intake_requirements = {}       #Dictionary to store different calorie requirements based on the goal.
    self.ref_data = pd.read_csv("./Body_measurements_of_507_physically_active_individuals.csv")    #Reference data.
    self.mean_age_and_gender_bmi = 0.0        #Variable to store mean age and gender bmi from reference data.
    self.required_calories = 0                #Variable to store final required calories.

  def getBMIFromAPI(self):
      #print(self.input_dictionary)
      url = "https://fitness-calculator.p.rapidapi.com/bmi"

      #put that inputDictionary in API link for website for BMI:
      querystring = {
                     "age": str(round(self.input_dictionary['age'])) ,
                     "weight":str(self.input_dictionary['weight']),
                     "height":str(self.input_dictionary['height'])
                     }

      headers = {
          'x-rapidapi-host': "fitness-calculator.p.rapidapi.com",
          'x-rapidapi-key': "b0e38d457amshf93059959318267p152217jsn57a509da2f2d"
          }

      response = requests.request("GET", url, headers=headers, params=querystring)

      # json.loads converts string json response.text into a python object that we can use in the code 
      responseDict = json.loads(response.text)
      BMI = responseDict['data']['bmi']

      self.bmi = BMI

      return self.bmi

  def calculateBenchmarkedBMI(self):
      #Dictionary to convert user input to ref data key for sex/gender.
      gender_dict = {"male": 1, "female": 0}
      
      #Filtering data based on age and gender entered by the user.
      filtered_df = self.ref_data[(self.ref_data['age'] == self.input_dictionary['age']) 
                              & (self.ref_data['sex'] == gender_dict[self.input_dictionary['gender']])]

      #If user-entered values are not found, then take all rows belonging to the range(age-5,age+5)
      if len(filtered_df)==0:
        filtered_df = self.ref_data[((self.ref_data['age']>self.input_dictionary['age']-5)
                                 & (self.ref_data['age']<self.input_dictionary['age']+5)) 
                                 & (self.ref_data['sex'] == gender_dict[self.input_dictionary['gender']])]

      #Function to calculate square.
      def square(x):
        return math.pow(x,2)

      #Calculating bmi for all rows in the filtered df.(We divide height by 100 here to convert from centimeters to meters.)
      bmi_series = filtered_df['wgt']/(filtered_df['hgt']/100).apply(lambda x: square(x))

      self.mean_age_and_gender_bmi = bmi_series.mean()

      return self.mean_age_and_gender_bmi

  def interpretBMI(self):
      bmi = self.input_dictionary['weight']/math.pow(self.input_dictionary['height']/100,2)
      diff_in_bmi = bmi - self.calculateBenchmarkedBMI()
      
      print("Difference in your BMI and Benchmarked BMI: " + str(round(diff_in_bmi, 2)))
      
      if(diff_in_bmi > 0):
          print('Based on the above difference, we suggest you take up goals that help you reduce weight to reach your ideal BMI')
      elif(diff_in_bmi <0):
          print('Based on the above difference, we suggest you take up goals that help you gain weight to reach your ideal BMI')
      else:
          ("Based on the above difference, we suggest you take up goals that help you maintain weight to stay at your ideal BMI")
          
      return round(diff_in_bmi,2)

  def getCalorieIntakeRequirementsFromAPI(self):
      url = "https://fitness-calculator.p.rapidapi.com/dailycalorie"

      #put that inputDictionary in API link for website for Calorie intake requirements:
      querystring = {
                     "age": str(round(self.input_dictionary['age'])) ,
                     "weight":str(self.input_dictionary['weight']),
                     "height":str(self.input_dictionary['height']),
                     "gender":str(self.input_dictionary['gender']),
                     "activitylevel":"level_" + str(self.input_dictionary['activity'])
                     }

      headers = {
          'x-rapidapi-host': "fitness-calculator.p.rapidapi.com",
          'x-rapidapi-key': "b0e38d457amshf93059959318267p152217jsn57a509da2f2d"
          }

      response = requests.request("GET", url, headers=headers, params=querystring)

      responseDict = json.loads(response.text)
      self.calorie_intake_requirements = responseDict["data"]

      return self.calorie_intake_requirements

  def decisionOnWeightLossOption(self):
      print("Provided is option of goals you might want to achieve:")
      print("1: Maintain Weight")
      print("2: Weight loss")
      print("3: Extreme weight loss")
      print("4: Mild weight gain")
      print("5: Weight gain")
      print("6: Extreme weight gain")

      user_decision = int(input("Please pick your goal:"))

      while True:
        try:
          if (user_decision == 1):
              self.required_calories = self.calorie_intake_requirements["goals"]["Mild weight loss"]["calory"]
              break
          elif (user_decision == 2):
              self.required_calories = self.calorie_intake_requirements["goals"]["Weight loss"]["calory"]
              break
          elif (user_decision == 3):
              self.required_calories = self.calorie_intake_requirements["goals"]["Extreme weight loss"]["calory"]
              break
          elif (user_decision == 4):
              self.required_calories = self.calorie_intake_requirements["goals"]["Mild weight gain"]["calory"]
              break
          elif (user_decision == 5):
              self.required_calories = self.calorie_intake_requirements["goals"]["Weight gain"]["calory"]
              break
          elif (user_decision == 6):
              self.required_calories = self.calorie_intake_requirements["goals"]["Extreme weight gain"]["calory"]
              break
          else:
              print(">>Wrong input: Please enter correct choice!")
        except ValueError:
          print(">> Wrong input, goal choice should be a number!")
          continue
  
      return {'option':user_decision, 'calorie_requirement': self.required_calories}
  