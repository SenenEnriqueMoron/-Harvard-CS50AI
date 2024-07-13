import csv
import sys, os
import json
import time, random #quitar
#from util import Node, StackFrontier, QueueFrontier
from tree import ColaClass, NodesClass

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    sys.path.append(".")
    # Load people
    with open(f"degrees/{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": []
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = [row["id"]]
            else:
                names[row["name"].lower()].append(row["id"])

    # Load movies
    with open(f"degrees/{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": []
            }

    # Load stars
    with open(f"degrees/{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)        
        for row in reader:
            try:
                
                people[row["person_id"]]["movies"].append(row["movie_id"])
                movies[row["movie_id"]]["stars"].append(row["person_id"])
            except KeyError:
                pass

def write_temp_file():
    temp = {"people":people,"movies":movies,"names":names }
    # Save the data in a temporary JSON file for faster loading next time.
    with open ("./temp_file.json", "w") as j:
        json.dump(temp, j)

def read_temp_file():
    with open ("temp_file.json", "r") as j:
        data = json.load(j)
        names.update(data["names"])
        people.update(data["people"])
        movies.update(data["movies"])

def convertdictolist(entrada:dict)->list:
    salida=[]
    for key, value in entrada.items():
        salida.append((value, key))
    return salida


#region main
def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "small"#large

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    #read_temp_file()
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")
        
    path = shortest_path(source, target)    
            
            
    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

peliculasdicc = {}
def limpiar_info(infoguardada:list, infonueva:list):
    resultadoinfo = 0
    if len(infonueva) != 0:        
        resultadoinfo = [info for info in infonueva if info not in infoguardada]
    return resultadoinfo

def ValidarPeliculas(peliculassources:list, peliculasTarget:list):    
    for pelitarget in peliculasTarget:
        if pelitarget in peliculassources:
            return pelitarget        
    return None


#region shortest_path
def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    ULTIMO = -1
    INICIO = 0
    
    peliculas_lista = []
    arbol = NodesClass()
    cola = ColaClass()
    print(source)
    find = False
    
    peliculas_lista = people[source]["movies"]
    peliculas_target = people[target]["movies"]
    if len(peliculas_target) == 0 or len(peliculas_lista) == 0:
        return None
    
    cola.add_startree(source)
    pelicula_ultima = peliculas_lista[INICIO]
    cola.add_movietree(pelicula_ultima)
    arbol.add_node(source,pelicula_ultima)
    
    
    
    x=0
    while find == False or len(nodos) > 0:
        nodos = arbol.get_nodo()        
        pelicula_ultima = list(nodos.values())    
        estrellas_nuevas = limpiar_info(cola.get_startree(), movies[pelicula_ultima[ULTIMO]]["stars"])                
        if len(estrellas_nuevas) != 0:            
            source = estrellas_nuevas[ULTIMO]            
            cola.add_startree(source)
            peliculas = people[source]["movies"]           
            
            peliculas_lista = limpiar_info(cola.get_movietree(), peliculas)
            validar_pelicula = ValidarPeliculas(peliculas, peliculas_target)
            
            if validar_pelicula:                
                arbol.add_node(target,validar_pelicula)                            
                return convertdictolist(arbol.get_nodo())                
            
            if len(peliculas_lista) != 0:
                pelicula_ultima = peliculas_lista[INICIO]                
                arbol.add_node(source, pelicula_ultima)                
                cola.add_movietree(pelicula_ultima)
        else:
            nodo_llave = []
            nodo_llave = list(arbol.get_nodo().keys())
            if len(nodo_llave) != 0:
                arbol.del_node(nodo_llave[ULTIMO])
            else:                
                return convertdictolist(arbol.get_nodo())
    return None    

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()

# ToDo : vlimpiar codigo
