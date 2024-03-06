# NeoGen: A RAG-based Neo4j Query Generator

This script is designed to fetch the schema from a Neo4j database and generate a Cypher query based on user input using Google's Generative AI.

## Dependencies

- `neo4j`
- `google.generativeai`
- `dotenv`
- `os`

## Environment Variables

The script uses the following environment variables:

- `api_key`: Your Google Generative AI API key.
- `uri`: The URI of your Neo4j database.
- `neo4j_username`: Your Neo4j username.
- `password`: Your Neo4j password.

## Functions

- `fetch_schema()`: Fetches the schema from the Neo4j database. It returns a dictionary containing nodes and their keys, and relationships.

- `answer(question, nodes, relationship)`: Generates a Cypher query based on the user input (`question`), nodes, and relationships. It uses Google's Generative AI to generate the query. The function then runs the query on the Neo4j database and prints the result.

## Usage

1. Set your environment variables in a `.env` file.
2. Call `fetch_schema()` to fetch the schema from your Neo4j database.
3. Call `answer(question, nodes, relationship)` with your question and the schema to generate and run a Cypher query.

```python
schema = fetch_schema()
answer("your question", schema['nodes'], schema['relationship'])
```

This will print the Cypher query and the result of running the query on your Neo4j database. The generated Cypher query will be based on this question. 

Please note that the relationships in the database are strictly one-way, so the direction of the relationship is important when constructing the Cypher query. The script ensures that it considers the correct direction of the relationship. 

## Safety Settings

The script uses safety settings to block content that falls under the categories of harassment, hate speech, sexually explicit content, and dangerous content. These settings are used when generating the Cypher query with Google's Generative AI. 

## Note

The script does not hallucinate and uses only the information provided. It generates high-quality Cypher queries based on the provided user input, taking into account the significance of the relationship direction. It excludes any quotes from the response and provides only the code, without any special characters.