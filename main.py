import re

def parse_dictionary(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    # Удаляем многострочные комментарии
    lines = remove_multiline_comments(lines)
    
    # Регулярное выражение для поиска имен и значений
    pattern = re.compile(r'var\s+([_a-z]+)\s*:=\s*([\d.]+|\w+\s*[\+\-]\s*\w+);')
    matches = pattern.findall(' '.join(lines))  # Применяем поиск ко всему тексту

    dictionary = {}
    for name, value in matches:
        # Evaluate expressions for variables like `first + second`
        if '+' in value or '-' in value:
            # Split the expression and evaluate it
            parts = re.split(r'(\s*[+-]\s*)', value)
            evaluated_value = evaluate_expression(parts, dictionary)
            dictionary[name] = evaluated_value
        else:
            dictionary[name] = float(value) if '.' in value else int(value)  # Преобразуем значение в число
    
    return dictionary

def remove_multiline_comments(lines):
    inside_multiline_comment = False
    cleaned_lines = []
    
    for line in lines:
        if '#<' in line:
            inside_multiline_comment = True
        if inside_multiline_comment:
            if '#>' in line:
                inside_multiline_comment = False
            continue
        cleaned_lines.append(line)
    
    return cleaned_lines

def evaluate_expression(parts, dictionary):
    result = 0
    current_op = '+'
    
    for part in parts:
        part = part.strip()
        if part in ['+', '-']:
            current_op = part
        elif part.isidentifier():  # Если это имя переменной
            value = dictionary.get(part, 0)  # Если переменной нет, используем 0
            result = apply_operation(result, value, current_op)
        else:  # Это число
            value = float(part) if '.' in part else int(part)
            result = apply_operation(result, value, current_op)
    
    return result

def apply_operation(current, value, operation):
    if operation == '+':
        return current + value
    elif operation == '-':
        return current - value
    return current

def find_maximum(dictionary):
    """Находит максимальное значение среди всех ключей в словаре."""
    return max(dictionary.values(), default=float('-inf'))

file_path = 'config.txt'
parsed_dict = parse_dictionary(file_path)

print("Parsed dictionary:", parsed_dict)

try:
    # Выводим значения всех переменных
    for var, value in parsed_dict.items():
        print(f"{var} = {value}")

    # Вычисляем максимальное значение среди всех переменных
    max_value = find_maximum(parsed_dict)
    print(f"Maximum value among all variables = {max_value}")

except KeyError as e:
    print(f"KeyError: {e}. Please check your config file.")
