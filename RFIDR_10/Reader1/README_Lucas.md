# To build java when changes are made:
sudo javac -cp 'lib/*' -sourcepath ./src -d bin src/com/keonn/adrd/ADRD_M1_10Asynch.java

# To run program:
java -classpath bin:lib/slf4j-api-1.6.1.jar:lib/slf4j-simple-1.6.1.jar:lib/keonn-util.jar:lib/keonn-adrd.jar -Djava.library.path=./native-lib/linux-amd64 com.keonn.adrd.ADRD_M1_10Asynch eapi:///dev/ttyUSB0

# More information:
https://github.com/Keonn-Technologies/AdvanReader-10-Java-Examples