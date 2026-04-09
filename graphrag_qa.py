from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from neo4j import GraphDatabase

load_dotenv()

# OpenAI
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

# Neo4j
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "ksh12345")

driver = GraphDatabase.driver(URI, auth=AUTH)


def retrieve_graph(query):
    with driver.session() as session:
        result = session.run("""
            MATCH (a)-[r]->(b)
            RETURN a.name AS source, type(r) AS relation, b.name AS target
        """)
        return [f"{r['source']} {r['relation']} {r['target']}" for r in result]


def graphrag_qa(question):
    graph_data = retrieve_graph(question)
    context = "\n".join(graph_data)

    prompt = f"""
    다음은 그래프 데이터입니다:
    {context}

    질문: {question}
    """

    response = llm.invoke(prompt)
    return response.content


# 테스트 질문
questions = [
    "김세희는 어디서 활동해?",
    "김세희랑 김재은 관계는 뭐야?",
    "김채윤은 어떤 분야에 관심 있어?"
]

for q in questions:
    print("질문:", q)
    print("답변:", graphrag_qa(q))
    print()
    
driver.close()