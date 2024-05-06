import subprocess
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from reader_msg.msg import Reader10Msg

class NumberPublisherNode(Node):
    def __init__(self):
        super().__init__('Readers_node')
        self.publisher_ = self.create_publisher(Reader10Msg, 'Readers_readings', 1)
        self.timer_ = self.create_timer(0.5, self.publish_number)
        self.antenna_left_id = 1
        self.antenna_right_id = 2
        self.unique_epcs = []
        self.epcs = []
        self.unique_numtags = 0
        self.count_all_tags = 0

        # run java code

        # run until desired angle is reached
        # time.sleep(5)

        # then kill it
        # process.kill()


    def publish_number(self):
        process1 = subprocess.Popen(["sudo","java", "-classpath", "bin:lib/slf4j-api-1.6.1.jar:lib/slf4j-simple-1.6.1.jar:lib/keonn-util.jar:lib/keonn-adrd.jar", "-Djava.library.path=./native-lib/linux-amd64", "com.keonn.adrd.ADRD_M1_10Asynch", "eapi:///dev/ttyUSB0"], cwd="/home/lybot/ros2_lybot/src/RFIDR_10/Reader1")
        process2 = subprocess.Popen(["sudo","java", "-classpath", "bin:lib/slf4j-api-1.6.1.jar:lib/slf4j-simple-1.6.1.jar:lib/keonn-util.jar:lib/keonn-adrd.jar", "-Djava.library.path=./native-lib/linux-amd64", "com.keonn.adrd.ADRD_M1_10Asynch", "eapi:///dev/ttyUSB1"], cwd="/home/lybot/ros2_lybot/src/RFIDR_10/Reader2")
        time.sleep(2)
        process1.kill()
        process2.kill()

        # Read number and name from file
        tags_antenna1, self.count_all_tags, count_unique_tag  = self.read_from_file(self.antenna_left_id)
        tags_antenna2, self.count_all_tags, count_unique_tag= self.read_from_file(self.antenna_right_id)

        # Create message
        # msg = String()
        # msg.data = f"Num Tags: {number1}, Name: {name1}, Num Tags: {number2}, Name: {name2}"
        msg = Reader10Msg()
        msg.reader_id = "AdvanReader-10-1, AdvanReader-10-2"
        msg.antenna1_numtags[0] = self.antenna_left_id
        msg.antenna1_numtags[1] = tags_antenna1
        msg.antenna2_numtags[0] = self.antenna_right_id
        msg.antenna2_numtags[1] = tags_antenna2
        msg.numtotaltags = (self.count_all_tags)
        msg.unique_numtotaltags = count_unique_tag
        msg.goal_dir = self.choose_goal_dir(tags_antenna1, tags_antenna2)
        msg.epcs_detected[0] = str(tags_antenna1 + tags_antenna2)
        msg.epcs_detected[1] = str(self.epcs)

        # Publish message
        self.publisher_.publish(msg)

    def choose_goal_dir(self, number1, number2):
        if (number1>0 and number2>0) or (number1 == number2 ==0):
            return "Forward" 
        elif (number1>0 and number2==0) or number1>number2:
            return "Left"
        elif (number2>0 and number1==0) or number2>number1:
            return "Right"
        
        
    def read_from_file(self, antenna):
        # Read number and name from file

        # read created file and put it on a dictionary key time and value a set of tags readed
        time_epc = {}
        if antenna == 1:
            path = 'Reader1/reader_output.txt'
        else:
            path = 'Reader2/reader_output.txt'

        with open(path) as f:
            for line in f:
                line_splitted = line.split(",")
                read_time = line_splitted[0]
                epc = line_splitted[1].replace("\n", "")
                if read_time not in time_epc.keys():
                    time_epc[read_time] = set()
                time_epc[read_time].add(epc)



        # get the epc of the tags readed
        unique_counter=0
        unique_total_numtags = 0
        unique_epc = []
        semi_unique_epc = []
        path2 = 'total_tags.txt'
        with open(path2) as f:
            for line in f:
                epc_fromtotal = line.replace("\n", "")
                unique_total_numtags +=1
                self.unique_epcs.append(epc_fromtotal)
        
        semi_unique_counter=0
        for epc_list in time_epc.values():
            for epc in epc_list:
                self.epcs.append(epc)
                self.count_all_tags+=1
                if epc not in unique_epc:
                    # semi_unique_counter+=1    
                    semi_unique_epc.append(epc)
                    semi_unique_counter=int(len(semi_unique_epc)/10)

                    if epc not in self.unique_epcs:
                        unique_epc.append(epc)
                        unique_counter+=1
                        f = open("total_tags.txt", "a")
                        f.write(epc + "\n")
                        f.close()
        

        # dictionary -> k: epc , v: avg time (when joining with angels it will make sense)
        # avg_epc = {}
        # for epc in semi_unique_epc:
        #     in_times = []
        #     for item in time_epc.items():
        #         key = item[0]
        #         value = item[1]
        #         if epc in value:
        #             in_times.append(int(key))
        #     avg = sum(in_times) / len(in_times)
        #     avg_epc[epc] = avg

        # print("\nEPC : avg_time\n")
        # print("\n".join("{!r}: {!r}".format(k, v) for k, v in avg_epc.items()))
        # print("Total unique tags in 1Sec are: ")
        # print(unique_counter)
    
        #replace semi_unique_counter to unique_counter for only navigating with new unique detected tags
        return semi_unique_counter, self.count_all_tags, unique_total_numtags

def main(args=None):
    rclpy.init(args=args)
    number_publisher_node = NumberPublisherNode()
    rclpy.spin(number_publisher_node)
    number_publisher_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

