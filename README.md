# Email service extractor for account discovery
Python script to extract all unique domains form incoming email addresses from a `.mbox` file (gmail export format) to find your accounts, outputs to `.csv`

# Install
To use this you are going to need `python` and some libraries (thay all shoud come instaled wit python)

* mailbox
* pandas
* os
* threading
* time
* random

Get python [here](https://www.python.org/downloads/).

# How to get .mbox
[Youtube tutorial](https://youtu.be/x26B1_eHP3o)

* Go to [Google Take Out](http://example.com) and log in (if not logged in)
* Locate and select only Gmail
* Press on `All mail data included` and from what folders in your email you want to extract
* Scroll to bottom press `Next step`
* Select to what file sizes export should be spit (dont recommend more then 2GB)
* Press `Create export`
* Wait for email that your export is ready (possibly hours or days)
* Download to computer
# Usage
1. Put downloaded `.mbox` files in the `input` folder
2. Additionally adjust settings
3. Run program
4. Wait for program to finish
6. Results are in file named `output.csv`
5. Profit
# Features
* Works on multiple files
* Visual representation of file processing
    * Spends a lot of time to load 1GB size filed to memory, represented by `Loading file`
    * Shows live how many messages where processed and fow many are left
    * Shows live how many domains where found
    * Sows time elapsed
* Otput format is `.csv`, columns represent as follows:
    1. no.
    2. Sender's email 
    3. Domain
    4. First found message
* Additional result to be enabled: occurrence. Splits domains by `.`, saves how often all parts aper to allow you to better find your selves in the data. Results will be in `occurrence.csv`
    * Configure in code, section noted with `#occurrence CONFIG`, Config options:
        1. `occurrence`
            * enable/disable this extra output
        2. `com`
            * enable/disable exclude all `.com` parts
        3. `sing`
            * enable/disable remove all parts that appear once
    * For this output is also `.csv`, columns represent as follows:
        1. no.
        2. part string
        3. instance count

    

# Contributions
All contributions, issues, and messages are welcome! If you aren't sure about something or have any questions please reach out to me.