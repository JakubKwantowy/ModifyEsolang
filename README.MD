# The Modify Esolang Interpreter

This is the official Interpreter for the Modify Esolang

Modify is a self-modifying Esolang where code is data and data is code.  
Instead of Variables, data is stored in lines.  
(Only) Integers can be stored in one of four registers (a, b, c, d)

## Installation

Step 1: Clone this repo (example: `git clone https://github.com/JakubKwantowy/ModifyEsolang.git`)  
Step 2: Allow Execution `chmod u+x modify.py`

## Usage

Run `./modify.py`  
Help will be printed automatically

## Example Scripts

Example scripts can be found in the *examples* directory

## Documentation

Instructions are formatted like this: `<command> [arg0 [arg1 [... [argn]]]]`  

Argument Types:  
`%arg`: Evaluation (Integer, Register, # + Line Number, # + Reg. with Line Number, Label), invalid evaluations will either return 0 or ''  
`#arg`: Line Number as Evaluation (DO NOT USE # IN EVALUATION AS VALUE AT LINE WILL BE USED)  
`$arg`: Register  
`@arg`: Other Expression (Listed in Command)

TODO: Finish Readme
