

import pandas as pd
from calorie import Calorie
from food import FoodRecommendation
from workout import WorkOut
import pdfkit
import os

def askInput():
  print("Welcome to CMU healthier life application!")
  print("This application would help you plan your weekly meal and workout plan based on your basic information\n")
  
  print()
  print("-----------------------------------------------------------------------------------------------")
  print("------------------------------------- User Input ----------------------------------------------")
  print("-----------------------------------------------------------------------------------------------")
  print()
  
  while True:
    try:
      age = int(input("First, Enter your age: "))
      if age >= 0 and age <= 80:
        break;
      else:
        print(">> Wrong input, Age cannot be negative or bigger than 80. Input again.\n")
    except ValueError:
      print(">> Wrong input, Age should be in integer. Input again.\n")
      continue
  
  while True:
    gender = input("Next, Enter your gender (female or male): ")
    if gender.lower() == "female" or gender.lower() == "male":
      break;
    else:
      print(">> Wrong input, Gender should be female or male. Input again.\n")
      continue
  
  while True:
    try:
      height = float(input("Next, Enter your height (in cm): "))
      if height >= 130 and age <= 230:
        break;
      else:
        print(">> Wrong input, Height cannot be smaller than 130 or bigger than 230. Input again.\n")
    except ValueError:
      print(">> Wrong input, Height should be in number. Input again.\n")
      continue
  
  while True:
    try:
      weight = float(input("Next, Enter your weight (in kg): "))
      if weight >= 40 and weight <= 160:
        print()
        break;
      else:
        print(">> Wrong input, Weight cannot be smaller than 40 or bigger than 160. Input again.\n")
    except ValueError:
      print(">> Wrong input, Weight should be in number. Input again.\n")
      continue

  print("Provided is a list of activity level:")
  print("1: No or very little exercise")
  print("2: Exercise 1-3 times/week")
  print("3: Exercise 4-5 times/week")
  print("4: Daily exercise or intense exercise 3-4 times/week")
  print("5: Intense exercise 6-7 times/week")
  while True:
    try:
      activity = int(input("Please pick which one fits your current activity level: "))
      if activity >= 1 and activity <= 5:
        break;
      else:
        print(">> Wrong input, Activity cannot be smaller than 1 or bigger than 5. Input again.\n")
    except ValueError:
      print(">> Wrong input, Activity should be in number. Input again.\n")
      continue

  inputDictionary = {'age': age, 'gender': gender.lower(), 'height': height, 'weight': weight, 'activity':activity}
  
  #dictionary are returned
  return inputDictionary

def printOutput(foodRecDict, workoutSchedule):
    #as part of output, string html is created for the html format for pdf
    html = "<h1><center>Your Weekly Meal and Workout Plan</center></h1><br><h2>Meal Plan</h2>"
    print("---------------------------------------Weekly Meal Plan----------------------------------------")
    
    #counter i to help count the days
    i = 0
    
    #loop is entered for each day of the food dictionary (there will be 7, one for each day)
    for key in foodRecDict:
        if i != 0:
            print()
        print("-----------------------------------------------------------------------------------------------")
        print("---------------------------------------------Day " + str(i+1) + "---------------------------------------------")
        print("-----------------------------------------------------------------------------------------------")
        
        #html string is updated
        html = html + "<h3>Day "+ str(i+1) + "</h3>"
        #dictionary of food details per day stored in foodlist
        foodList = foodRecDict[key]
        
        #check the maximum length of column for purpose of creating dataframe
        foodDF = pd.DataFrame()
        maxfoodlength = 0
        for food in foodList:
            for component in food.keys():
                if component != 'MealBasicInfo':
                    for info in food[component]:
                        allFood = food[component][info]
                        #if the current length of food details is shorter, then update the value
                        if maxfoodlength < len(allFood):
                            maxfoodlength = len(allFood)                        
                   
        #getting information from the dictionary given
        for food in foodList:
            for component in food.keys():
                #this if statement is entered when the dictionary has value of the daily nutrition intake
                if component == 'MealBasicInfo':
                    #get the dictionary of daily nutrition intake
                    basicInfo = foodList[0]['MealBasicInfo']
                    #print the value
                    print ("\nDaily Nutrition : {:<15} {:<15} {:<13} {:<15}".format(('Calories: '+ basicInfo['Calories']),('Protein: '+ basicInfo['Protein']),('Fat: '+ basicInfo['Fat']),('Carbohydrates: '+ basicInfo['Carbohydrates'])))
                    #update html string
                    html = html + "<p>Calories: " + basicInfo['Calories'] + "      Protein: " + basicInfo['Protein'] + "      Fat: " + basicInfo['Fat']  + "   Carbohydrates: " + basicInfo['Carbohydrates'] +"</p>"
                #this if statement is entered when the dictionary has value of daily food recommendation
                else:
                    for info in food[component]:
                        allFood = food[component][info]
                        #get the name of the meal and how much calorie it has
                        columnName = (component + " (" + info + ")")
                        currentColumn = []
                        #store the value of each ingredients
                        for eachIngredient in allFood:
                            for ingredient in eachIngredient.keys():
                                currentColumn.append(ingredient + " (" + eachIngredient[ingredient] + ")")
                    #if lenght of column is shorter then maximum length, fill in the rest with empty string
                    if not maxfoodlength == len(currentColumn):
                        currentColumn.extend(['']*(maxfoodlength-len(currentColumn)))
                    #concat column to existing dataframe
                    foodDF[columnName] = currentColumn
        i = i+1
        print()
        #add html version of dataframe to html string
        html = html + foodDF.to_html()
        print(foodDF)	
    
    #update the value of html string
    html = html + "<br><h2>Workout Plan</h2>"
    #create the workout dataframe`
    workoutDF = pd.DataFrame()    
    i = 0
    
    #checking the maximum length of each column
    workoutMaxLength = 0
    for dailyExercise in workoutSchedule:
        currentLength = len(dailyExercise[1])
        #check the length of exercise of each day, if current length is longer than the max value, update it
        if workoutMaxLength < currentLength:
            workoutMaxLength = currentLength
        
    #getting information
    for dailyExercise in workoutSchedule:
        columnName = "Day " + str(i+1) + " - " + dailyExercise[0]
        currentList = dailyExercise[1]
        #if information is shorter than the maximum length, fill the rest with empty string
        if not workoutMaxLength == len(currentList):
            currentList.extend(['']*(workoutMaxLength-len(currentList)))
        #combnine information to the existing dataframe
        workoutDF[columnName] = currentList
        i = i+1
    
    print()
    print("-----------------------------------------------------------------------------------------------")
    print("-------------------------------------Weekly Workout Plan---------------------------------------")
    print("-----------------------------------------------------------------------------------------------")
    print()
    html = html + workoutDF.to_html()
    
    #print the workout dataframe
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(workoutDF)
    
    #edit this path for testing
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    
    #getting output in form of pdf
    pdfkit.from_string(html, "FinalOutput.pdf", configuration=config)
    
#main method
#program starts here when it runs
#its purpose is only to call other methods
def main():
  
    
    print("--------------------------------------------------------------------------------------------------------------") 
    print("----------------------------------------CMU HEALTHIER LIFE APPLICATION----------------------------------------")
    print("--------------------------------------------------------------------------------------------------------------")    
    print()
    
    #call askinput method
    inputDictionary = askInput()
    
    #create calorie object
    calorie = Calorie(inputDictionary)
    #get the BMI
    calorie.getBMIFromAPI()
    #get calorie intake
    calorie.getCalorieIntakeRequirementsFromAPI()
    #calculate benchmark bmi
    calorie.calculateBenchmarkedBMI()
    
    print("\nCalculating your BMI and the Benchmark BMI")
    calorie.interpretBMI()
    
    print()
    #shows result
    calorieResult = calorie.decisionOnWeightLossOption()
    
    print()
    print("-----------------------------------------------------------------------------------------------")
    print("------------------------------------- User Output ---------------------------------------------")
    print("-----------------------------------------------------------------------------------------------")
    print()
    print("Your calorie intake requirement is: " + str(round(calorieResult['calorie_requirement'], 2)))
    print()
    
    #create FoodRecommendation object
    foodRec = FoodRecommendation(calorieResult['calorie_requirement'])
    #get food recommendation
    foodRecDict = foodRec.getRecommendation()
    
    #create workout object
    wo = WorkOut(inputDictionary['age'], calorieResult['option'], inputDictionary['gender'])
    #categorize the workout
    wo.categorizeWorkOut()
    #get workout plan
    workoutSchedule = wo.getWorkOutPlan()
    
    #call printOutput to shows result
    printOutput(foodRecDict, workoutSchedule)
    

if __name__== '__main__':
  main()