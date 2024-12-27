from flask import Flask, request, jsonify
import mysql.connector
import json

app = Flask(__name__)

# MySQL database configuration (Fill these in later)
MYSQL_HOST = ""  # Replace with your MySQL host
MYSQL_USER = ""  # Replace with your MySQL username
MYSQL_PASSWORD = ""  # Replace with your MySQL password
MYSQL_DATABASE = ""  # Replace with your MySQL database name

def update_issue_in_db(issue_data):
    """
    Updates or inserts an issue in the MySQL database.

    Args:
        issue_data: A dictionary containing the Jira issue data.
    """
    try:
        mydb = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        mycursor = mydb.cursor()

        # Check if the issue already exists
        sql = "SELECT id FROM jira_issues WHERE issue_key = %s"
        mycursor.execute(sql, (issue_data["issue_key"],))
        result = mycursor.fetchone()

        if result:
            # Update existing issue
            sql = """
                UPDATE jira_issues
                SET summary = %s,
                    status = %s,
                    assignee = %s,
                    updated = %s,
                    issue_type = %s,
                    priority = %s,
                    labels = %s,
                    components = %s,
                    project_key = %s,
                    project_name = %s,
                    resolution_date = %s,
                    description = %s,
                    environment = %s,
                    due_date = %s,
                    reporter = %s,
                    status_category = %s,
                    raw_data = %s
                WHERE issue_key = %s
            """
            values = (
                issue_data["summary"],
                issue_data["status"],
                issue_data["assignee"],
                issue_data["updated"],
                issue_data["issue_type"],
                issue_data["priority"],
                issue_data["labels"],
                issue_data["components"],
                issue_data["project_key"],
                issue_data["project_name"],
                issue_data["resolution_date"],
                issue_data["description"],
                issue_data["environment"],
                issue_data["due_date"],
                issue_data["reporter"],
                issue_data["status_category"],
                issue_data["raw_data"],
                issue_data["issue_key"]
            )
        else:
            # Insert new issue
            sql = """
                INSERT INTO jira_issues (issue_key, summary, status, assignee, created, updated, issue_type, priority, labels, components, project_key, project_name, resolution_date, description, environment, due_date, reporter, status_category, raw_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                issue_data["issue_key"],
                issue_data["summary"],
                issue_data["status"],
                issue_data["assignee"],
                issue_data["created"],
                issue_data["updated"],
                issue_data["issue_type"],
                issue_data["priority"],
                issue_data["labels"],
                issue_data["components"],
                issue_data["project_key"],
                issue_data["project_name"],
                issue_data["resolution_date"],
                issue_data["description"],
                issue_data["environment"],
                issue_data["due_date"],
                issue_data["reporter"],
                issue_data["status_category"],
                issue_data["raw_data"]
            )

        mycursor.execute(sql, values)
        mydb.commit()
        print(f"Issue {issue_data['issue_key']} updated in database.")

    except mysql.connector.Error as err:
        print(f"Error updating issue in MySQL: {err}")
    finally:
        if 'mydb' in locals() and mydb.is_connected():
            mycursor.close()
            mydb.close()

@app.route('/')
def home():
    """
    Simple route for the root URL.
    """
    return jsonify({"message": "Welcome to the Flask app!"})

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Handles incoming webhook requests from Jira.
    """
    try:
        data = request.get_json()

        # Check if the webhook event is for issue creation or update
        if data.get("webhookEvent") in ["jira:issue_created", "jira:issue_updated"]:
            issue = data.get("issue")
            if issue:
                # Extract relevant data from the issue (customize as needed)
                issue_data = {
                    "issue_key": issue["key"],
                    "summary": issue["fields"]["summary"],
                    "status": issue["fields"]["status"]["name"],
                    "assignee": issue["fields"]["assignee"]["displayName"] if issue["fields"]["assignee"] else None,
                    "created": issue["fields"]["created"],
                    "updated": issue["fields"]["updated"],
                    "issue_type": issue["fields"]["issuetype"]["name"],
                    "priority": issue["fields"]["priority"]["name"] if issue["fields"]["priority"] else None,
                    "labels": json.dumps(issue["fields"]["labels"]),
                    "components": json.dumps([c["name"] for c in issue["fields"]["components"]]),
                    "project_key": issue["fields"]["project"]["key"],
                    "project_name": issue["fields"]["project"]["name"],
                    "resolution_date": issue["fields"]["resolutiondate"],
                    "description": issue["fields"]["description"],
                    "environment": issue["fields"]["environment"],
                    "due_date": issue["fields"]["duedate"],
                    "reporter": issue["fields"]["reporter"]["displayName"] if issue["fields"]["reporter"] else None,
                    "status_category": issue["fields"]["status"]["statusCategory"]["name"],
                    "raw_data": json.dumps(issue)
                }

                update_issue_in_db(issue_data)

        return jsonify({"message": "Webhook received successfully."}), 200
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"message": "Error processing webhook."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Run on port 5000
