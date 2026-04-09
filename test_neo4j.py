from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "ksh12345")  # 너 비번

driver = GraphDatabase.driver(URI, auth=AUTH)

try:
    driver.verify_connectivity()
    print("Neo4j 연결 성공!")

    with driver.session() as session:
        result = session.run("RETURN 'Hello from Python!' AS message")
        print(result.single()["message"])

except Exception as e:
    print("오류:", e)

finally:
    driver.close()