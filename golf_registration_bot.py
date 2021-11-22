from bs4 import BeautifulSoup
import requests as req
import logging, time, random, schedule
import golf_configuration as config
import calendar, datetime

# Format Logger
log_format = (
    '[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s')

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    filename=('C:\\Program Files (x86)\\Golf\\GolfRegistration.log'),
)
# This should only be enabled if you want to run the script one off - with predefined time in config file
#bookingStart = config.bookingStart
#selectedDate = config.selectedDate
#bookingDate = config.bookingDate

clubGuid = config.golfClubId # Club GUID
ressourceGuid = config.ressourceId

# Login credentials
userName = config.userName
password = config.password
loginData = [
    ('loginform.submitted', 'true'),
    ('command', 'login'),
    ('loginform.username', userName),
    ('loginform.password', password),
    ('loginform.submit', 'LOGIN')
]

def isServiceAlive():
    logging.info('Hello - I am still alive')

def setBookingTimeBasedOnWeekday(today):
    if today == 'Sunday':
        #We want 9 something AM on Saturdays
        # Need to add some variance in time picking
        today = datetime.datetime.now() + datetime.timedelta(days=6)
        selectedDate = today.date().strftime('%Y%m%dT%H%M%S')
        bookingDate = selectedDate[6:8] + '.' + selectedDate[4:6] + '.' + selectedDate[0:4]
        bookingStart = (datetime.datetime.strptime(selectedDate, '%Y%m%dT%H%M%S') + datetime.timedelta(hours=9) + datetime.timedelta(minutes=random.choice(config.additionalWeekendMinutes))).strftime('%Y%m%dT%H%M%S')
    elif today == 'Monday':
        # We want 9 something AM on Sundays
        # Need to add some variance in time picking
        today = datetime.datetime.now() + datetime.timedelta(days=6)
        selectedDate = today.date().strftime('%Y%m%dT%H%M%S')
        bookingDate = selectedDate[6:8] + '.' + selectedDate[4:6] + '.' + selectedDate[0:4]
        bookingStart = (datetime.datetime.strptime(selectedDate, '%Y%m%dT%H%M%S') + datetime.timedelta(hours=9) + datetime.timedelta(minutes=random.choice(config.additionalWeekendMinutes))).strftime('%Y%m%dT%H%M%S')
    elif today == 'Tuesday':
        selectedDate = ''
        bookingDate = ''
        bookingStart = ''
        logging.info('No interest in registration by automation - will do manually if needed')
    elif today == 'Wednesday':
        # We want 17 something AM on Sundays
        today = datetime.datetime.now() + datetime.timedelta(days=6)
        selectedDate = today.date().strftime('%Y%m%dT%H%M%S')
        bookingDate = selectedDate[6:8] + '.' + selectedDate[4:6] + '.' + selectedDate[0:4]
        bookingStart = (datetime.datetime.strptime(selectedDate, '%Y%m%dT%H%M%S') + datetime.timedelta(hours=17) + datetime.timedelta(minutes=random.choice(config.additionalWeekMinutes))).strftime('%Y%m%dT%H%M%S')
    elif today == 'Thursday':
        # We want 17 something AM on Sundays
        today = datetime.datetime.now() + datetime.timedelta(days=6)
        selectedDate = today.date().strftime('%Y%m%dT%H%M%S')
        bookingDate = selectedDate[6:8] + '.' + selectedDate[4:6] + '.' + selectedDate[0:4]
        bookingStart = (datetime.datetime.strptime(selectedDate, '%Y%m%dT%H%M%S') + datetime.timedelta(hours=17) + datetime.timedelta(minutes=random.choice(config.additionalWeekMinutes))).strftime('%Y%m%dT%H%M%S')
    elif today == 'Friday':
        selectedDate = ''
        bookingDate = ''
        bookingStart = ''
        logging.info('No interest in registration by automation - will do manually if needed')
    elif today == 'Saturday':
        selectedDate = ''
        bookingDate = ''
        bookingStart = ''
        logging.info('No interest in registration by automation - will do manually if needed')
    return bookingStart, bookingDate, selectedDate

def executeRegistration():
    ### Disable this section and predefine booking times in config file if you want to run this script only one time ###
    now = datetime.datetime.now()
    bookingStart, bookingDate, selectedDate = setBookingTimeBasedOnWeekday(calendar.day_name[now.weekday()])
    print(bookingStart, bookingDate, selectedDate)
    ### Disable this section and predefine booking times in config file if you want to run this script only one time ###

    if(config.isDateValidForRegistration(selectedDate, bookingStart)):

        logging.info('------------------ LOGIN REQUEST ----------------')
        s = req.Session()

        headersLogin = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.golfbox.dk",
            "Cache-Control": "max-age=0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        }
        #try to login 3 times if there is an error on login as sometimes seen in the first few seconds after 22
        for i in range (0,3):
            login_response = s.post('https://golfbox.dk/login.asp', headers=headersLogin, data=loginData)

            if login_response.status_code == 200 or login_response.status_code == 302:
                logging.info('------------------ RESPONSE HISTORY ----------------')
                logging.info(login_response.history)
                # Sleep randomly for 0-3 seconds after login (try broader interval later)
                time.sleep(random.random()*3)
                break
            elif login_response.status_code == 500:
                logging.error('Internal Server ERROR 500 - RETRY login for ' + str(i) + ' time')
            else:
                logging.error('UNKNOWN ERROR IN LOGIN PHASE')


        ########################################################## REGISTRATION REQUEST 1 ##############################################################
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "max-age=0",
            "Referer": "https://www.golfbox.dk/site/ressources/booking/window.asp?Ressource_GUID={"+ressourceGuid+"}&Booking_Start="+bookingStart+"&club_GUID={"+clubGuid+"}",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        }

        registration_url = "https://www.golfbox.dk/site/ressources/booking/window.asp?Ressource_GUID={"+ressourceGuid+"}&Booking_Start="+bookingStart+"&club_GUID={"+clubGuid+"}"
        registration_data = config.arrayAllUsers

        logging.info('------------------ REGISTRATION REQUEST ----------------')
        #It might come up that registration doesn't open exactly at 22 so lets try 5 times with 1 sec delay until success
        for j in range (0,5):
            registration_response = s.post(registration_url, headers=headers, data=registration_data)

            if registration_response.status_code == 200 or registration_response.status_code == 302:
                logging.info('SUCCESS ON 1st REGISTRATION REQUEST')
                break
            elif registration_response.status_code == 500:
                logging.error('ERROR ON 1st REGISTRATION REQUEST do to internal server error 500 - booking probably not open yet')
                logging.error('--- RETRY in 1 sec --- for the ' + str(j) + ' time')
                time.sleep(1)
            else:
                logging.error('Unknown ERROR on registration 1')

        ########################################################## REGISTRATION REQUEST 2 ##############################################################

        headers2 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "max-age=0",
            "Referer": "https://www.golfbox.dk/site/ressources/booking/grid.asp?SelectedDate="+selectedDate+"&Ressource_GUID={"+ressourceGuid+"}&Club_GUID={"+clubGuid+"}&makeWindowPop=0",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        }
        registration_url2 = "https://www.golfbox.dk/site/ressources/booking/grid.asp?SelectedDate="+selectedDate+"&Ressource_GUID={"+ressourceGuid+"}&Club_GUID={"+clubGuid+"}&makeWindowPop=0"
        registration_data2 = [
            ('command','goToDay'),
            ('commandValue',''),
            ('blockValues',''),
            ('SelectedDate',selectedDate),
            ('ddlClub','%7B'+clubGuid+'%7D'),
            ('ddlRessource_GUID','%7B'+ressourceGuid+'%7D'),
            ('chkShowPlayerDetails','on'),
            ('BookingDate',bookingDate)
        ]

        logging.info('------------------ REGISTRATION REQUEST 2 ----------------')
        # if server error then try again up to 5 times
        for k in range (0,5):
            registration_response2 = s.post(registration_url2, headers=headers2, data=registration_data2)

            if registration_response2.status_code == 200 or registration_response2.status_code == 302:
                logging.info('SUCCESS ON 2nd REGISTRATION REQUEST')
                break
            elif registration_response2.status_code == 500:
                logging.error('ERROR ON 2nd REGISTRATION REQUEST')
                logging.error('--- RETRY in 1 sec --- for the ' + str(k) + ' time')
                time.sleep(1)
            else:
                logging.error('UNKNOWN ERROR ON 2nd REGISTRATION REQUEST')
    else:
        logging.error('Date is invalid for registration')

schedule.every().day.at("22:00:02").do(executeRegistration) # 2 seconds past 22 - should probably change it to random 0-5 sec
schedule.every(5).minutes.do(isServiceAlive)

while 1:
    schedule.run_pending()
    time.sleep(1)