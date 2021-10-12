from flask import Flask, request, make_response, jsonify
from flask.wrappers import Response
from requests.auth import HTTPBasicAuth
import json
import requests

class JiraContext():

    auth = HTTPBasicAuth("klavskruz@gmail.com", "zvBQsTHhb4tc5jy0kMvK2FDF")

    @staticmethod
    def get_all_issues():
        url = f"https://jira-agent.atlassian.net/rest/api/3/search"

        headers = {
            "Accept": "application/json"
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=JiraContext.auth
        )

        return json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))

    @staticmethod
    def get_issue_by_id(id):
        url = f"https://jira-agent.atlassian.net/rest/api/2/issue/{id}"

        headers = {
            "Accept": "application/json"
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=JiraContext.auth
        )
        
        response_json =  response.json()
        response_text = f"Issue Id: {response_json['id']} \n Issue Key: {response_json['key']} \n Summary: {response_json['fields']['summary']} \n Description: {response_json['fields']['description']}\n Asignee: {response_json['fields']['assignee']['displayName']}\n Priority: {response_json['fields']['priority']['name']} \n Status: {response_json['fields']['status']['name']}"
        return response_text
    @staticmethod
    def delete_issue(id):
        url = f"https://jira-agent.atlassian.net/rest/api/2/issue/{id}"

        response = requests.request(
            "DELETE",
            url,
            auth=JiraContext.auth
        )

        return response.text
    @staticmethod
    def get_all_issues_user():
        url = "https://jira-agent.atlassian.net/rest/api/2/search?jql=assignee=currentuser()"
        headers = {
         "Accept": "application/json",
        "Content-Type": "application/json"
        }
        response = requests.request(
           "GET",
           url,
           headers=headers,
           auth=JiraContext.auth
        )
        response_json = response.json()
        print(response_json)
        assigned_issues = []
        for i in response_json['issues']:
            issue = {'key':i['key'],'summary':i['fields']['summary']}
            assigned_issues.append(issue)
        response_text = ""
        for issue in assigned_issues:
            response_text = response_text + f"{issue['key']} | Summary: {issue['summary']} \n"
        return response_text
        
    @staticmethod
    def add_comment(id,comment_text):
        url = f"https://jira-agent.atlassian.net/rest/api/2/issue/{id}/comment"
        headers = {
         "Accept": "application/json",
        "Content-Type": "application/json"
        }
        

        payload = json.dumps( {
          "visibility": {
            "type": "role",
            "value": "Administrators"
          },
          "body": f"{comment_text}"
        } )

        response = requests.request(
           "POST",
           url,
           data=payload,
           headers=headers,
           auth=JiraContext.auth
        )
        
        return "Comment added"
    @staticmethod
    def get_all_comments(id):
        url = f"https://jira-agent.atlassian.net/rest/api/2/issue/{id}/comment"

        headers = {
            "Accept": "application/json"
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=JiraContext.auth
        )

        return json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))

    @staticmethod
    def change_status(id, new_status):
        url = f"https://jira-agent.atlassian.net/rest/api/3/issue/{id}/transitions"
        payload = json.dumps({
          "transition": {"id": f"{new_status}"}
        })
        headers = {
         "Accept": "application/json",
        "Content-Type": "application/json"
        }
        response = requests.request(
           "POST",
           url,
           data=payload,
           headers=headers,
           auth=JiraContext.auth
        )
        status_codes = {11:'backlog',21:'selected for development',31:'in progress', 41:'done'}
        return f"The status of {id} has been successfully changed to {status_codes[new_status]}"
        