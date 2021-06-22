import time
import re
import email
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PIL import ImageGrab
from PIL import ImageEnhance
from playsound import playsound
# Requirement is that you have pytesseract installed
import pytesseract

#Below add the path to where 'pytesseract' is installed:
pytesseract.pytesseract.tesseract_cmd = r"<Path to 'tesseract.exe' Goes Here>"

#Add your phone number as a string:
phoneNumber = ''
recipientEmailAddress = ""
# Add an email from which you want the text to come from, but you must know the credentials:
senderEmailAddress = 'example@example.com'
# Enter the credentials for your email:
emailPassword = ''
# Enter your cellphone's carrier service.
carrierService = 'verizon'

# Carrier Dictionary for the most common networks in the US. Feel free to add your carrier if it's not listed.
# If you do not see/know what the suffix of your carrier's email to text email is then Google it.
carrierDict = {
    'att&t' : '@txt.att.net',
    'verizon' : '@vtext.com',
    't-mobile' : '@tmomail.net',
    'sprint' : '@messaging.sprintpcs.com',
    'mint mobile' : '@tmomail.net'
}


# We don't care about everything on the screen, but rather just a small cropped portion of the screen shot which is the in-game notifcation popup alert
# The reason we don't want to extract the whole screen is because parsing unnecessary other text could easily interfere with the desired result.
# The following def was used to configure what part of the screen the pytesseract is capturing. 
# Every screen/monitor size can vary and so you can run this def configureSS() independently to see and adjust accordingly so it only captures the necessary part of the screen
# Uncomment the debug statements and add break points for easy visualization and debugging.
def configureSS():

    img = ImageGrab.grab()
    #img.show()
    width, height = img.size
    xcenter = width/2
    ycenter = height/2
    #print(f'Here are the center points:\nHorizontal Center: {xcenter} \nVertical Center: {ycenter}')
    x1 = xcenter - 200
    y1 = 0
    x2 = xcenter + 200
    y2 = height * (1/(3.5))
    img = img.crop((x1,y1,x2,y2))
    #img.show()

# Function will prep the imaage for image recogniziton:
# Image preperation includes turning the image to black and white:
def get_queue_popped(img):
    width, height = img.size
    xcenter = width / 2
    ycenter = height / 2
    x1 = xcenter - 200
    y1 = 0
    x2 = xcenter + 200
    y2 = height * (1 / (3.5))
    img = img.crop((x1, y1, x2, y2))
    #img.show()
    img = img.point(lambda p: p > 128 and 255)
    #img.show()
    img = ImageEnhance.Color(img).enhance(0)
    #img.show()

    imagedata = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    imgtext = ''.join([x for i, x in enumerate(imagedata['text']) if int(imagedata['conf'][i]) >= 70])
    # Below is what we're searching the image for. In this example we're searching for the following strings:
    # 'isready','leavequeue', with any character(s) proceeding those strings. Feel free to modify this
    queueReady = re.search('isready|isready$|leavequeue|leavequeue$', imgtext, re.IGNORECASE)
    if queueReady:
        #print(f"here is the text {queueReady.group(0)}")
        return queueReady

def send_alert(alarm=True,email=False,playSound=False):

    if alarm:
        print(chr(7))

    if email:
        # set up the SMTP server
        smtp_server = "smtp.gmail.com"
        port = 587
        context = ssl.create_default_context()
        try:
            emailserver = smtplib.SMTP(smtp_server, port)
            emailserver.starttls(context=context)
            emailserver.login(senderEmailAddress, emailPassword)
        except Exception as e:
            print(e)

        # set up the message
        msg = MIMEMultipart()
        msg['From'] = senderEmailAddress
        # Checking for proper phone number length:
        validNumber = False
        if len(phoneNumber) < 10 or len(phoneNumber) > 11:
            validNumber = False
            recipient = recipientEmailAddress
        if len(phoneNumber) == 10:
            if carrierService.lower() == 't-moble' or carrierService.lower() == 'mint mobile':
                formattedNumber = str (1) + phoneNumber

            else:
                formattedNumber = phoneNumber

            validNumber = True

        if validNumber:
            try:
                carrierGateway = carrierDict[carrierService.lower()]
                recipient = formattedNumber + carrierGateway
                # print(f'here is the selected carrier service: {carrierGateway}')
            except:
                print("SMS notification because service provider gateway not found.")
                validNumber = False
                recipient = recipientEmailAddress


        msg['To'] = recipient
        # Add Custom Subject here:
        msg['Subject'] = "Time to WoW!"
        # Add Custom Message here:
        message = 'Your WoW queue is has popped!'
        msg.attach(MIMEText(message, 'plain'))
        # send the message
        emailserver.send_message(msg)
        print(f'Email notification sent to {recipient}')
        emailserver.quit()

    if playSound:
        soundFile = "<path to song file>"
        playsound(soundFile)


def queue_alert(interval=2, occurrences=3, alarm=True, emailAlert=True, playSound=False):

    counter = 0
    while True:
        # First we'll grab a screenshot every x seconds, where x = interval passed in:
        time.sleep(interval)
        img = ImageGrab.grab()
        #img.show()
        queuePopped = get_queue_popped(img)
        if not queuePopped:
            print ('Could not extract queue!')
        else:
            counter += 1
            # We use 'occurrences' to ensure that screenshot has been processed successfully at least x number of times
            # Where x = occurrences
            if counter >= occurrences:
                print ('Queue has popped!')
                send_alert(alarm=alarm,email=emailAlert,playSound=playSound)
                emailAlert = False
                break
        # The following lines will stop the alarm after 5 alarms:
        if counter > 5:
            break

# @interval is used to set how often a screenshot will be captured and assessed in seconds
# @occurances is used to set how many times the notification code should be run once it hits a valid case (Aka how many text/emails/alerts you will get when a valid case is met).
# @alarm, @emailAlert, and @playSound is a boolean used to determine what block of code to run inside the def send_alert(). 
queue_alert(interval=.5, occurrences=1, alarm=False, emailAlert=True, playSound=False)
#configureSS()

