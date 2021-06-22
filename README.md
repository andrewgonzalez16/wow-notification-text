# wow-notification-text
This repository will host my World of Warcraft notification code.
This code requires pytesseract to be installed prior to running the code. You can download Pytesseract at https://pypi.org/project/pytesseract/
This python script uses pytesseract to evaluate text from a screenshot and send a notification (e.g. a text message) to the user when your World of Warcraft battleground/arena notification pops up. This is particularly useful for times when battleground queues are 10-20 minutes long and you want to step away from your computer, or really any other time you need to step away from your computer, but want to make sure you don't miss your queue popping! 

***IMPORTANT NOTE: because this script is working off of pytesseract OCR (aka screenshots) it does require that World of Warcraft is the forefront window. Thus this script is mainly to be used for cases where you need to step away from the computer as opposed to switching windows/tabbing out of World of Warcraft.
