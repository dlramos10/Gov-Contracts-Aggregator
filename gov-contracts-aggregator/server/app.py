import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    return "🚀 Titan Government Services API is Live!"


@app.route("/api/hello")
def hello():
    return {"message": "Hello from the server!"}


def fetch_federal_contracts(keyword=None, naics=None, start_date=None, end_date=None):
    """Fetch contracts from SAM.gov"""
    sam_api_key = os.getenv("SAM_API_KEY")
    if not sam_api_key:
        return []

    url = "https://api.sam.gov/prod/opportunities/v2/search"
    params = {"api_key": sam_api_key, "limit": 20}

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
    state_api_url = os.getenv("STATE_API_URL")
    state_api_key = os.getenv("STATE_API_KEY")
    if not state_api_url or not state_api_key:
        return []

    params = {"api_key": state_api_key}
    if keyword:
        params["keyword"] = keyword
    if naics:
        params["naics"] = naics
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date

    try:
        resp = requests.get(state_api_url, params=params, timeout=10)
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


@app.route("/api/update_key", methods=["POST"])
def update_key():
    """Update API keys without restarting the server."""
    data = request.get_json(force=True)
    sam_key = data.get("sam_api_key")
    state_key = data.get("state_api_key")
    if sam_key:
        os.environ["SAM_API_KEY"] = sam_key
    if state_key:
        os.environ["STATE_API_KEY"] = state_key
    return jsonify({"message": "API keys updated"})


if __name__ == "__main__":
    app.run(debug=True)
