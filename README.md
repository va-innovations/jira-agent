# Jira Virtual Agent

This is an API which is built with Flask, to respond to webhooks calls performed by JiraBot2021 Agent. 
It is meant to be connected with Jira Cloud project and manipulate the tickets on the Kanban board.

## Current functionality

get_issue_by_id - returns issue details with ID provided

delete_issue - deletes issues with ID provided

get_all_issues_user - returns all issues assigned to user

add_comment - adds a comment to issue with ID provided

 get_all_comments - returns all comments of an issue with ID provided
 
 change_status - changes issues status with ID and new status ID provided. 
 
 All of the methods are defined in jira_authentication.py file.
 
 ## Auth
 
 To link the API to a Jira Cloud project replace email and api key values with actual values in jira_authentication.py file
 
 ## Deployment
 
 To deploy the project on Heroku:
 1. Initialize a new git repository
 2. Add Heroku as remote repositoty to the project
 3. Push the project to remote.

