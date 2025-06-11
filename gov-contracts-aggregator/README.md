# Gov Contracts Aggregator

This project provides a simple Flask API and React client for aggregating federal and state government contract data.

## Configuration

Copy `.env.example` inside `gov-contracts-aggregator/server` to `.env` and fill in your API credentials:

```
SAM_API_KEY=your-sam-gov-api-key
# Optional state API configuration
STATE_API_URL=https://example.state.api/contracts
STATE_API_KEY=your-state-api-key
```

Only `SAM_API_KEY` is required for basic federal searches. State parameters are optional and depend on the state data source you want to use.

## Running the server

```
cd gov-contracts-aggregator/server
pip install -r requirements.txt
python app.py
```

The server exposes `/api/contracts` which accepts `keyword`, `naics`, `start_date`, and `end_date` query parameters.

## Running the client

```
cd gov-contracts-aggregator/client
npm install
npm start
```

The React application lets you submit searches and view aggregated results from the server.

## Updating API keys

You can change the SAM.gov or state API keys at any time. Edit the values in your `.env` file or send a `POST` request to `/api/update_key`:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"sam_api_key": "NEW_KEY"}' http://localhost:5000/api/update_key
```

The server reads keys from environment variables on each request, so updates take effect immediately.
