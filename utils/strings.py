def is_positive_number(value):
    try:
        number_string = float(value) # Convertendo string para float
    except Exception as e:
        return f'Erro: {e}' # Se valor não puder ser convertido
    
    return number_string > 0 # True -> Se o número for positivo. False -> Número negativo