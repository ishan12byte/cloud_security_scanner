from flask import Flask, render_template, redirect, request, send_file, flash
import boto3
from botocore.exceptions import ClientError

from scanner.main_scanner import run_scan
from services.summary import generate_summary
from services.scoring import calculate_security_score
from services.storage import load_scan, save_scan
from services.exporter import export_json, export_csv

app = Flask(__name__)

app.secret_key = "sdfha;wah38723872rfhhjjklfs"

@app.route("/") 
def dashboard():

    data = load_scan()
    
    findings = data["findings"]

    summary = generate_summary(findings)

    score = calculate_security_score(findings)

    return render_template(
        "dashboard.html",
        findings=findings,
        summary=summary,
        score=score,
        scan_time=data["scan_time"],
        account=data.get("account")
    )
    
@app.route("/scan")
def scan():

    findings = run_scan()

    save_scan(findings)

    return redirect("/")

@app.route("/findings")
def findings():

    data = load_scan()

    findings = data["findings"]

    severity = request.args.get("severity")
    service = request.args.get("service")

    if severity:
        findings = [
            f for f in findings
            if f["severity"] == severity
        ]

    if service:
        findings = [
            f for f in findings
            if f["service"] == service
        ]

    return render_template(
        "findings.html",
        findings=findings,
        selected_severity=severity,
        selected_service=service
    )
    
@app.route("/download/json")
def download_json():

    export_json(load_scan()["findings"])

    return send_file(
        "reports/findings.json",
        as_attachment=True
    )
    
@app.route("/download/csv")
def download_csv():

    export_csv(load_scan()["findings"])

    return send_file(
        "reports/findings.csv",
        as_attachment=True
    )

@app.route("/connect", methods=["GET", "POST"])
def connect():

    if request.method == "POST":

        access_key = request.form["access_key"]
        secret_key = request.form["secret_key"]
        region = request.form["region"]

        try:

            session = boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )
            
            # Verify credentials
            sts = session.client("sts")

            identity = sts.get_caller_identity()

            account_info = {
                "account_id": identity["Account"],
                "arn": identity["Arn"],
                "region": region
            }

            findings = run_scan(session)

            save_scan(findings, account_info)

            return redirect("/")

        except ClientError:

            flash("Unable to connect to AWS. Check your credentials.")

    return render_template("connect.html")

if __name__ == "__main__":
    app.run(debug=True)