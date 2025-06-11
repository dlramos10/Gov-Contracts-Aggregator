import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)

SAM_API_KEY = os.getenv("SAM_API_KEY")
STATE_API_URL = os.getenv("STATE_API_URL")
STATE_API_KEY = os.getenv("STATE_API_KEY")


@app.route("/")
def index():
    return "🚀 Titan Government Services API is Live!"


@app.route("/api/hello")
def hello():
    return {"message": "Hello from the server!"}


def fetch_federal_contracts(keyword=None, naics=None, start_date=None, end_date=None):
    """Fetch contracts from SAM.gov"""
    if not SAM_API_KEY:
        return []

    url = "https://api.sam.gov/prod/opportunities/v2/search"
    params = {"api_key": SAM_API_KEY, "limit": 20}

    if keyword:
        params["q"] = keyword
    if naics:
        params["naics"] = naics
    if start_date:
        params["posted_from"] = start_date
    if end_date:
        params["posted_to"] = end_date

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("opportunitiesData", [])
    except Exception as exc:  # pragma: no cover - best effort network call
        print(f"Federal fetch error: {exc}")
        return []


def fetch_state_contracts(keyword=None, naics=None, start_date=None, end_date=None):
    """Fetch contracts from a state API if configured"""
    if not STATE_API_URL or not STATE_API_KEY:
        return []

    params = {"api_key": STATE_API_KEY}
    if keyword:
        params["keyword"] = keyword
    if naics:
        params["naics"] = naics
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date

    try:
        resp = requests.get(STATE_API_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict):
            return data.get("results", [])
        return data
    except Exception as exc:  # pragma: no cover - best effort network call
        print(f"State fetch error: {exc}")
        return []


@app.route("/api/contracts")
def contracts():
    """Aggregate federal and state contracts"""
    keyword = request.args.get("keyword")
    naics = request.args.get("naics")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    federal = fetch_federal_contracts(keyword, naics, start_date, end_date)
    state = fetch_state_contracts(keyword, naics, start_date, end_date)

    return jsonify({"federal": federal, "state": state})


if __name__ == "__main__":
    app.run(debug=True)
