#This is a webscraping project in Python I did for fun for a Hackathon. I scraped from builtinchicago and GoFundMe and presented the user with questions about donations and made it interactive with user input, as well as tracking the money left over in their budget.

#startups: builtinchicago
import requests
from bs4 import BeautifulSoup
response = requests.get('https://www.builtinchicago.org/2020/01/21/50-chicago-startups-watch-2020')
soup = BeautifulSoup(response.text, 'html.parser')

names = str(soup.select('.description')[0])

#viewNames: gets names of top ten startups in readable format
viewNames = names.replace('</li><li>', '\n')
viewNames = viewNames.replace('</li></ul></div>', '')
viewNames = viewNames.replace('</li></ul><li>', '')
viewNames = viewNames.replace('<div class="description"><ul><li>', '')

#nameList: gets list of names of top ten startups
nameList = viewNames.split('\n')



#donations: GoFundMe
response = requests.get('https://www.gofundme.com/c/act/justice-aapi-community')
soup = BeautifulSoup(response.text, 'html.parser')
titles = soup.find_all(class_='fund-title truncate-single-line show-for-medium')

#titleList: gets list of titles of top ten AAPI fundraisers
index = 0
titleList = []
while index <= 10:
    titleList.append(titles[index].get_text())
    index +=1

#viewTitles: gets titles of top ten AAPI fundraisers in readable format
viewTitles = '\n'.join(map (str, titleList))
print(viewTitles)


#functions:
class purchaseHistory:
    #constructor
    def __init__(self, clothes, food, edu, transport, other,
                    cbudget, fbudget, ebudget, tbudget, obudget):
        self.clothes = clothes
        self.food = food
        self.edu = edu
        self.transport = transport
        self.other = other
        self.cbudget = cbudget
        self.fbudget = fbudget
        self.ebudget = ebudget
        self.tbudget = tbudget
        self.obudget = obudget

    def overBudget(self):
        if (int(self.clothes) > int(self.cbudget)):
            print("Clothes over budget by " 
            + str(int(self.clothes) - int(self.cbudget)))
        if (self.food > self.fbudget):
            print("Food over budget by " 
            + str(int(self.food) - int(self.fbudget)))
        if (self.edu > self.ebudget):
            print("Education over budget by " 
            + str(int(self.edu) - int(self.ebudget)))
        if (self.transport > self.tbudget):
            print("Transportation over budget by " 
            + str(int(self.transport) - int(self.tbudget)))
        if (self.other > self.obudget):
            print("Other over budget by " 
            + str(int(self.other) - int(self.obudget)))
    
    def SurplusOrDeficit(self):
        totalSpent = (int(self.clothes))+(int(self.food))
        +(int(self.edu))+(int(self.transport))+(int(self.other))

        totalBudget = (int(self.cbudget))+(int(self.fbudget))
        +(int(self.ebudget))+(int(self.tbudget))+(int(self.obudget))

        gap = totalSpent - totalBudget

        if (totalSpent > totalBudget):
            print("Deficit of " + str(gap))
        elif (totalSpent < totalBudget):
            print("Surplus of " + str(-gap))
            return -gap
        else:
            print("No net surplus or deficit")
        
    
    #ask if you would like to invest in a startup!
    def investmentAsker(self):
        print("Would you like to invest in one of the following Chicago startups?")
        print('\n' + viewNames +'\n')
        key = input('Enter a for Cameo, b for Livly, c for BrokerX, '
        'd for Clearstep, e for FRST, f for Journey Foods, g for Mavely, '
        'h for Omega Grid, i for The Small Exchange, or j for Zerv.')
        keyList = ['a','b','c','d','e','f','g','h','i','j']
        if key not in keyList:
            print('Error: key entered does not match. Exiting program')
            return
        else:
            investment = input('Invest how much? ')
            listindex = keyList.index(key)

            print("Successfully invested $" + investment + " in " 
            + nameList[listindex] + "!")

            newSurplus = int(self.cbudget)+int(self.fbudget)+int(self.ebudget)
            +int(self.tbudget)+int(self.obudget) 
            - (int(self.clothes)+int(self.food)+int(self.edu)
            +int(self.transport)+int(self.other))

            newSurplus = newSurplus - int(investment)
            print("Your updated budget surplus is: " + str(newSurplus))
        
    #ask if you would like to donate to a fundraiser!
    def donationAsker(self):
        print("Would you like to donate to one of the following AAPI causes?")
        print('\n' + viewTitles +'\n')
        key = input('To select a charity, enter a, b, c, d, e, f, g, h, i, or j.')
        keyList = ['a','b','c','d','e','f','g','h','i','j']
        if key not in keyList:
            print('Error: key entered does not match. Exiting program')
            return
        else:
            donation = input('Donate how much? ')
            listindex = keyList.index(key)
            print("Successfully donated $" + donation + " to the cause: " + titleList[listindex] + "!")
            newSurplus = int(self.cbudget)+int(self.fbudget)+int(self.ebudget)+int(self.tbudget)+int(self.obudget) - (int(self.clothes)+int(self.food)+int(self.edu)+int(self.transport)+int(self.other))
            newSurplus = newSurplus - int(donation)
            print("Your current budget surplus is: $" + str(newSurplus))



#init user object (tests)
print("person1 tests")
person1 = purchaseHistory(100, 30, 18000, 70, 200,
                            200, 200, 18000, 200, 300)
person1.overBudget()
person1.SurplusOrDeficit()

print('\n')
print("person2 tests")
person2 = purchaseHistory(500, 200, 0, 300, 50,
                            350, 250, 0, 250, 100)
person2.overBudget()
person2.SurplusOrDeficit()

print('\n')
print("person3 tests")
person3 = purchaseHistory(200, 200, 50, 400, 100,
                            500, 250, 0, 700, 100)
person3.overBudget()
person3.SurplusOrDeficit()

#person1.donationAsker()
#person3.investmentAsker()
