# CSC 322 Project

# Set Up
## Any pip or python command might be python3 and pip3 depending on what your default version of python is
### This project was developed using Django, Python3 and SQlite
1.  Install pip if not installed already **(package manager) pip commands are executed from the terminal**
2.  Clone project to a directory of your choice

**This instructions are to be executed in the directory just outside of the project folder (the directory into which you cloned the repo).**

[3]  pip install virtualenv
4.  SetUp virtual env as follow
5.  python -m venv env_name
6.  source env_name/bin/activate
7.  pip install --upgrade pip
8.  pip install django
9.  pip install django-widget-tweaks
10. pip install django-crispy-forms
11. cd project_name
12.  python manage.py makemigrations
13. python manage.py migrate
14. python manage.py createsuperuser
15. Enter user name
16. Enter email **can leave blank**
17. Enter password
18. Confirm password
19. python manage.py runserver
20. Open browser and go to localhost:8000/admin
21. login with super user account
22. go the accepted users tables and click on the add button on the top right
    add your user as an accepted user and check the SU checkbox and type anything
    as a reference then click save. **Super user can login in the site with the credentials previously created on the terminal**
13. proceed to localhost:8000
124. **Test!!!!!!**

This is a Web-Based Application that allows users to create teams with a certain purpose
so that other users can join them either by themselves or invite.

Time spent: Over **60** hours spent in total

## User Stories

The following **required** functionality is completed:

- [x] User can apply for an account
- [x] Visitor gets a GUI showcasing the top 3 rated projects and top tated OU profiles
- [x] Super user can review application and accept the user
- [x] Email is sent to the user with their user name and password
- [x] OUs can form groups by inviting other OU(s) for a certain purpose
- [x] OUs can accept or reject the invite
- [x] User can sign in
- [x] User can log out
- [x] An OU can put some OU's on his/her whitebox to accept invites automatically
- [x] An OU can put some OU's on his/her blackbox to reject invites automatically
- [x] Once a group is form a web-page is made available that is accessible to all group members
- [x] All group members can moderate or post to the group page
- [x] All group members can create polls to set up a meeting time or vote on other things
- [x] Display winning poll/destroy after date
- [x] Group members can vote to praise or warn the user
- [x] After 3 Warnings the user wil be automatically removed from the group(
- [x] Remove 5 rep-points from user being automatically kicked out
- [x] Vote to kick out member **Vote must be unanimous**
- [x] OUs can complain or praise other OUs
- [x] Group members can close the group and conduct an exit evaluation to other members
- [x] System keeps a list of taboo words that the system converts into
- [x] VIP's can vote other vip as a democratic superuser
