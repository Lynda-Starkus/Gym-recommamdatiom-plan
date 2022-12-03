import requests
from bs4 import BeautifulSoup

class FoodRecommendation:
    
    
    def __init__(self, recommendedCal):
        self.__calories = recommendedCal
        self.__closestCal = 0

    def getRecommendation(self):
        
        
        self.__closestCal =round(self.__calories/100)*100
        mealBasicInfoDict=dict()
        dayDict=dict()
        macroList=list()
        
        
        minCalories=1000
        maxCalories=4000
        calorieCorrection=1300
        
        
        if self.__closestCal<minCalories:
            self.__closestCal=minCalories
        if self.__closestCal>maxCalories:
            self.__closestCal=maxCalories

        
        if self.__closestCal==calorieCorrection:
            link="https://www.prospre.io/meal-plans/"+str(self.__closestCal)+"-calories-meal-plan"
        else:
            link="https://www.prospre.io/meal-plans/"+str(self.__closestCal)+"-calorie-meal-plan"
            
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser') 
        typeList = ['Calories', 'Protein', 'Fat', 'Carbohydrates']
        
        
        nutrientDay=soup.find_all("div", {"class": "nutrient-summary"})
        for a in nutrientDay:	
            amount=a.find_all(class_="macro-amount")
            for b in amount:
                macroList.append(b.get_text())

        d=1
        
        
        for i in range(0,len(macroList),+4):
            mealBasicInfoDict=dict()
            dayDictComponent=list()
            value=macroList[i:i+4]
            basicInfoDict=dict(zip(typeList, value))
            mealBasicInfoDict['MealBasicInfo']=basicInfoDict
            dayDictComponent.append(mealBasicInfoDict)
            tagDay="Day"+str(d)
            dayDict[tagDay]=dayDictComponent
            d=d+1

        meal = soup.find_all('div', {"class": "meal-card"})
        foodList = list()
        for m in meal:
            mealRecipesDict=dict()
            mealTypeDict=dict()
            h3 = m.find('h3')
            mealComponent = h3.get_text()
            mealComponentQuantity= mealComponent.split(':')[1].strip()
            mealComponentName= mealComponent.split(':')[0].strip()
            detail=m.find_all('div',{"class":"meal-columns w-row"})
            recipesList=list()
            for d in detail:
                recipeDict=dict()
                name=d.find(class_="recipe-name").get_text()
                amount=d.find(class_="recipe-amount").get_text()
                recipeDict[name]=amount
                recipesList.append(recipeDict)
            mealRecipesDict[mealComponentQuantity]=recipesList
            mealTypeDict[mealComponentName]=mealRecipesDict
            foodList.append(mealTypeDict)

        
        d=0
        for i in range (0, len(foodList)):
            if 'Breakfast' in foodList[i].keys():
                d=d+1
                tagDay="Day"+str(d)
                dayDict[tagDay].append(foodList[i])   
            else:   
                dayDict[tagDay].append(foodList[i])   
                
        return dayDict