import pandas as pd
import pyautogui #responsible for taking screenshots
from PIL import Image #responsible for image manipulation and open and replacing
from datetime import datetime #used to get current time
import pytesseract
import time

'''################################################################
newRound is the text we look for on the screen to see if its a new round
endResult is the text we use to close a new round to csv file
phase is for the folder structure - you can leave this variable out
since the software is always running, we allowNewRow and allowEditinfOfRow for error corrections
meaning we only enter values once
################################################################'''
newRound = 'WAITING FOR NEXT ROUND'
endResult = 'FLEW AWAY'
dataFile = pd.DataFrame(columns=["Date","Start Time","End Time","Total Bets","Value"])
phase = "phase6"
allowNewRow = True
allowEditingOfRow = True

'''################################################################
depending on what loop you want to use (time for time and for date), 
this is variable to stop the system automatically
################################################################'''
#c = datetime.now().time()
c = datetime.now().date()
resultFileName = f"results_{c}.csv"

'''################################################################
the +1 indicate a added time to stop the loop
for newDate is for the next day and newTime is the next minute
################################################################'''
#newTime = f"{str(c)[0]}{str(c)[1]}{str(c)[2]}{str(c)[3]}{str(int(str(c)[4])+1)}"
newDate = f"{str(c)[0:8]}{int(str(c)[8:10])+1}"


'''################################################################
i use this to check the new date or time
################################################################'''
#print(f'{datetime.now().date()}_{datetime.now().time()}')
#print(newDate + "\n" + str(c)[0:10])

'''################################################################
i use the sleep to add a 10sec delay to allow you to swap between screens/applications
the for loop is for testing increase you dont want to use the time or date
the while loop is for time or date loop
################################################################'''

time.sleep(10)
#for i in range(0,50):
while str(c)[0:10] != newDate:
	#nameOfFile uses the current date and time to give each screenshot a name
	nameOfFile = f'{datetime.now().date()}_{str(datetime.now().time()).replace(":","-").replace(".","-")}'
	#region, the first two numbers arre for the screen location and the last2 are for the photo dimensions
	ss = pyautogui.screenshot(f"C:\\Users\\Administrator\\Desktop\\screenshotsOfBetway\\{phase}\\{nameOfFile}.png",region=(675,350,350,150))
	totalBetsScreenshots = pyautogui.screenshot(f"C:\\Users\\Administrator\\Desktop\\screenshotsOfBetway\\{phase}\\{nameOfFile}-totalbets.png",region=(0,350,50,50))
	
	# update the date variable so it stops when the time matches what you want, it stops
	c = datetime.now().date()
	time.sleep(1)

	#image of the total score
	binaryImage = Image.open(f"C:\\Users\\Administrator\\Desktop\\screenshotsOfBetway\\{phase}\\{nameOfFile}.png")
	#binaryImage = Image.open("C:\\Users\\Administrator\\Desktop\\screenshotsOfBetway\\phase5\\2024-07-20_20-03-44-134215.png")
	binaryImage = binaryImage.point(lambda p: 255 if p < 128 else 0)
	newImage = pytesseract.image_to_string(binaryImage).strip()
	lengthOfDataframe = len(dataFile)

	#image of the total bet score
	binaryImageTotalBets = Image.open(f"C:\\Users\\Administrator\\Desktop\\screenshotsOfBetway\\{phase}\\{nameOfFile}-totalbets.png")
	#binaryImageTotalBets = Image.open("C:\\Users\\Administrator\\Desktop\\screenshotsOfBetway\\phase5\\2024-07-20_20-03-42-174387-totalbets.png")
	binaryImageTotalBets = binaryImageTotalBets.convert('L').point(lambda p: 255 - p)
	newImageOfTotalBets = pytesseract.image_to_string(binaryImageTotalBets).strip()

	#initialize the first row of empty data if it is a new round
	if lengthOfDataframe == 0:
	newRow = pd.DataFrame({'Date': c,'Start Time': datetime.now().time(),'Value': 0},index=[0])
	dataFile = pd.concat([dataFile,newRow])
	print("initialize the first row of empty data if it is a new round")

	#responsible for setting up new rounds    
	if newRound in newImage:
		if allowNewRow == True:
		    #new empty row if it is a new round on existing dataframe
		    newRow = pd.DataFrame({'Date': c,'Start Time': datetime.now().time(),'Value': 0},index=[lengthOfDataframe])
		    time.sleep(1)
		    dataFile = pd.concat([dataFile,newRow])
		    allowEditingOfRow = True
		    allowNewRow = False
		    print("NEW ROUND")
		    
	#responsible for closing of rounds        
	if endResult in newImage:
	workingNumber=''
	workingNumberTotalBets=''

		#filter screenshot of total bet and get the number
		for n in newImage.replace(" ",""):
		    if n.isdigit() or n == ".":
			workingNumber+=n
		#filter screenshot of total bet and get the number
		for b in newImageOfTotalBets.replace(" ",""):
		    if b.isdigit() or b == ".":
			workingNumberTotalBets+=b
		#adds everything into a dataframe row

		if allowEditingOfRow == True:
		    dataFile.loc[lengthOfDataframe-1, ["End Time","Total Bets","Value"]] = [datetime.now().time(), workingNumberTotalBets, workingNumber]
		    dataFile.to_csv(f"C:\\Users\\Administrator\\Desktop\\screenshotsOfBetway\\{resultFileName}",index=False)
		    allowEditingOfRow = False
		    allowNewRow = True
		    print("NEW ENTRY")
        
