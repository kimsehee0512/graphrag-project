# GraphRAG Project

## Overview
This project implements a basic GraphRAG (Graph-based Retrieval-Augmented Generation) system using Neo4j and OpenAI.

This project was developed as a hands-on practice to understand how graph databases and LLMs can be integrated for knowledge-based question answering.

It demonstrates how to:
- Extract entities and relationships from text using LLM
- Store them in a graph database (Neo4j)
- Retrieve graph data to answer user queries

---

## Architecture

Text → LLM → Entity & Relation Extraction → Neo4j Graph → Retrieval → LLM Answer

---

## Features

-  Automatic knowledge graph generation from text
-  Neo4j-based graph storage and visualization
-  Graph-based question answering using LLM
-  End-to-end GraphRAG pipeline

---

##  Project Structure
├── data/ # Input text data
│ └── sample.txt
├── build_graph_from_text.py # Extract graph from text
├── graphrag_basic.py # Basic GraphRAG example
├── graphrag_qa.py # Graph-based QA system
├── test_openai.py # OpenAI connection test
├── test_neo4j.py # Neo4j connection test
├── test_neo4j_data.py # Neo4j data creation test
├── main.py # Entry file (optional)
├── pyproject.toml # Project dependencies
└── uv.lock # Lock file
