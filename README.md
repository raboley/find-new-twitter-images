# Find New Twitter Images

This lambda function searches twitter for new tweets by a specified user, checks against a specified s3 bucket and calls a download lambda with the url if the image hasn't already been downloaded.

## Local setup

to setup locally run the setup.sh file in terminal from the root folder.

``` bash
bash setup.sh
```

this will create a python virtual environment and download all the required packages into that environment. To run commands you will have to put your terminal or debuger in that virtual environment. to change the terminal window use the virtual environment run:

``` bash
# Mac linux
source env/bin/activate

# Windows
. env/bin/activate
```

if you are using vscode as the debugger then you will want to make sure that is also running in the virtual environment. in the bottom left next to the git buttons should be `python 3. something or other`. click that and select the option that is a version of python 3 and ends with `('env')`. If there is no option like that ensure the env folder that got created upon setup is in the root folder of your project. If this repo isn't the root for the folder open in vscode it may not recognize the virtual env right away, so make sure it is in the root, or change in the vscode python settings where it looks for virtualenvironments.

once all the dependencies are setup you can test the whole thing by running handler.py. I like to open the file in vscode and hit F5 (fn + F5 for mac) so I can see the debugger values at my breakpoints if needed. Since this file has a block at the bottom that runs it as if it were a script if executed directly, you can do just that, but if it is imported or called by something else only the command specified will be run.

Once it runs it will check the twitter name, verify that image hasn't been downloaded yet, call a lambda function to download the image and then move onto the next tweet for n tweets.

## Deploy

The build and deploy steps use the serverless framework to create the lambda function as well as all associated items (s3 buckets, IAM permissions, etc.). First is to install serverless if you don't have it:

``` bash
npm install -g serverless
```

next is to install the python package requirements plugin for serverless

``` bash
serverless plugin install -n serverless-python-requirements
```

to deploy to aws make sure the user you are using has the proper aws credentials setup and has permission to create in cloud formation, IAM, Lambda, S3.

``` bash
serverless deploy
```

