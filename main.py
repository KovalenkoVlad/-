import os
import ast
import pylint.lint


def analyze_code(file_path):
    """Аналізує код Python: підраховує кількість функцій, класів, змінних."""
    with open(file_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read())

    num_functions = sum(isinstance(node, ast.FunctionDef) for node in tree.body)
    num_classes = sum(isinstance(node, ast.ClassDef) for node in tree.body)
    num_variables = sum(isinstance(node, ast.Assign) for node in tree.body)

    return {
        "Файл": os.path.basename(file_path),
        "Кількість функцій": num_functions,
        "Кількість класів": num_classes,
        "Кількість змінних": num_variables
    }


def run_pylint(file_path):
    """Запускає pylint для аналізу коду."""
    pylint_opts = [file_path, "--disable=C,R"]  # Вимикаємо деякі категорії зауважень
    pylint.lint.Run(pylint_opts)


if __name__ == "__main__":
    file_name = "example.py"
    if os.path.exists(file_name):
        results = analyze_code(file_name)
        print("Метрики коду:")
        for key, value in results.items():
            print(f"{key}: {value}")
        print("\nPylint аналіз:")
        run_pylint(file_name)
    else:
        print("Файл не знайдено!")
