<<<<<<< HEAD
# -*- coding: utf-8 -*-
__author__ = "Pranav Sakulkar, Jiatong Wang, Pradipta Ghosh, Quynh Nguyen, Bhaskar Krishnamachari"
__copyright__ = "Copyright (c) 2018, Autonomous Networks Research Group. All rights reserved."
__license__ = "GPL"
__version__ = "1.0"

=======
"""
 * Copyright (c) 2018, Autonomous Networks Research Group. All rights reserved.
 *     contributors: 
 *      Pranav Sakulkar
 *      Jiatong Wang
 *      Pradipta Ghosh
 *      Bhaskar Krishnamachari
 *     Read license file in main directory for more details  
"""

# -*- coding: utf-8 -*-
>>>>>>> 2421ba79d8b7968b8be5a8f9d9c3c9e970da8498

import json
import random
import re
import threading
import time
import os
import sys
import urllib
<<<<<<< HEAD

=======
from urllib import parse
>>>>>>> 2421ba79d8b7968b8be5a8f9d9c3c9e970da8498
import shutil

import _thread
from flask import Flask, request
import requests
import datetime
from pymongo import MongoClient

app = Flask(__name__)

<<<<<<< HEAD

def prepare_global():
    """Prepare global information (Node info, relations between tasks)
    """
    # Get ALL node info
    node_count = 0
    nodes = {}
    for node_name, node_ip in zip(os.environ['ALL_NODES'].split(":"), os.environ['ALL_NODES_IPS'].split(":")):
        if node_name == "":
            continue
        nodes[node_name] = node_ip + ":48080"
        node_count +=  1
    master_host = os.environ['HOME_IP'] + ":48080"
    print("Nodes", nodes)

    #
    node_id = -1
    node_name = ""
    debug = True

    # control relations between tasks
    control_relation = {}

    local_children = "local/local_children.txt"
    local_mapping = "local/local_mapping.txt"
    local_responsibility = "local/task_responsibility"

    # lock for sync file operation
    lock = threading.Lock()

    kill_flag = False


#@app.route('/assign_task')
def assign_task():
    """Summary
    
    Returns:
        TYPE: Description
    """
=======
'''

'''

# Get ALL node info
node_count = 0
nodes = {}
for node_name, node_ip in zip(os.environ['ALL_NODES'].split(":"), os.environ['ALL_NODES_IPS'].split(":")):
    if node_name == "":
        continue
    nodes[node_name] = node_ip + ":48080"
    node_count +=  1
master_host = os.environ['HOME_IP'] + ":48080"
print("Nodes", nodes)

#
node_id = -1
node_name = ""
debug = True

# control relations between tasks
control_relation = {}

local_children = "local/local_children.txt"
local_mapping = "local/local_mapping.txt"
local_responsibility = "local/task_responsibility"

# lock for sync file operation
lock = threading.Lock()

kill_flag = False


@app.route('/assign_task')
def assign_task():
>>>>>>> 2421ba79d8b7968b8be5a8f9d9c3c9e970da8498
    try:
        task_name = request.args.get('task_name')
        write_file(local_responsibility + "/" + task_name, [], "w+")
        return "ok"
    except Exception:
        return "not ok"
<<<<<<< HEAD
app.add_url_rule('/assign_task', 'assign_task', assign_task)

#@app.route('/kill_thread')
def kill_thread():
    """assign kill thread as True
    """
    global kill_flag
    kill_flag = True
    return "ok"
app.add_url_rule('/kill_thread', 'kill_thread', kill_thread)

def init_folder():
    """Initialize folders (``local``,``local_responsibility``), prepare ``local_children`` and ``local_mapping`` file.
    
    Raises:
        Exception: ``ok`` if successful, ``not ok`` otherwise
    """
=======


@app.route('/kill_thread')
def kill_thread():
    global kill_flag
    kill_flag = True
    return "ok"


def init_folder():
>>>>>>> 2421ba79d8b7968b8be5a8f9d9c3c9e970da8498
    print("Trying to initialize folders here")
    try:
        if not os.path.exists("./local"):
            os.mkdir("./local")

        if not os.path.exists(local_children):
            write_file(local_children, [], "w+")

        if not os.path.exists(local_mapping):
            write_file(local_mapping, [], "w+")

        if not os.path.exists(local_responsibility):
            os.mkdir(local_responsibility)
        return "ok"
    except Exception:
        print("Init folder fialed: Why??")
        return "not ok"


<<<<<<< HEAD
#@app.route('/recv_control')
def recv_control():
    """Get assigned control function, prepare file ``DAG/parent_controller.txt`` storing parent control information of tasks 
    
    Raises:
        Exception: ``ok`` if successful, ``not ok`` otherwise
    """
=======
@app.route('/recv_control')
def recv_control():
>>>>>>> 2421ba79d8b7968b8be5a8f9d9c3c9e970da8498
    try:
        control = request.args.get('control')
        items = re.split(r'#', control)

        to_be_write = []
        for _, item in enumerate(items):
            to_be_write.append(item.replace("__", "\t"))
            tmp = re.split(r"__", item)
            key = tmp[0]
            del tmp[0]
            control_relation[key] = tmp

        if not os.path.exists("./DAG"):
            os.mkdir("./DAG")

        write_file("DAG/parent_controller.txt", to_be_write, "a+")
    except Exception:
        return "not ok"
    return "ok"
<<<<<<< HEAD
app.add_url_rule('/recv_control', 'recv_control', recv_control)


def assign_task_to_remote(assigned_node, task_name):
    """Assign task to remote node
    
    Args:
        assigned_node (str): Node to be assigned
        task_name (str): task name 
    
    Raises:
        Exception: request if successful, ``not ok`` if failed
    """
    try:
        url = "http://" + nodes[assigned_node] + "/assign_task"
        params = {'task_name': task_name}
        params = urllib.parse.urlencode(params)
=======


def assign_task_to_remote(assigned_node, task_name):
    try:
        url = "http://" + nodes[assigned_node] + "/assign_task"
        params = {'task_name': task_name}
        params = parse.urlencode(params)
>>>>>>> 2421ba79d8b7968b8be5a8f9d9c3c9e970da8498
        req = urllib.request.Request(url='%s%s%s' % (url, '?', params))
        res = urllib.request.urlopen(req)
        res = res.read()
        res = res.decode('utf-8')
    except Exception:
        return "not ok"
    return res


def call_send_mapping(mapping, node):
<<<<<<< HEAD
    """
    - A function that used for intermediate data transfer.
    - Return mapping information for specific node.
    
    Args:
        mapping (dict): mapping information (task-assigned node)
        node (str): node name
    
    Raises:
        Exception: request if successful, ``not ok`` if failed
    """
    try:
        url = "http://" + master_host + "/recv_mapping"
        params = {'mapping': mapping, "node": node}
        params = urllib.parse.urlencode(params)
=======
    try:
        url = "http://" + master_host + "/recv_mapping"
        params = {'mapping': mapping, "node": node}
        params = parse.urlencode(params)
>>>>>>> 2421ba79d8b7968b8be5a8f9d9c3c9e970da8498
        req = urllib.request.Request(url='%s%s%s' % (url, '?', params))
        res = urllib.request.urlopen(req)
        res = res.read()
        res = res.decode('utf-8')
    except Exception as e:
        return "not ok"
    return res


<<<<<<< HEAD

def watcher():
    """- thread to watch directory: ``local/task_responsibility``
       - Write tasks to `local/local_children.txt` and `local/local_mapping.txt` that appear under the watching folder
    """
=======
# thread to watch directory: local/task_responsibility
def watcher():
>>>>>>> 2421ba79d8b7968b8be5a8f9d9c3c9e970da8498
    pre_time = time.time()

    tmp_mapping = ""
    while True:
        if kill_flag:
            break

        if not os.path.exists(local_responsibility):
            time.sleep(1)
            continue

        tasks = scan_dir(local_responsibility)
        output("Find tasks under task_responsibility: " + json.dumps(tasks))
        for _, task in enumerate(tasks):
            if task in control_relation.keys():
                controlled = control_relation[task]
                for _, t in enumerate(controlled):
                    todo_task = t + "\tTODO"
                    write_file(local_children, [todo_task], "a+")
                    output("Write content to local_children.txt: " + todo_task)

                write_file(local_mapping, [task], "a+")
                if tmp_mapping != "":
                    tmp_mapping = tmp_mapping + "#"
                tmp_mapping = tmp_mapping + task

                output("Write content to local_mapping.txt: " + task)
            else:
                write_file(local_mapping, [task], "a+")
                if tmp_mapping != "":
                    tmp_mapping = tmp_mapping + "#"
                tmp_mapping = tmp_mapping + task

                output("Write content to local_mapping.txt: " + task)

        shutil.rmtree(local_responsibility)
        os.mkdir(local_responsibility)

        if time.time() - pre_time >= 60:
            if tmp_mapping != "":
                res = call_send_mapping(tmp_mapping, node_name)
                if res != "ok":
                    output("Send mapping content to master failed");
                else:
                    tmp_mapping = ""

            pre_time = time.time()

        time.sleep(10)


<<<<<<< HEAD

def distribute():
    """thread to assign todo task to remote nodes
    """
=======
# thread to assign todo task to nodes
def distribute():
>>>>>>> 2421ba79d8b7968b8be5a8f9d9c3c9e970da8498
    done_dict = set()
    while True:
        if kill_flag:
            break

        if not os.path.exists(local_children):
            time.sleep(1)
            continue

        lines = read_file(local_children)
        for line in lines:
            line = line.strip()
            if "TODO" in line:
                output("Find todo item: " + line)
                tmp_node_id = random.randint(1, node_count)
                while tmp_node_id == node_id and node_count > 1:
                    tmp_node_id = random.randint(1, node_count)

                assign_to_node = "node" + str(tmp_node_id)
                items = re.split(r'\t+', line)
                if items[0] in done_dict:
                    print(items[0], "already assigned")
                    continue

                print("Trying to assign", items[0], "to", assign_to_node)
                status = assign_task_to_remote(assign_to_node, items[0])
                if status == "ok":
                    output("Assign " + items[0] + " to " + assign_to_node + " successfully")
                    done_dict.add(items[0])
                else:
                    output("Assign " + items[0] + " to " + assign_to_node + " failed")

        time.sleep(10)


def scan_dir(directory):
<<<<<<< HEAD
    """Scan the directory, append all file names to list ``tasks``
    
    Args:
        directory (str): directory path
    
    Returns:
        list: tasks - List of all file names in the directory
    """
=======
>>>>>>> 2421ba79d8b7968b8be5a8f9d9c3c9e970da8498
    tasks = []
    for file_name in os.listdir(directory):
        tasks.append(file_name)
    return tasks


<<<<<<< HEAD

def create_file():
    """Do nothing/ pass
    """
=======
def create_file():
>>>>>>> 2421ba79d8b7968b8be5a8f9d9c3c9e970da8498
    pass


def write_file(file_name, content, mode):
<<<<<<< HEAD
    """Write the content to file
    
    Args:
        file_name (str): file path
        content (str): content to be written
        mode (str): write mode 
    """
=======
>>>>>>> 2421ba79d8b7968b8be5a8f9d9c3c9e970da8498
    lock.acquire()
    file = open(file_name, mode)
    for line in content:
        file.write(line + "\n")
    file.close()
    lock.release()


<<<<<<< HEAD
def read_file(file_name):
    """get all lines in a file
    
    Args:
        file_name (str): file path
    
    Returns:
        str: file_contents - all lines in a file
    """
=======
# get all lines in a file
def read_file(file_name):
>>>>>>> 2421ba79d8b7968b8be5a8f9d9c3c9e970da8498
    lock.acquire()
    file_contents = []
    file = open(file_name)
    line = file.readline()
    while line:
        file_contents.append(line)
        line = file.readline()
    file.close()
    lock.release()
    return file_contents


def output(msg):
<<<<<<< HEAD
    """if debug is True, print the msg
    
    Args:
        msg (str): message to be printed
    """
    if debug:
        print(msg)


def get_resource_data():
    """Collect resource profiling information
    """
=======
    if debug:
        print(msg)

@app.route('/')
def hello_world():
    return 'Hello World!'

def get_resource_data():
>>>>>>> 2421ba79d8b7968b8be5a8f9d9c3c9e970da8498
    print("Startig resource profile collection thread")
    # Requsting resource profiler data using flask for its corresponding profiler node
    RP_PORT = 6100
    result = None
    while True:
        time.sleep(60)
        # print("Get resource profiler data from http://"+os.environ['PROFILER']+ ":" + str(RP_PORT))
        try:
            r = requests.get("http://"+os.environ['PROFILER']+":" + str(RP_PORT)+"/all")
            result = r.json()
            if len(result) != 0:
                break
        except Exception:
            print("Resource request failed. Will try again")

    data=json.dumps(result)
    print("Got profiler data from http://"+os.environ['PROFILER']+ ":" + str(RP_PORT))
    print("Resource profiles:", data)

def get_network_profile_data():
<<<<<<< HEAD
    """Collect the network profile from local MongoDB peer
    """
=======
>>>>>>> 2421ba79d8b7968b8be5a8f9d9c3c9e970da8498
    # Collect the network profile from local MongoDB peer
    print('Collecting Netowrk Monitoring Data from MongoDB')
    NP_PORT = 6200
    client_mongo = MongoClient('mongodb://'+os.environ['PROFILER']+':'+str(NP_PORT)+'/')
    db = client_mongo.droplet_network_profiler
    print(db[os.environ['PROFILER']])

<<<<<<< HEAD
def main():
    """
        - Prepare global information
        - Initialize folders (``local``,``local_responsibility``), prepare ``local_children`` and ``local_mapping`` file.
        - Start thread to get resource profiling data
        - Start thread to get network profiling data
        - Start thread to watch directory: ``local/task_responsibility``
        - Start thread to thread to assign todo task to nodes
    """

    prepare_global()
    
=======
if __name__ == '__main__':
>>>>>>> 2421ba79d8b7968b8be5a8f9d9c3c9e970da8498
    node_name = os.environ['SELF_NAME']
    node_id = int(node_name.split("e")[-1])

    node_port = sys.argv[1]
    print("Node name:", node_name, "and id", node_id)
    print("Starting the main thread on port", node_port)

    while init_folder() != "ok": # Initialize the local folders
        pass

    # Get resource data
    _thread.start_new_thread(get_resource_data, ())

    # Get network profile data
    _thread.start_new_thread(get_network_profile_data, ())

    _thread.start_new_thread(watcher, ())
    _thread.start_new_thread(distribute, ())
<<<<<<< HEAD
    app.run(host='0.0.0.0', port=int(node_port))    

if __name__ == '__main__':
    main()
    
=======
    app.run(host='0.0.0.0', port=int(node_port))
>>>>>>> 2421ba79d8b7968b8be5a8f9d9c3c9e970da8498

