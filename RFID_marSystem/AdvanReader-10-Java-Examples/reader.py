import subprocess
import time

# run java code
process = subprocess.Popen(["java", "-classpath", "bin:lib/slf4j-api-1.6.1.jar:lib/slf4j-simple-1.6.1.jar:lib/keonn-util.jar:lib/keonn-adrd.jar", "-Djava.library.path=./native-lib/linux-amd64", "com.keonn.adrd.ADRD_M1_10Asynch", "eapi:///dev/ttyUSB0"])

# run until desired angle is reached
time.sleep(5)

# then kill it
process.kill()

# read created file and put it on a dictionary key time and value a set of tags readed
time_epc = {}
with open('reader_output.txt') as f:
    for line in f:
        line_splitted = line.split(",")
        read_time = line_splitted[0]
        epc = line_splitted[1].replace("\n", "")
        if read_time not in time_epc.keys():
            time_epc[read_time] = set()
        time_epc[read_time].add(epc)


# get the epc of the tags readed
unique_epc = []
for epc_list in time_epc.values():
    for epc in epc_list:
        if epc not in unique_epc:
            unique_epc.append(epc)


# dictionary -> k: epc , v: avg time (when joining with angels it will make sense)
avg_epc = {}
for epc in unique_epc:
    in_times = []
    for item in time_epc.items():
        key = item[0]
        value = item[1]
        if epc in value:
            in_times.append(int(key))
    avg = sum(in_times) / len(in_times)
    avg_epc[epc] = avg

print("\nEPC : avg_time\n")
print("\n".join("{!r}: {!r}".format(k, v) for k, v in avg_epc.items()))