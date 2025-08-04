import os

project_dir = '.'  # Корень проекта
output_file = 'project_code.txt'
exclude_dirs = {'.venv','venv', '__pycache__', '.git', '.idea', '.mypy_cache', '.pytest_cache'}

extra_files = {'Dockerfile', 'docker-compose.yml', 'docker-compose.yaml'}
nginx_dirs = {'nginx'}
nginx_extensions = {'.conf'}

def should_include_file(file_path, file_name):
    if file_name.endswith('.py') and not file_name.endswith('.pyc'):
        return True
    if file_name in extra_files:
        return True
    if any(file_name.endswith(ext) for ext in nginx_extensions):
        return True
    if 'nginx' in file_path.split(os.sep):  # если файл внутри папки nginx
        return True
    return False

with open(output_file, 'w', encoding='utf-8') as outfile:
    for root, dirs, files in os.walk(project_dir):
        # Исключаем ненужные директории
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            file_path = os.path.join(root, file)
            if should_include_file(file_path, file):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()
                        outfile.write(f'# File: {file_path}\n')
                        outfile.write(code + '\n\n')
                except Exception as e:
                    print(f"Ошибка при чтении {file_path}: {e}")
