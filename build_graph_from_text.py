import os
import json
import re
from dotenv import load_dotenv
from neo4j import GraphDatabase
from langchain_openai import ChatOpenAI

load_dotenv()

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "ksh12345")
TEXT_FILE = "data/sample.txt"

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
driver = GraphDatabase.driver(URI, auth=AUTH)


def clean_json_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def safe_rel_type(rel: str) -> str:
    rel = rel.upper().strip()
    rel = re.sub(r"[^A-Z0-9_]", "_", rel)
    rel = re.sub(r"_+", "_", rel).strip("_")
    return rel or "RELATED_TO"


def extract_graph(text: str) -> dict:
    prompt = f"""
다음 문서에서 엔티티와 관계를 추출해라.

반드시 아래 JSON 형식만 출력해라. 설명 문장은 절대 쓰지 마라.

{{
  "entities": [
    {{"name": "엔티티명", "type": "Person/Organization/Project/Field/Activity/University/Lab 등"}}
  ],
  "relations": [
    {{"source": "엔티티명", "target": "엔티티명", "relation": "관계명"}}
  ]
}}

관계명은 짧고 명확하게 영어 대문자 스타일로 써라.
예: STUDIES_AT, WORKS_AT, FRIEND_OF, INTERESTED_IN, COLLABORATES_WITH, PARTICIPATED_IN

문서:
{text}
"""
    response = llm.invoke(prompt)
    content = clean_json_text(response.content)
    return json.loads(content)


def save_to_neo4j(graph_data: dict) -> None:
    entities = graph_data.get("entities", [])
    relations = graph_data.get("relations", [])

    with driver.session() as session:
        for entity in entities:
            session.run(
                """
                MERGE (e:Entity {name: $name})
                SET e.type = $type
                """,
                name=entity["name"],
                type=entity["type"],
            )

        for rel in relations:
            rel_type = safe_rel_type(rel["relation"])
            query = f"""
            MATCH (a:Entity {{name: $source}})
            MATCH (b:Entity {{name: $target}})
            MERGE (a)-[r:{rel_type}]->(b)
            """
            session.run(
                query,
                source=rel["source"],
                target=rel["target"],
            )


def main():
    with open(TEXT_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    graph_data = extract_graph(text)

    print("=== 추출된 엔티티 ===")
    for e in graph_data.get("entities", []):
        print(f"- {e['name']} ({e['type']})")

    print("\n=== 추출된 관계 ===")
    for r in graph_data.get("relations", []):
        print(f"- {r['source']} -[{r['relation']}]-> {r['target']}")

    save_to_neo4j(graph_data)
    print("\nNeo4j 저장 완료!")


if __name__ == "__main__":
    try:
        main()
    finally:
        driver.close()