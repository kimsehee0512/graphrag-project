from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from neo4j import GraphDatabase

load_dotenv()

# OpenAI
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

# Neo4j
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "ksh12345")

driver = GraphDatabase.driver(URI, auth=AUTH)

# 그래프에서 정보 가져오기
def get_graph_data():
    with driver.session() as session:
        result = session.run("""
            MATCH (p:Person)-[:WORKS_AT]->(c:Company)
            RETURN p.name AS person, c.name AS company
        """)
        return [f"{r['person']} works at {r['company']}" for r in result]

# GraphRAG 실행
def graphrag_query(question):
    graph_data = get_graph_data()
    context = "\n".join(graph_data)

    prompt = f"""
    다음은 그래프 데이터입니다:
    {context}

    질문: {question}
    """

    response = llm.invoke(prompt)
    return response.content

# 테스트
answer = graphrag_query("김철수는 어디에서 일해?")
print("답변:", answer)

driver.close()