import pymysql as sql
import re
db = sql.connect(
    host="pf.c7wjaspqw9qm.us-east-1.rds.amazonaws.com",
    user="root",
    password="AWSPassword",
    database="pf2"
)
cur = db.cursor()

def register():
    username = input("Please enter your username: ")
    firstName = input("Please enter your First Name: ")
    lastName = input("Please enter your Last Name: ")
    birthdate = input("Please enter your birthdate in the YYYY-MM-DD: ")
    gender = input("Please enter your gender, M or F: ")
    while gender.upper() not in ["M", "F", "N"]:
        print("Invalid entry!")
        gender = input("Please enter M or F:")
    email = input("Please enter your email address: ")
    while not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("You entered an invalid email address, please try again: ")
        email = input()
    password = input("Please enter your password: ")

    cur.execute("INSERT INTO PUser (Username, FName, LName, Email, Birthdate, gender, UPassword) VALUES (%s,%s,%s, %s,%s,%s, %s)", (username, firstName, lastName, email, birthdate,gender, password,))
    db.commit()
    return username

def agentReview():
    username=input("Please enter your username")
    number = input("Please enter the phone number of the agent you want to review: ")
    query = "SELECT * FROM Agent A WHERE A.ContactNum = '" + number + "';"

    if query is not None:
        cur.execute(query)
        agents = cur.fetchall()
        if (len(agents) == 0):
            print("The agent doesn't exist")
        else:
            rating = input("Please give them a rating from 1 to 10:")
            while not rating.isdigit() and (rating > 10 or rating < 1):
                rating = input("Please enter a valid rating between 1 and 10 ")
            textualReview = input("Please enter a textual review:")
            cur.execute("INSERT INTO Reviews (Username, AgentNum, TextualReview, Rating) VALUES (%s,%s,%s, %s)", (username, number, textualReview, rating))
            db.commit()

#agentReview('aksa')

def viewExistingReviews():
    agentNum = input("Enter the phone number of the agent you would like to see the reviews of: ")
    
    query = "SELECT R.Username, A.FName, A.LName, R.Rating, R.TextualReview FROM Agent A INNER JOIN Reviews R on A.ContactNum=R.AgentNum WHERE A.ContactNum='" + agentNum + "'"
 
    if query is not None:
        cur.execute(query)
        reviews = cur.fetchall()
        for i in range(len(reviews)):
            print("Username: " + reviews[i][0] + " Agent Name: " + reviews[i][1]+ " " +reviews[i][2])
            print(" Rating: ", reviews[i][3])
            print(" Textual Review: " + reviews[i][4])

#viewExistingReviews()

def aggRating():
    print("Please provide us with the name of the broker company")
    brokerCompanies = "SELECT CompanyName FROM BrokerCompany"
    cur.execute(brokerCompanies)
    brokerCompanies = cur.fetchall()
    brokerCompanies = [co[0] for co in brokerCompanies]

    companyIn = input("Please enter the name of the company: ")
    while companyIn not in brokerCompanies:
        print("Invalid company name, try again: ")
        companyIn = input()
    query = "select Br.CompanyName, AVG(R.Rating) as aggRating from Reviews R inner join Agent A on R.AgentNum = A.ContactNum inner join BrokerCompany Br on A.CompanyName = Br.CompanyName where Br.CompanyName='" + companyIn + "'"
    cur.execute(query)
    items = cur.fetchall()
    print("Aggregated rating: {}".format(items[0][1]))

#aggRating()
propertyTypes = "SELECT distinct PType FROM Property;"
cur.execute(propertyTypes)
propertyTypes = cur.fetchall()
propertyTypes = [co[0] for co in propertyTypes]

def devDetails():
    devProjects = "SELECT * FROM DevlopmentProject;"
    cur.execute(devProjects)
    dev_projects = cur.fetchall()

    projName = input("Choose enter the project name of one of the development projects: ")
    
    for propTypes in propertyTypes:
        query = "select devProj.ProjectName, devProj.Location, devProj.PricePerSqft, Count(devProj.ProjectName) from DevlopmentProject devProj inner join Property P on P.ProjectName = devProj.ProjectName where devProj.ProjectName='" + projName + "' and P.PType = '" + propTypes +"'"
        cur.execute(query)
        items = cur.fetchall()
        print("ProjectName: ")
        print(items[0][0])
        print("Location: ")
        print(items[0][1])
        print("Price Per Sqft: ")
        print(items[0][2])
        print("Num of Listings: ")
        print(items[0][3])
        print("Propety Type: " +propTypes)
        print('\n')

#devDetails()
cities = "SELECT distinct City FROM Property;"
cur.execute(cities)
cities = cur.fetchall()
cities = [co[0] for co in cities]

def propInCity():
        city = input("Please enter the city: ")

        while city not in cities:
            print("City not available.")
            city = input("Please enter city from list above: ")

        #Show all the properties of in a certain city, along with the average price / sqm for each unit type  
        for propTypes in propertyTypes:
            query = "select P.Proptitle, P.PType, P.Size, AVG(P.Price/P.Size) as AvgPricePer, P.Listing_Date, P.Bedrooms, P.Bathrooms, P.Price, P.Area, P.City, P.Country, P.Pdescription from Property P where P.City='" + city + "' and P.PType = '" + propTypes +"'"
            cur.execute(query)
            items = cur.fetchall()

            if(items is not None):
                print("Property Title: ")
                print(items[0][0])
                print("Property Type: ")
                print(items[0][1])
                print("Property Size: ")
                print(items[0][2])
                print("Average price per sqft: ")
                print(items[0][3])
                print("Listing Date: ")
                print(items[0][4])
                print("Num of Bedrooms: ")
                print(items[0][5])
                print("Num of Bathrooms ")
                print(items[0][6])
                print("Price: ")
                print(items[0][7])
                print("Area: ")
                print(items[0][8])
                print("City: ")
                print(items[0][9])
                print("Country: ")
                print(items[0][10])
                print("Description: ")
                print(items[0][11])
                print('\n')
            else: print("nothing is available to output")

#propInCity()

#Show all the properties in a certain city in a given price range, with a given set of amenities 
def propbyUser():
    city=input("Please enter the city: ")
    lowRange=input("Please input the lower price range: ")
    upperRange=input("Please input the upper price range: ")
    print("Please input four amentities you would like to have in your property: ")
    amenities = []
    for _ in range(4):
        amenities.append(input())
    
    query = "select P.Proptitle, P.PType, P.Size, P.Listing_Date, P.Bedrooms, P.Bathrooms, P.Price, P.Area, P.City, P.Country, P.Pdescription from Property P inner join Amenities A on A.PropertyId=P.PropertyId where P.City='" + city + "' and P.Price between "+lowRange+" and "+upperRange+" and A.Amenity in ( '" + amenities[0] +"', '"+amenities[1]+"', '"+amenities[2]+"', '"+amenities[3]+"')"
    #print(query)
    cur.execute(query)
    items = cur.fetchall()
    if(items is not None):
        print("Property Title: ")
        print(items[0][0])
        print("Property Type: ")
        print(items[0][1])
        print("Property Size: ")
        print(items[0][2])
        print("Listing Date: ")
        print(items[0][3])
        print("Num of Bedrooms: ")
        print(items[0][4])
        print("Num of Bathrooms ")
        print(items[0][5])
        print("Price: ")
        print(items[0][6])
        print("Area: ")
        print(items[0][7])
        print("City: ")
        print(items[0][8])
        print("Country: ")
        print(items[0][9])
        print("Description: ")
        print(items[0][10])
        print('\n')
    else: print("Nothing is available to output")

#propbyUser()

# Show the top 10 areas in a given city by num of listings and price / sqm of a given unit type
def top10():
        city = input("Please enter the city: ")

        while city not in cities:
            print("City not available.")
            city = input("Please enter a valid city: ")

        query = "select distinct P.Area, count(*) as numOfListings, AVG(P.Price/P.Size) as pricePer from Property P where P.city = '" + city + "' GROUP BY P.Area ORDER BY numOfListings DESC, pricePer DESC LIMIT 10;"
        #print(query)
        cur.execute(query)
        items = cur.fetchall()
        for i in items:
            print("Area: ")
            print(i[0])

#top10()

# Show the top 5 brokerage companies by the amount of listings they have, along with their avg price / sqm, number of agents, and average listings per agent
def top5():

    query = "select BC.CompanyName, AVG(P.Price/P.Size) as pricePer, count(Distinct A.ContactNum) as numOfAgents, BC.NumActiveListings/Count(A.ContactNum) as avgListings from BrokerCompany BC inner join Agent A on A.CompanyName=BC.CompanyName inner join Property P on P.AgentNum=A.ContactNum GROUP BY  BC.CompanyName ORDER BY BC.NumActiveListings DESC, pricePer DESC, numOfAgents DESC, avgListings DESC LIMIT 5;"
    #print(query)
    cur.execute(query)
    items = cur.fetchall()
    for i in items:
        print("Broker Company: ")
        print(i[0])

#top5()

# Show all the properties listed by a specific agent (given their first and last name and / or phone no) 
def propbyAgent():
    lastName=''
    agent = input("Please enter the first and last name of the agent or this phone number: ")
    Name = agent.split(' ')
    if(len(Name)==1):
        firstName=Name[0]
    else:
        firstName=Name[0]
        lastName=Name[1]

    if agent[0].isnumeric():
        query = "select P.Proptitle, P.PType, P.Size, P.Listing_Date, P.Bedrooms, P.Bathrooms, P.Price, P.Area, P.City, P.Country, P.Pdescription from Property P inner join Agent A on A.ContactNum=P.AgentNum WHERE A.ContactNum='" + agent + "';"
        #print(query)
        cur.execute(query)
        items = cur.fetchall()
        print("Property Title: ")
        print(items[0][0])
        print("Property Type: ")
        print(items[0][1])
        print("Property Size: ")
        print(items[0][2])
        print("Listing Date: ")
        print(items[0][3])
        print("Num of Bedrooms: ")
        print(items[0][4])
        print("Num of Bathrooms ")
        print(items[0][5])
        print("Price: ")
        print(items[0][6])
        print("Area: ")
        print(items[0][7])
        print("City: ")
        print(items[0][8])
        print("Country: ")
        print(items[0][9])
        print("Description: ")
        print(items[0][10])
        print('\n')
    elif agent[0].isalpha():
        query = "select P.Proptitle, P.PType, P.Size, P.Listing_Date, P.Bedrooms, P.Bathrooms, P.Price, P.Area, P.City, P.Country, P.Pdescription from Property P inner join Agent A on A.ContactNum=P.AgentNum WHERE A.FName='" + firstName + "' and A.LName = '"+lastName+"'"
        #print(query)
        cur.execute(query)
        items = cur.fetchall()
        if(items is not None):
            print("Property Title: ")
            print(items[0][0])
            print("Property Type: ")
            print(items[0][1])
            print("Property Size: ")
            print(items[0][2])
            print("Listing Date: ")
            print(items[0][3])
            print("Num of Bedrooms: ")
            print(items[0][4])
            print("Num of Bathrooms ")
            print(items[0][5])
            print("Price: ")
            print(items[0][6])
            print("Area: ")
            print(items[0][7])
            print("City: ")
            print(items[0][8])
            print("Country: ")
            print(items[0][9])
            print("Description: ")
            print(items[0][10])
            print('\n')
    else:
        print("Wrong entry")

#propbyAgent()

def run():
    print("Welcome to the Property Finder Application")
    while True:
        print("Please choose one of the following options:")
        print("1. Register User")
        print("2. Review an Agent")
        print("3. View existing reviews of a given Agent")
        print("4. View aggregated rating of a Brokerage company")
        print("5. Show location of Development project")
        print("6. Show properties in a certain city")
        print("7. Show properties in a certain city within a certain price range and list of amenities")
        print("8. Show top 10 areas in a given city--filtered")
        print("9. Show top 5 Brokerage Companies--filtered")
        print("10. Show properties listed by a specific agent")
        print("11. Exit")

        choice = input()
        if choice == "11":
            return 
        elif choice =="1":
            register()
        elif choice =="2":
            agentReview()
        elif choice =="3":
            viewExistingReviews()
        elif choice =="4":
            aggRating()
        elif choice =="5":
            devDetails()
        elif choice=="6":
            propInCity()
        elif choice =="7":
            propbyUser()
        elif choice =="8":
            top10()
        elif choice =="9":
            top5()
        elif choice =="10":
            propbyAgent()

        again=input("Would you like to view something else? Y/N")
        if(again=='Y'):
            run()


if __name__ == "__main__":
    run()