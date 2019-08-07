codeMAFIA
--------------------------------------------------------------------------------------------------------------------------------------------------------
General Allocation Portal
--------------------------------------------------------------------------------------------------------------------------------------------------------

	Members				|	Roll Number	|	Contribution  	|
	------------------------------  |  -------------------  |  --------------------	|
	Kunal Goyal			|	160050026	|	100%		|
	Aman Jain			|	160050034	|	100%		|
	Eashan Gupta			|	160050045	|	100%		|

#### System Requirements:
--------------------------------------------------------------------------------------------------------------------------------------------------------

* Python 3.5
* Django 1.11.5 installed on python 3.5
* A web browser to run the web application

#### How to execute:
--------------------------------------------------------------------------------------------------------------------------------------------------------

1. In terminal, cd to the project directory `cd project`
2. Then run the command `python3 manage.py makemigrations` and then `python3 manage.py migrate`. These commands start a new database or modify the existing database.
3. To start the local host and run the portal, run the command `python3 manage.py runserver`. You should get an output as:
	
    >Performing system checks...  
	>System check identified no issues (0 silenced).  
	>October 31, 2014 - 16:23:39  
	>Django version 1.7.1, using settings 'mysite.settings'  
	>Starting development server at http://127.0.0.1:8000/  
	>Quit the server with CONTROL-C. 

4. Now open the GAP website in your web browser by going to the link http://127.0.0.1:8000/
5. To create an admin use the command `python3 manage.py createsuperuser` in the terminal.
6. Click on the 'Register with us' link on the homepage to register an institute and create its portal.
7. Once your institute has registered click on the link 'Institute login' to login to your dashboard.
8. You will find links for applicants and choices and on clicking them, all the corresponding existing database will be displayed.
9. Initially there will be no choices available. To add applicants and choices, click on the upload file button to and select a csv file with the appropriate format.
10. The csv file format of the choices is: choice name, choice capacity
11. The csv file format of the applicants is: name, rank, email-id, account-password
12. After uploading the file for applicants, corresponding users with the username as 'name' and password as 'user_password' will be created.
13. The applicants can login by clicking the link 'Applicant login'. After login students can fill their rspective choices and priorities and submit.
14. The institute can then allocate the applicants by clicking 'Allocate' button on teir dashboard.
15. The applicants will now be have the options to freeze, float or drop their choices.

Task-wise details:
--------------------------------------------------------------------------------------------------------------------------------------------------------

1. **Institute registration**
	* New Institutes can register using a form.
	* The portal, once active, allows various institutes to use the matchmaking problem solver and so it can cater a wide variety of matchmaking problems.

2. **Institute Login:**
	* The various institutes using the portal are admins with access to all the information of the applicants and the choices made available.
	* The institute can create a large number of applicant users, through csv file input, to give their preferences and allocate them choices.

3. **Applicant Login:**
	* The various applicant users of the portal are also provided with a username and a password as given by their institute. 
	* They can use this to login and fill in their preferences.

4. **Allocation:**
	* Sort the students in order of their rank and allocated as per the rank list.
	* Checking it's correctness is tough. One needs to solve the test cases manually and then check with the program output.

5. **Freeze, Float, Drop:**
	*  After allocating once, all the applicants can choose to either freeze, float or drop their current branch.
		1. **Freeze**: Accept the current allocated choice and be removed from further rounds of allocation.
		2. **Float**: Be included in further rounds of allocation thus risking the current allocated seat in hope for a better allocation.
		3. **Drop**: To drop the current seat and not be included in further rounds of allocation.


