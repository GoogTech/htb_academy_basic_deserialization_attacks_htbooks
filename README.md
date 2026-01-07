It’s a Python web application that primarily focuses on code review, identifying deserialization vulnerabilities in the code, and demonstrating basic deserialization attack techniques. It's worth noting that they were developed as part of the HackTheBox Academy's `Introduction to Deserialization Attacks` module.

❗️❗️❗️Deserialization Attacks include:

* Object Injection (Payload in `/Exploit/Object_Injection`
* RCE: Magic(Special) Methods (Payload in `/Exploit/Remote_Code_Execution`

## How to run it
```shell
# 1.Install the sqlite3

# 2.Create the python venv
python3 -m venv venv

# 3.Install the python modules
python3 -m pip install -r requirements.txt

# 4.Run the web server
python3 -m flask run
```
