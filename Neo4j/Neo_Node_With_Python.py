from neo4j import GraphDatabase

uri = "bolt://localhost:7687"

user = "neo4j"
password = "neo4j/password"

driver = GraphDatabase.driver(uri, auth=(user, password))

def run_query(query):
    with driver.session() as session:
        result = session.run(query)
        return result

person1 = "CREATE (p:Person {name: 'Alice', age: 30})"
person2 = "CREATE (p:Person {name: 'Bob', age: 25})"
person3 = "CREATE (p:Person {name: 'Charlie', age: 35})"

run_query(person1)
run_query(person2)
run_query(person3)

query_all_persons = "MATCH (p:Person) RETURN p.name, p.age"

with driver.session() as session:
    result = session.run(query_all_persons)
    results_list = list(result)


for record in results_list:
    print(f"Name: {record['p.name']}, Age: {record['p.age']}")

