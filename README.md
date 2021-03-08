## Assignment #2
Course: COMP445 <br />
By: <br />
- Muhammad Saad Mujtaba (40043156)
- Mohammad Naimur Rashid (40027867)

## Getting Started
This is a repo for running your Simplified Python IRC implemented using 
Client and Server based on RFC 1459. 

### Prerequisites

For this module, you need to have Python3 downloaded and the windows curses 
module installed
* Installation
  ```sh
  git clone https://github.com/RumianR/SocketProgramming.git
  ``` 
* windows-curses 2.2.0
  ```sh
  pip install windows-curses
  ```
  
### Usage

To run this solution, run the following commands in your local terminal. 
You will need one terminal to run the server and multiple other ones 
depending on how many clients you decide to run.

* First, to start the server
  ```sh
  python server.py --port <PORT-OF-YOUR-CHOICE>
  ```
* Secondly, to run a client (do this for each client you want to run)
  ```sh
  python client.py --server <SERVER> --port <PORT> --name <NAME> --nickname <NICKNAME>
  ```
  
 ## CLI Example
* Client Usage <br />
 ![alt text](https://drive.google.com/file/d/1Zef_JvHryUx5BPaHNtx_2JiFEZLA-dWu/view?usp=sharing)

* Server Usage <br />
 ![alt text](https://drive.google.com/file/d/1JxSrlvVCVuAkAuUs-R0MM_pfBnexw7B8/view?usp=sharing)
