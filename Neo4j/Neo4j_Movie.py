from neo4j import GraphDatabase

uri = "bolt://localhost:7687"

user = "neo4j"
password = "neo4j/password"

driver = GraphDatabase.driver(uri, auth=(user, password))


def run_query(query):
    with driver.session() as session:
        result = session.run(query)
        return list(result)

actors = [
    "CREATE (a:Actor {name: 'Tom Hanks'})",
    "CREATE (a:Actor {name: 'Meryl Streep'})",
    "CREATE (a:Actor {name: 'Tom Cruise'})",
    "CREATE (a:Actor {name: 'Julia Roberts'})",
]

movies = [
    "CREATE (m:Movie {title: 'Forrest Gump', year: 1994})",
    "CREATE (m:Movie {title: 'The Post', year: 2017})",
    "CREATE (m:Movie {title: 'Top Gun', year: 1986})",
    "CREATE (m:Movie {title: 'Pretty Woman', year: 1990})",
]

for actor in actors:
    run_query(actor)

for movie in movies:
    run_query(movie)

relationships = [
    "MATCH (a:Actor {name: 'Tom Hanks'}), (m:Movie {title: 'Forrest Gump'}) CREATE (a)-[:ACTED_IN]->(m)",
    "MATCH (a:Actor {name: 'Tom Hanks'}), (m:Movie {title: 'The Post'}) CREATE (a)-[:ACTED_IN]->(m)",
    "MATCH (a:Actor {name: 'Meryl Streep'}), (m:Movie {title: 'The Post'}) CREATE (a)-[:ACTED_IN]->(m)",
    "MATCH (a:Actor {name: 'Tom Cruise'}), (m:Movie {title: 'Top Gun'}) CREATE (a)-[:ACTED_IN]->(m)",
    "MATCH (a:Actor {name: 'Julia Roberts'}), (m:Movie {title: 'Pretty Woman'}) CREATE (a)-[:ACTED_IN]->(m)",
]

for relationship in relationships:
    run_query(relationship)

def recommend_movies(liked_actor_name):
    query = f"""
    MATCH (liked_actor:Actor {{name: '{liked_actor_name}'}})-[:ACTED_IN]->(liked_movie:Movie)
    MATCH (other_actor:Actor)-[:ACTED_IN]->(liked_movie)
    MATCH (other_actor)-[:ACTED_IN]->(recommended_movie:Movie)
    WHERE NOT (liked_actor)-[:ACTED_IN]->(recommended_movie)
    RETURN DISTINCT recommended_movie.title AS title, recommended_movie.year AS year
    ORDER BY year DESC
    """

    results = run_query(query)
    return results


def check_data():
    query_actors = "MATCH (a:Actor) RETURN a.name"
    query_movies = "MATCH (m:Movie) RETURN m.title"
    
    actors = run_query(query_actors)
    movies = run_query(query_movies)
    
    print("Actors in the database:")
    for record in actors:
        print(record["a.name"])
        
    print("Movies in the database:")
    for record in movies:
        print(record["m.title"])

#check_data()


def check_relationships():
    query_relationships = "MATCH (a:Actor)-[:ACTED_IN]->(m:Movie) RETURN a.name, m.title"
    relationships = run_query(query_relationships)
    
    print("Actors and Movies with relationships:")
    for record in relationships:
        print(f"{record['a.name']} acted in {record['m.title']}")

#check_relationships()

liked_actor_name = "Tom Hanks"
recommended_movies = recommend_movies(liked_actor_name)

print(f"Movie recommendations based on liking {liked_actor_name}:")
for record in recommended_movies:
    print(f"{record['title']} ({record['year']})")
