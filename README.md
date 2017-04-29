# Contents
1. [What is JFlapToCode?](../../#what-is-jflaptocode)
    * [Why HLSM and MDPs?](../../#why-hlsms-and-mdps)
2. [Getting Started](../../#getting-started)
3. [Languages/Platforms Supported](../../#languagesplatforms-supported)
4. [Special Commands](../../#special-commands)
    * [States](../../#special-commands-for-states)
    * [Transitions](../../#special-commands-for-transitions)
5. [Associate *.jff files with JFlapToCode](../../#associate-jff-files-with-jflaptocode)


# What is JFlapToCode?

JFlapToCode is a Python application that translates **High Level State Machines (HLSM)** and **Markov Decision Processes (MDP)** to real code. It translates diagrams designed by JFlap, a Java application for experimenting with formal languages. The application itself is built ontop of Jinja2.

![State Diagram](http://acsweb.ucsd.edu/~mmg005/img/SimpleRPiHLSM_2.png)

### Why HLSMs and MDPs?
High level diagrams provide a useful abstraction when describing complex behavior found in domains such as robotics and video game AI. However, the process of writing code that implement HLSM and MDP structure can be tedious and error prone. Fortunately, the process is easily automatable.  

# Getting Started
Coming soon...

# Languages/Platforms Supported
| Name   | HLSM | MDP
| ---    | ---  | ---
| Unity  | Implemented | Implemented
| Python | Implemented | Planned
| Arduino | Implemented | Planned
| C       | Implemented | Planned
| C++     | Implemented | Planned
| C# | Should extract common interface from Unity | Planned
| Java | Should extract common interface from Unity | Deprecated
| JavaScript | Planned | Not Planned
| Android | Should extract common interface from Java | Deprecated

# Special Commands

Special Commands are 3 character strings attached to the end of state/transition names that affects how JFlapToCode creates code. In general, they make the generated code more succient at the expense of state machine readability. All Special Commands begin with the **hash (#)** and are followed by two other characters. A Special Command may end with the **colon (:)** to accept additional parameters. For example, naming a state **Idle#NF** will tell JFlapToCode to not generate a function to execute within the **Idle** state. The state transitions are not affected by Special Commands. 
### Special Commands for States

| Name | Command | Description 
| ---  | ---    | ---
| No Function  | **#NF** | JFlapToCode will not generate a function for the preceding state
| Specify Function | **#F:FUNC_NAME** | JFlapToCode will generate and use **FUNC_NAME** for the preceding state rather than the default state generated. This is useful when multiple states execute the same logic
| Create Delay Variable| **#D:DELAY_TIME** | JFlapToCode will generate create a variable with a name similar with the state containing the value **DELAY_TIME**. 

### Special Commands for Transition
| Name | Command | Description
| ---  | ---     | ---
| Negation | ! | The function associated with this transition will be negated. **Note: This command does not follow the #(hash) structure of the other commands. Furthermore, the ! is added to the front of the transition. ** 
| Literal Expression | **#LE** | The transition will be treated as a literal expression. JFlap will not generate a function for the transition and will place the literal string within the generated conditional statement
More coming soon...

# Associate *.jff files with JFlapToCode

## Windows:

Run the following commands on the windows command line as an administrator:

assoc .jff=JFlapFile

ftype JFlapFile="**PYTHON_EXE_PATH**\python.exe" "**JFlapToCode_Dir**\src\JFlapToCode.py" "%1" %*

**PYTHON_EXE_PATH** is the directory on your machine where python is installed

**JFlapToCode_Dir** is the directory on your machine where this repo has been cloned
