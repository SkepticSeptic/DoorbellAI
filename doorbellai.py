import jetson.inference
import jetson.utils
import smtplib, ssl
import time

#quick definition to take user input for several things such as email, place, and whatever else i decide to use it for
def verification(whatis, addmessage=" "): #yes i know my variable naming is super inconsistent :(
    confirmed = 'not confirmed'
    while confirmed != 'y':
        userinput = input("input " + whatis + " " + addmessage)
        confirmed = input("is '"+ userinput + "' your " + whatis + "? (type 'y' & enter to confirm or any other key to try again)")
        if confirmed != 'y':
            print("Okay, lets try again:")
    print(whatis + " successfully added: ")
    return userinput


#variables, sender email is a default email. change it if it gets overloaded from people using it (as if)
DBAIEmail = 'doorbellai01@gmail.com'
emailPass = 'defaultpassword' #(dont change this variable, its synced to the actual gmail acc)
#email holding

#ask for stuff needed for email (recieving email, subject, message, & place)
userEmail = verification('email', 'to recieve alerts on: ') #email user will recieve alerts on
subj = verification('subject', 'to title email') #email subject
message = verification('email message', 'to be alerted by: ') #email message/body text
place = verification('camera location', '(where is this camera located?)')
message = message + '     (camera location:' + place + ')'
cooldown = verification('cooldown', '(how long should the camera wait for after\ndetecting a person? [ENTER IN SECONDS])')

date='2/22/22' #just messing around here

#establishing server variable
server = smtplib.SMTP('smtp.mail.yahoo.com',587) 
msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % ( DBAIEmail, userEmail, subj, date, message )
print("email setup complete!\nstarting detectmodel...")

#initiate detectnet model
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
#initiate camera
camera = jetson.utils.videoSource("/dev/video0") # 
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file
print("System ready!\nPausig for 3 minutes to prevent faulse alarms...")
time.sleep(180)

#cam feed:
while display.IsStreaming():
	img = camera.Capture()
	detections = net.Detect(img)
	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
	#if person detected, send email:
	for detection in detections:
		class_name = "reset" #resets variable to prevent false alarms
		class_name = net.GetClassDesc(detection.ClassID)
		print(f"Detected '{class_name}'")
		if (class_name == "person"):
			print("WARN: Person detected, attempting to send email:")
			try:
				print("email setup in progress, logging into server... ")
				server.login(DBAIEmail, emailPass) # connects to server
				print("attempting to send email...")
				server.sendmail(DBAIEmail, userEmail, msg) # actually sending notification
				print("ALERT: Email sent successfully")
				print("logging out of email...")
				server.quit() # logs out
				print("logged out.\npasuing script for 10 minutes...")
				time.sleep(600)
			except:
        #error message
				print("Error: Exception occurred. Likely a problem in the script itself") 
