# The Modify Esolang Interpreter

This is the official Interpreter for the Modify Esolang

Modify is a self-modifying Esolang where code is data and data is code.  
Instead of Variables, data is stored in lines.

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
`%arg`: Evaluation (Integer, Register, # + Line Number, # + Reg. containing Line Number, Label), invalid evaluations will either return 0 or an empty string  
`#arg`: Line Number as Evaluation (Note: # can be used for Pointers to Lines)  
`$arg`: Register  
`@arg`: Other Expression (Listed in Command)

### Registers

Registers are a quick way to store Integer Values and do mathematical operations on them.  
Supported Registers are: `a, b, c, d`

### Evaluation

Evaluations are used for efficient representation of data in Modify.  
There are multiple types of evaluation. All of them are Listed here:  
&emsp;Integer: Results in the Literal value of an integer being returned.  
&emsp;Regster: Results in the value of a given register being returned.  
&emsp;# + Integer: Results in the value of a given line being returned.  
&emsp;# + Register: Results in the value of a line pointed at by a given register being returned.  
&emsp;Label: Results in the Line number of a Label being returned.  
If an evaluation has to convert a string to an integer (like when setting registers or integer conditionals) it will do one of two things:
If the string is numeric (a decimal number in string form), it will be directly converted to an integer. Otherwise, it will take the string's length.

### Labels

Labels are lines that consist of a colon followed by a name.  
Labels can be Read by an Evaluation, returning with the line number of the Label.  
Labels are only parsed at the beginning of runtime, meaning that if you change the contents of a label's line, the label will not be affected.

### The Stack

The stack is used for additional storage of integer values.  
The registers can be Pushed, Popped and Peeked off and onto the Stack.  
For string storage on the stack, line numbers can be used.

### The Verbose (-v) flag

The Modify interpreter can be run with the -v flag, which turns on Verbose Mode.  
In Verbose Mode, extra debug information is printed to the Console.

Here is a list of all implemented Commands:

### print

Usage: `print %val`  
Prints the value of %val to the Console.

### println

Usage: `println %val`  
Prints the value of %val to the Console with a newline.

### exit

Usage: `exit [%code]`  
Exits Program with Exit Code %code.  
If %code is not specified Program will exit with Code 0.

### setreg

Usage: `setreg $reg %val`  
Sets value of Register $reg to the value of %val

### &lt;stackop&gt;reg

Usage: `<stackop>reg $reg`  
Performs stack operation on register $reg  
&lt;stackop&gt; can be one of following:  
&emsp;`push`: Pushes register onto stack  
&emsp;`pop`: Pops value from stack into register  
&emsp;`peek`: Peeks (Reads without removing) value from stack into register

### &lt;mathop&gt;reg

Usage: `<mathop>reg $reg %n1 %n2`  
Performs Mathematical Operation on %n1 and %n2 and stores result in $reg  
&lt;mathop&gt; can be one of following:  
&emsp;`add`: $reg = %n1 + %n2  
&emsp;`sub`: $reg = %n1 - %n2  
&emsp;`mul`: $reg = %n1 * %n2  
&emsp;`div`: $reg = %n1 / %n2

### sqrtreg

Usage: `sqrtreg $reg %n`  
Sets $reg to the square root of the value of %n

### setline

Usage: `setline #line %val`  
Sets line #line to value %val

### jumpline

Usage: `jumpline #line`  
Jumps Execution to Line #line

### inputline

Usage: `inputline #line`  
Reads input from User and stores it into #line

### conditional (string)

Usage: `conditional %v1 %v2 @cond #target %val`  
Compares %v1 and %v2 with condition @cond, and treats %v1 and %v2 as strings. If the comparison is true, line #target will be set to value %val.  
Valid string Conditions @cond are:  
&emsp;`eq`: Checks if %v1 and %v2 are equal

### conditional (int)

Usage: `conditional %v1 %v2 @cond #target %val`  
Compares %v1 and %v2 with condition @cond, and treats %v1 and %v2 as integers. If comparison is true, line #target will be set to value %val.  
Valid inetegr Conditions @cond are:  
&emsp;`numeq`: Checks if %v1 and %v2 are equal  
&emsp;`less`: Checks if %v1 is lower than %v2  
&emsp;`gtr`: Checks if %v1 is greater than %v2  
&emsp;`lesseq`: Checks if %v1 is lower than or equal %v2  
&emsp;`gtreq`: Checks if %v1 is greater than or equal %v2
