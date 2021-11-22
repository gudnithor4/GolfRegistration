import numpy, datetime

# Login credentials
userName = 'IS-3-1234' #example: 'IS-3-1234'
password = 'XXX'

# Set this as the club where you want to book a tee time
# See list of clubs and respective GUIDs below
golfClubId = "0CA7A186-060B-4338-85A5-C4776B9F7D4D"
# ResourceId is the Golf Course Id (not to be confused with the clubId e.g. GR has 3 different courses)
ressourceId = "11D1FAE4-EE64-487C-91AD-2693B8C3FA1E"

# These minutes will be used to randomly choose booking times on weekends and normal days
additionalWeekendMinutes = [6, 15, 24, 33, 42, 51]
additionalWeekMinutes = [3, 12, 21, 30, 39, 48, 57]
#additionalWeekMinutes = [6, 15, 24, 33, 42, 51]

### 
### NOTE: This is only needed if you want to manually register time for each run of the script
###
# Booking time on the Format YYYYMMDDTHHmmss
# SelectedDate always seems to be equal to bookingStart in all requests so it is set as such
# Seconds should not be set 
# 10 minute intervals are allowed
bookingStart = '20210520T213300'
selectedDate = bookingStart[0:9] + '000000'

# Booking date on the format DD.MM.YYYY
# Have tried values in the past, today, future, does not seem to matter.
# Should be set as same date value as in bookingStart and selectedDate
bookingDate = selectedDate[6:8] + '.' + selectedDate[4:6] + '.' + selectedDate[0:4]

# Function to validate 9 minute intervals between the allowed registration hours
def minuteValidation(start, bookingTime):
    start = datetime.datetime.strptime(start,'%Y%m%dT%H%M%S')
    startAtSeven = start + datetime.timedelta(hours=7)
    seq = []
	# There are 100 possible slots in 9 minute intervals from 07:00 - 21:51
    for x in range(99):
        startAtSeven = startAtSeven + datetime.timedelta(minutes=9)
        seq.append(startAtSeven.strftime('%Y%m%dT%H%M%S'))
    if bookingTime in seq:
        return 1
    else:
        return 0


#### BookingDate Rules ####
# You can only book 6 days in advance e.g. if registration opens at 22:00 on 20.04 you can book tee times on the following days 
# 21.04, 22.04, 23.04, 24.04, 25.04, 26.04 //depends on clubs
# Only between the hours of 07:00 - 21:51 //This depends on golfclubs and might change base on time of year
# Always 9 minutes between tee times : starting at 07:00 and ends ar 21:51
# Latest time for booking a tee time is 0 minutes before
def isDateValidForRegistration(selectedDate, bookingStart):
	dateFormat = '%Y%m%dT%H%M%S'
	try:
		date = datetime.datetime.strptime(bookingStart, dateFormat)
		# Check if date is in the past
		if(date < datetime.datetime.now()):
			return 0
		# Check if we are booking more than 6 days in advance
		if(date > date.today() + datetime.timedelta(6)):
			return 0
		# Check if the minutes are always divisible by 9
		if(not minuteValidation(selectedDate, bookingStart)):
			return 0
		else:
			return 1
	except ValueError:
		print("Incorrect data format, should be YYYYMMDDTHHmmss")
		return 0


# List of users 
# Note that there are 2 distinct unique identifiers 
# 1. is the part of the login username minus the countrycode e.g. 3-1234
# 2. is internal code aquired through Fiddler 
# AuthUser is defined differently due to the need for internal GUID
authUser = ('Gudni', '3-1234', 'MyGUID')

# When populating the registry we work sequentially through this
# Need to find GUID through Fiddler or browser developer tools
otherUsersList = [
    ('NameOfUser1', '3-1111', 'GUID1'),
    ('NameOfUser2', '3-2222', 'GUID2'),
    ('NameOfUser3', '3-3333', 'GUID3')
	#('NameOfUser4', '3-4444', 'GUID4')
]

# How many users to register out of the otherUser list
# Can never exceed 3
registerOthersCount = 3

# Default bodyprefix
bodyPrefix = [
    ('command', 'next'),
	('commandValue', ''),
]

# Default bodypostfix
bodyPostfix = [
    ('txtAttachedMessage', ''),
    ('txtExtraEmail', ''),
    ('txtExtraEmail', ''),
    ('txtExtraEmail', '')
]

# List of all golfclubs available via GolfBox
# Set the unique identifier as the value of the golfClubId variable
golfclubs = {
	"EA7782D7-DAB4-49DA-A09D-7A5A808633BC":"Golfklúbbur Akureyrar",
	"9EFBBF80-F5BE-42FD-A2DB-36BB511EB445":"Golfklúbbur Ásatúns",
	"7ED5FAEA-ACBB-4A43-999D-A3C023DA06AC":"Golfklúbbur Borgarness",
	"215D6C19-CA8A-47B6-8310-2ECF13C927EE":"Golfklúbbur Brautarholts",
	"E5D8A3C8-CB0D-4848-A821-11BD65EF4B93":"Golfklúbbur Fjallabyggðar",
	"BC3F5804-FA09-4A2E-A252-0FA18112EE90":"Golfklúbbur Grindavíkur",
	"97CDDD19-0A68-4CA5-9AC8-4236749E4A5E":"Golfklúbbur Hellu",
	"F03AAAB5-C76E-450A-9469-E0CC1FD69D76":"Golfklúbbur Hornafjarðar",
	"E1979B30-3880-4059-AB99-99A1425C8315":"Golfklúbbur Húsafells",
	"4CAADC07-7BFE-4A41-A6DE-CD1AF1A80127":"Golfklúbbur Húsavíkur",
	"5B68D091-81D9-44FA-A2E6-CB662E169D47":"Golfklúbbur Hveragerðis",
	"34FF0E44-676F-4B4B-9901-B4DDA8886095":"Golfklúbbur Kiðjabergs",
	"61D58E44-21EE-4614-A6C0-B37234B69C84":"Golfklúbbur Kópavogs og Garðabæjar",
	"59FE960B-100A-4D6A-8FEC-CA5FBFFEF385":"Golfklúbbur Mosfellsbæjar",
	"B8A0EA5F-6307-4EE6-B41A-9CE8911D9CD3":"Golfklúbbur Norðfjarðar",
	"CD9E8B4C-01BC-42AB-834E-FC2BE6871B8F":"Golfklúbbur Reykjavíkur",
	"F1ADA83F-C368-4881-9817-7C1B045ACC7A":"Golfklúbbur Sandgerðis",
	"1AF49B4D-499C-4C65-B86C-6408F4612D93":"Golfklúbbur Selfoss",
	"74A10E17-1CDE-4234-9D1A-FB8AFBBB7A55":"Golfklúbbur Siglufjarðar",
	"90E31435-0F0C-4EF3-9C11-1D6AAAD0510B":"Golfklúbbur Skagafjarðar",
	"0943B8CA-441E-4CEE-99CB-B502A13E3D32":"Golfklúbbur Skagastrandar",
	"3F6FD083-9D8C-4A5C-9E9D-083551376458":"Golfklúbbur Staðarsveitar",
	"2E1269E2-0145-4074-B37D-0386F184DCDE":"Golfklúbbur Suðurnesja",
	"2B36F72E-A77B-4801-8639-4F53F05FC2E5":"Golfklúbbur Þorlákshafnar",
	"60A58428-DCC2-4EF1-BD7C-1FCDE4F3BF06":"Golfklúbbur Vatnsleysustrandar",
	"A20FFB00-2A2C-4441-B554-EED1BDCBCABE":"Golfklúbbur Vestmannaeyja",
	"A30DDB2D-54FB-441E-A906-44793ACAB700":"Golfklúbburinn á Hellishólum",
	"075F8165-6B4E-4CD9-8075-3A3688A5E869":"Golfklúbburinn Dalbúi",
	"C3D3B9B4-4011-4893-92B2-C12DD48FF421":"Golfklúbburinn Flúðir",
	"4FB9C256-E8C7-46F5-897E-C3D52E10E948":"Golfklúbburinn Glanni",
	"03F948CF-9F0A-4ED3-A5F5-8A7B3E85B20C":"Golfklúbburinn Hamar Dalvík",
	"5E3A46CE-6B98-4B81-9A5E-592C39A6D3B0":"Golfklúbburinn Keilir",
	"91DD123D-E1E6-41DC-A96B-2C02AD374BDC":"Golfklúbburinn Leynir",
	"7D5D4AF3-2FF7-4A33-BF09-0050EEAADDC6":"Golfklúbburinn Lundur",
	"73B7A5D1-17A0-4F31-92E2-4A2AE29A1AA6":"Golfklúbburinn Mostri",
	"0CA7A186-060B-4338-85A5-C4776B9F7D4D":"Golfklúbburinn Oddur",
	"8D4871E0-E648-4023-90AF-B3A5BAB198FD":"Golfklúbburinn Ós",
	"3E42E51B-EF3D-4019-8ADE-5C010545E556":"Golfklúbburinn Setberg",
	"73DD5623-A182-4C60-B33E-70E7A27092F6":"Golfklúbburinn Úthlíð",
	"BD99A1B7-DB02-4045-B69F-7FC0CBC1BA30":"Golfklúbburinn Vestarr",
	"1690AE0C-BD20-4B85-A648-2B9EBB0AB05B":"Nesklúbburinn"
}

# Construction of body params is different for authenticated user than the others
def constructBodyParamsForAuthenticatedUser():
    authUserBodyParams = [
        ('gbMembers', '0'),
        ('guid_0', '%7B'+authUser[2]+'%7D'),
        ('GBDropDown_SelectedOption_ddlUnion_0', 'IS'),
        ('txt_MemberClubID_0', authUser[1]),
        ('hidden_BookingPrice_0_9Hole', '0'),
        ('hidden_BookingIsPaid_0', '0'),
        ('hidden_BookingPrice_0', '0')
    ]
    return authUserBodyParams

# Need to construct the NOT authenticated users body params differently
# Only the authentiacated one needs the interanl GUID the other simply use GolfBox ID.
def constructBodyParamsForOtherUsers(otherUsersList, registerOthersCount):
    otherUserList = []
    for i in range(0, registerOthersCount):
        otherUserList.append(('guid_'+str(i+1), ''))
        otherUserList.append(('chk_Favorite_1_'+str(i+1), 'on'))
        otherUserList.append(('GBDropDown_SelectedOption_ddlUnion_'+str(i+1), 'IS'))
        otherUserList.append(('chk_IsGuest_'+str(i+1), '0'))
        otherUserList.append(('txt_MemberClubID_'+str(i+1), ''))
        otherUserList.append(('txt_Name_+'+str(i+1), ''))
        otherUserList.append(('rdo_MemberType_'+str(i+1), 'M'))
        otherUserList.append(('txt_MemberHCP_'+str(i+1), ''))
        otherUserList.append(('txt_ClubName_'+str(i+1), ''))
        otherUserList.append(('chk_Favorite_2_'+str(i+1), 'on'))
        otherUserList.append(('ddl_Favorites_'+str(i+1), otherUsersList[i][2]))
        otherUserList.append(('txtSearchAble', str(i+1)))

    return otherUserList

def constructAllBodyParamsForRegistration(otherUsersList, registerOthersCount):
    authenticatedUser = constructBodyParamsForAuthenticatedUser()
    otherUsersBodyParams = constructBodyParamsForOtherUsers(otherUsersList, registerOthersCount)

    return bodyPrefix.__add__(authenticatedUser.__add__(otherUsersBodyParams)).__add__(bodyPostfix)

arrayAllUsers = constructAllBodyParamsForRegistration(otherUsersList, registerOthersCount)