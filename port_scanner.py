from datetime import datetime
import socket
import platform  # getting OS name
import subprocess  # to execute shell command

# socket.AF_INET = IP4, socket.SOCK_STREAM = TCP connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# returns true if port is open
def is_port_open(port):
    try:
        con = s.connect((host, port))
        return True
    except:
        return False


# scan all ports from 1 to 1025 and write open ports to file port_scanner_results.txt
def scan_ports():
    for x in range(130, 140):
        if is_port_open(x):
            file = open("port_scanner_results.txt", "a+")
            file.write("Port %s is OPEN\n" % (x))
            file.close()
            print("Port ", x, "is OPEN")
        else:
            print("Port ", x, "is NOT OPEN")


# ping host to check connection and print any errors to file port_scanner_results.txt
def ping(host):
    print("Pinging host to check connection...")
    param = "-n" if platform.system().lower() == 'windows' else 'c'
    command = ['ping', param, '1', host]
    text = subprocess.Popen(command, stdout=subprocess.PIPE)
    out = text.communicate()[0].decode("utf-8")
    lower_output = out.lower()

    if lower_output.find("destination host unreachable") > 0:
        file = open("port_scanner_results.txt", "a")
        file.write("Destination Host Unreachable\n")
        file.close()
        print("Unable to scan. Destination Host Unreachable")
    elif lower_output.find("ttl expired in transit") > 0:
        file = open("port_scanner_results.txt", "a")
        file.write("TTL Expired in Transit\n")
        file.close()
        print("Unable to scan. TTL Expired in Transit")
    elif lower_output.find("request timed out") != -1:
        file = open("port_scanner_results.txt", "a")
        file.write("Request Timed Out\n")
        file.close()
        print("Unable to scan. Request Timed Out")
    elif lower_output.find("could not find host") > 0:
        file = open("port_scanner_results.txt", "a")
        file.write("Could Not Find Host\n")
        file.close()
        print("Unable to scan. Could Not Find Host")
    elif lower_output.find("0% loss") > 0:
        print("Connection established. Starting Scan...")
        scan_ports()


# begin program
host = input("Enter a host to scan: ")
start_time = datetime.now()
print("Start Time: ", datetime.now().strftime("%m/%d/%y %H:%S:%M"))

ping(host)

end_time = datetime.now()
totalTime = end_time - start_time
print("End Time: ", datetime.now().strftime("%m/%d/%y %H:%S:%M"))
print("Total Time Elapsed: ", totalTime)
print("Results have been saved to: port_scanner_results.txt")
