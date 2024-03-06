from neo4j import GraphDatabase
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()


#google gen ai
genai.configure(api_key=os.getenv('api_key'))

def fetch_schema():
    uri = os.getenv('uri')
    username = os.getenv('neo4j_username')
    password = os.getenv('password') 
    
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        session = driver.session()
        nodes = {}
        relationships=[]
        result = session.run("MATCH (n) RETURN labels(n), keys(n)")
        
        for item in result:
            labels = item['labels(n)']
            keys = item['keys(n)']
            
            for label in labels:
                if label not in nodes:
                    nodes[label] = keys
        relation=session.run("match (n1)-[r]->(n2) return distinct type(r),labels(n1),labels(n2)")
        for item in relation:
            relationship_type = item['type(r)']
            node1_labels = str(item['labels(n1)'])
            node2_labels = str(item['labels(n2)'])
            relationship=f"{node1_labels} {relationship_type} {node2_labels}"
            relationships.append(relationship)
    
    return {"nodes":nodes,"relationship":relationships } 



# model
def answer(question,nodes, relationship):
    generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)
    
    prompt_parts = [
        f"As a skilled Neo4j expert, your expertise lies in generating precise Cypher queries based on user input. Here’s some essential information about the database:Nodes and their keys: {nodes}"
        f"Relationships and their keys: {relationship}.donnot haullicinate.use only the information that i gave"
        "It’s crucial to note that relationships in this database are strictly one-way. This means that the direction of the relationship holds utmost importance. For instance, cell values is from sheets, but sheets are not from cell values. Therefore, when constructing your Cypher query, ensure that you consider the correct direction of the relationship."
        "Your task is to generate a high-quality Cypher query based on the provided user input, taking into account the significance of the relationship direction. Remember to exclude any quotes from the response and provide only the code, without any special characters ",question
        ]
    
      
    #neo4j connection
    uri = os.getenv('uri')
    username = os.getenv('neo4j_username')
    password = os.getenv('password')
        
    response = model.generate_content(prompt_parts)
    query=response.text.strip()
    print(query)
    with GraphDatabase.driver(uri,auth=(username,password)) as driver:
        with driver.session() as session:
            result = session.run(query)
            for record in result:
                print(record)

schema = fetch_schema()
answer("which sheet has the most connected cellvalue.also get the count", schema['nodes'],schema['relationship'])
