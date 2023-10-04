# list_to_set.py

def list_to_set(input_list):
    return set(input_list)

if __name__ == "__main__":
    input_list = [1, 2, 3, 4, 3, 2, 1]  # Ejemplo de lista
    result_set = list_to_set(input_list)
    print("Lista original:", input_list)
    print("Conjunto resultante:", result_set)
