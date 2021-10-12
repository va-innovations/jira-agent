from flask import Flask, request, make_response, jsonify
from requests.auth import HTTPBasicAuth
import json
import requests
from jira_authentication import JiraContext


app = Flask(__name__)

@app.route("/")
def home_view():
    return "<h1>Jira Agent Api</h1>"

@app.route("/dialog", methods = ['POST'])
def dialog_controller():
    data = request.get_json(force=True)
    intent = data['queryResult']['action']
    if intent == "addIssueComment":
        comment = data['queryResult']['parameters']['comment'].strip('"')
        issue_id = data['queryResult']['parameters']['issue-id'].upper()
        print(JiraContext.add_comment(issue_id, comment))
        response = {'fulfillmentText':f'Your comment on {issue_id} has been successfully added.'}
        response_json = jsonify(response)
        return make_response(response_json) 
    if intent == "changeIssueStatus":
        issue_id = data['queryResult']['parameters']['issue-id'].upper()
        status = data['queryResult']['parameters']['status']
        response_text = JiraContext.change_status(issue_id, int(status))
        response = {'fulfillmentText':f'{response_text}'}
        response_json = jsonify(response)
        return make_response(response_json) 
    if intent == "getIssueDetails":
        issue_id = data['queryResult']['parameters']['issue-id']
        response_text = JiraContext.get_issue_by_id(issue_id)
        response = {'fulfillmentText':f'{response_text}'}
        response_json = jsonify(response)
        return make_response(response_json) 
    if intent == "getAllAssignedIssues":
        response_text = JiraContext.get_all_issues_user()
        response = {"fulfillmentText": f"{response_text}"}
        response_json = jsonify(response)
        return make_response(response_json)
    if intent == "deleteIssue":
        issue_id = data['queryResult']['parameters']['issue-id'].upper()
        response_text = JiraContext.delete_issue(issue_id)
        response = {"fulfillmentText": f"{issue_id} has been deleted."}
        response_json = jsonify(response)
        return make_response(response_json)   

    

if __name__ == '__main__':
    app.run(debug=True)