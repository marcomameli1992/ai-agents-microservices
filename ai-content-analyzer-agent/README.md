# AI Content Analyzer Agent

This project implements an AI content analyzer agent that utilizes the results from a web search agent to extract and analyze content from web pages. The agent classifies entities present in the analyzed content and provides insights through a FastAPI API.

## Project Structure

```
ai-content-analyzer-agent
├── src
│   ├── main.py                # Entry point of the application
│   ├── analyzer_service.py     # Contains the ContentAnalyzerService class for analyzing web pages
│   ├── entity_classifier.py     # Contains the EntityClassifier class for classifying entities
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
│   ├── test_main.py           # Unit tests for the main module
│   ├── test_analyzer_service.py  # Unit tests for the analyzer_service module
│   └── test_entity_classifier.py  # Unit tests for the entity_classifier module
├── requirements.txt            # Lists project dependencies
├── Dockerfile                  # Dockerfile for building the application image
├── Dockerfile.test             # Dockerfile for running tests
├── docker-compose.yml          # Docker Compose configuration for running the application
├── .env.example                # Example environment variables
└── README.md                   # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ai-content-analyzer-agent
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the application by editing the `config/config.toml` file to set the desired settings.

## Usage

To run the application, execute the following command:
```
uvicorn src.main:app --host 0.0.0.0 --port <port>
```
Replace `<port>` with the port specified in the `config.toml` file.

### API Endpoints

- **POST /analyze**
  - Request Body: 
    ```json
    {
      "urls": [{"href": "http://example.com", "affinity_score": 0.95}]
    }
    ```
  - Response:
    ```json
    {
      "pages": [{"url": "http://example.com", "title": "Example", "description": "An example page", "keywords": ["example"], "headings": {"h1": ["Example"], "h2": []}, "links_count": 5, "images_count": 2, "text_content": "This is an example.", "word_count": 4, "language": "en", "original_search_score": 0.95}],
      "total_analyzed": 1
    }
    ```

- **GET /health**
  - Response:
    ```json
    {
      "status": "healthy",
      "service": "content-analyzer"
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