from bs4 import BeautifulSoup
import requests
import mysql.connector

global host_name
host_name = "hostname"
global user_name
user_name = "username"
global my_password
my_password = "password"
global my_database
my_database = "database" 

def urlChoice():
    print("1: Event \n2: Community Day \n3: Spotlight Hour \n4: Tier 5 Raid \n5: Mega Raid \n6: Shadow Raid")
    uType = input('What type of url are you using?: ')
    urlType = str(uType)
    if (urlType == '1'):
        return getEventDetails()
    elif (urlType == '2'):
        return getComDayDetails()
    elif(urlType == '3'):
        return getSpotHourDetails()
    elif(urlType == '4'):
        return getT5Details()
    elif(urlType == '5'):
        return getMegaRaidDetails()
    elif(urlType=='6'):
        return getShdwRaidDetails()
    else:
        print("Invalid error... try again")
        urlChoice()


def getEventDetails(my_url):
    print('x')
def getComDayDetails(my_url):
    print('x')
def getSpotHourDetails(my_url):
    print('x')
def getT5Details():
    print('x')
def getMegaRaidDetails(my_url):
    print('x')
def getShdwRaidDetails(my_url):
    print('x')

def getDetails(my_url):
    r=requests.get(my_url)
    soup=BeautifulSoup(r.content,"html.parser")
    title_text=soup.find("h1",{"class":"page-title"}).get_text().strip()
    start_text=soup.find("span",{"id":"event-date-start"}).get_text().strip()
    end_text=soup.find("span",{"id":"event-date-end"}).get_text().strip()
    description_text=soup.find("div",{"class":"event-description"}).get_text().strip()
    pkmn_name_text=soup.find("div",{"class":"pkmn-name"}).get_text().strip()
    print("Title: " + title_text + '\nDescription: ' + description_text + '\nStart Date: ' + start_text + '\nEnd Date: ' + end_text + '\nPokémon: ' + pkmn_name_text)
    return title_text, description_text, start_text, end_text, pkmn_name_text

def sqlChoice(url_details):
    sql_choice = input("Would you like to send this to sql? [Y/N]: ").capitalize()
    if (sql_choice == 'Y'):
        print("Sent to SQL!")
        sendSQL(url_details)
    elif (sql_choice == 'N'):
        print("Your data was not sent to SQL")
    else:
        print("Invalid Input")
        sqlChoice()
    
def again():
    again_choice = input("Would you like to input another link? [Y/N]: " ).capitalize()
    if (again_choice == 'Y'):
        main()
    elif (again_choice == 'N'):
        print("Thank you for using :D")
        quit()
    else:
        print("Invalid Input...")
        again()

def sendSQL(send_details):
    print("Do here")
    mydb = mysql.connector.connect(
        host= host_name,
        user= user_name,
        password= my_password,
        database= my_database
    )

    mycursor = mydb.cursor()

    data_to_insert = (send_details)
    print(send_details)
    # Need a way to get the dates, times, and color code from the url...
    # Right now I can only get event name, start dates (in string not dateformat, and the name of pokemon)
    # Think it would make sense to add a "What kind of event is this?" choice to make sure two different events have ways to break it lolz
    insert_query = "INSERT INTO PokeData.all_events(type, name, description,  begin_date, final_date, start_date, end_date, begin_time, start_time, thumnail_url, title_url, embed_color, footer) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s)"
def main():
    urlChoice()
    print('=============================')
    details = urlChoice(url)
    print('=============================')
    sqlChoice(details)
    again()

main()
