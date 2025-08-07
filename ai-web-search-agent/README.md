# AI Web Search Agent

This project implements an AI web search agent that utilizes the SentenceTransformer model and DuckDuckGo to perform web searches based on keywords provided by the user through a FastAPI API.

## Project Structure

```
ai-web-search-agent
├── src
│   ├── main.py                # Entry point of the application
│   ├── search_service.py       # Contains the WebSearchService class for web searching
│   ├── models
│   │   ├── __init__.py        # Initializes the models package
│   │   └── schemas.py         # Defines data models for API requests and responses
│   └── utils
│       ├── __init__.py        # Initializes the utils package
│       └── logging_config.py   # Configures logging for the application
├── config
│   └── config.toml            # Configuration file for application settings
├── tests
│   ├── __init__.py            # Initializes the tests package
│   ├── test_search_service.py  # Unit tests for the search_service module
│   └── test_main.py           # Unit tests for the main module
├── requirements.txt            # Lists project dependencies
├── Dockerfile                  # Dockerfile for building the application image
├── docker-compose.yml          # Docker Compose configuration for running the application
├── .env.example                # Example environment variables
├── .gitignore                  # Specifies files to ignore in Git
└── README.md                   # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ai-web-search-agent
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the application by editing the `config/config.toml` file to set the desired AI model and port.

## Usage

To run the application, execute the following command:
```
uvicorn src.main:app --host 0.0.0.0 --port <port>
```
Replace `<port>` with the port specified in the `config.toml` file.

### API Endpoints

- **POST /search**
  - Request Body: 
    ```json
    {
      "keywords": ["keyword1", "keyword2"],
      "max_results": 10
    }
    ```
  - Response:
    ```json
    {
      "urls": [{"title": "Title", "body": "Snippet", "affinity_score": 0.95}],
      "total_results": 1
    }
    ```

- **GET /health**
  - Response:
    ```json
    {
      "status": "healthy",
      "service": "web-search"
    }
    ```

## Testing

To run the tests, use the following command:
```
pytest
```

## Docker

To build and run the application using Docker, execute:
```
docker-compose up --build
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.