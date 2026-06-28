# 🔒 Cloud Security Scanner

A Flask-based web application that performs **read-only AWS cloud security assessments** by auditing common security misconfigurations across IAM, Amazon S3, Amazon EC2, and Security Groups.

The application connects to an AWS account using temporary IAM credentials, scans the configured resources, generates security findings, calculates an overall security score, and presents the results through an interactive web dashboard.

---

# 📖 Table of Contents

* Overview
* Features
* Architecture
* Security Checks
* Technology Stack
* Project Structure
* Installation
* AWS Setup
* Running the Application
* Dashboard Overview
* Security Score
* Exporting Reports
* Screenshots
* Future Improvements
* License

---

# 🚀 Overview

Cloud Security Scanner is designed to help identify common AWS security misconfigurations without making any changes to cloud resources.

Unlike administrative automation tools, this application performs **read-only security auditing** using AWS APIs and presents the results through an intuitive Flask dashboard.

The project demonstrates practical cloud security concepts including:

* AWS Identity and Access Management (IAM)
* Infrastructure auditing
* Secure AWS authentication
* Cloud resource inspection
* Security reporting
* Flask web development
* Python modular application design

---

# ✨ Features

## Dashboard

* Security Score (0–100)
* Total findings
* Severity breakdown
* Findings by AWS service
* Connected AWS account information
* Last scan timestamp

---

## AWS Security Scanners

### IAM Scanner

* Detect users without MFA
* Detect AdministratorAccess policy
* Detect PowerUserAccess policy
* Detect inherited privileged permissions
* Detect multiple access keys
* Detect access keys older than 90 days

---

### Amazon S3 Scanner

* Bucket versioning status
* Default encryption configuration
* Public Access Block configuration

---

### Amazon EC2 Scanner

* Public IP detection
* Stopped instances
* Termination protection status
* EBS volume encryption

---

### Security Group Scanner

* SSH (Port 22) exposed to the internet
* RDP (Port 3389) exposed to the internet
* Database ports exposed publicly
* Unrestricted inbound rules
* HTTP/HTTPS exposure

---

## Findings Processing

* Severity classification
* Security score calculation
* Findings summary
* JSON export
* CSV export

---

# 🏗 Architecture

```text
                     User
                       │
                       ▼
              Flask Web Dashboard
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
   AWS Connection             Findings Viewer
         │                           │
         └─────────────┬─────────────┘
                       ▼
               Scanner Engine
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
       IAM            EC2             S3
                       │
                Security Groups
                       │
                       ▼
              Findings Processing
                       │
             JSON / CSV / Dashboard
```

---

# 🔍 Security Checks

| AWS Service     | Checks Performed                                                               |
| --------------- | ------------------------------------------------------------------------------ |
| IAM             | MFA, privileged policies, inherited permissions, multiple access keys, key age |
| Amazon S3       | Versioning, bucket encryption, public access block                             |
| Amazon EC2      | Public IPs, stopped instances, termination protection, EBS encryption          |
| Security Groups | SSH, RDP, HTTP, HTTPS, database exposure, unrestricted rules                   |

---

# 🛠 Technology Stack

## Backend

* Python 3
* Flask
* boto3

## Frontend

* HTML5
* Bootstrap 5
* Jinja2 Templates

## AWS Services

* IAM
* Amazon EC2
* Amazon S3
* Security Groups
* STS

---

# 📁 Project Structure

```text
cloud-security-scanner/

├── app.py
├── requirements.txt
│
├── scanner/
│   ├── iam_scanner.py
│   ├── s3_scanner.py
│   ├── ec2_scanner.py
│   ├── sg_scanner.py
│   ├── main_scanner.py
│   └── utils.py
│
├── services/
│   ├── summary.py
│   ├── scoring.py
│   ├── exporter.py
│   ├── storage.py
│   └── aws_session.py
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── findings.html
│   ├── connect.html
│   └── setup.html
│
├── static/
│
└── reports/
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/cloud-security-scanner.git
```

Move into the project directory

```bash
cd cloud-security-scanner
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start the application

```bash
python app.py
```

Open your browser

```
http://127.0.0.1:5000
```

---

# ☁ AWS Setup

The scanner requires a dedicated IAM user with read-only permissions.

## Step 1

Create a new IAM User.

Recommended name:

```
SecurityScannerUser
```

---

## Step 2

Attach the AWS managed policy

```
ReadOnlyAccess
```

---

## Step 3

Generate an Access Key

Save:

* Access Key ID
* Secret Access Key

---

## Step 4

Open the application.

Navigate to:

```
Connect AWS
```

Enter

* AWS Access Key ID
* AWS Secret Access Key
* AWS Region

Click

```
Connect & Run Scan
```

---

# 📊 Dashboard Overview

The dashboard displays

* Overall Security Score
* Total Findings
* Connected AWS Account
* Findings grouped by severity
* Findings grouped by service
* Last Scan Time

---

# 📈 Security Score

The application calculates a security score out of **100**.

Points are deducted based on finding severity.

| Severity | Penalty |
| -------- | ------- |
| Critical | 20      |
| High     | 10      |
| Medium   | 5       |
| Low      | 2       |

This provides a simple indicator of the cloud environment's security posture.

---

# 📤 Exporting Reports

The application supports exporting findings as

* JSON
* CSV

These reports can be used for documentation or further analysis.

---

# 🔐 Security

The application is designed to be non-intrusive.

It

* Performs only read-only AWS API calls
* Does not modify AWS resources
* Does not create or delete infrastructure
* Does not remediate findings automatically
* Uses supplied AWS credentials only for the scanning session

---

# 📸 Screenshots

* Dashboard
  <img width="1920" height="1873" alt="screencapture-verbose-space-spoon-x57jxqpgrrxfpvvx-5000-app-github-dev-2026-06-28-12_14_21" src="https://github.com/user-attachments/assets/a4bb8334-ac45-43c4-868b-8e8f1f753005" />

* AWS Connection Page
  <img width="1920" height="1080" alt="Screenshot 2026-06-28 121254" src="https://github.com/user-attachments/assets/28374c12-f6d6-4f3c-b3ef-41ef9f546565" />

* Setup Guide
  <img width="1920" height="1080" alt="Screenshot 2026-06-28 121530" src="https://github.com/user-attachments/assets/6468fa13-13d7-4dc5-a03a-468e2d4949e8" />

* Findings Page
  <img width="1920" height="1080" alt="Screenshot 2026-06-28 121654" src="https://github.com/user-attachments/assets/2a5f86f9-9d7a-4b5f-9ae9-346fdb762b72" />


---

# 🚀 Future Improvements

* PDF report generation
* Interactive dashboard charts
* Additional AWS service coverage (CloudTrail, RDS, VPC, IAM Password Policies)
* Docker support
* Scheduled security scans
* Email notifications
* Historical scan comparison

---

# 🎯 Learning Outcomes

This project demonstrates practical experience with

* AWS Cloud Security
* IAM
* Amazon S3
* Amazon EC2
* Security Groups
* boto3
* Flask
* Python
* REST-style application architecture
* Cloud resource auditing
* Secure credential handling
* Dashboard development

---

# 📄 License

This project is intended for educational and portfolio purposes.

Feel free to fork, improve, and extend it.
