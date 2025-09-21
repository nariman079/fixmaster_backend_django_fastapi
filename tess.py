import os

# Определяем расширения файлов, которые нужно читать
EXTENSIONS = {'.py', '.yml', '.yaml',}
FILENAMES = {'Dockerfile', 'dockerfile'}

# Имя выходного файла
OUTPUT_FILE = 'output.txt'

def should_include_file(filename):
    """Проверяет, нужно ли включать файл в вывод."""
    if filename in FILENAMES:
        return True
    _, ext = os.path.splitext(filename)
    return ext.lower() in EXTENSIONS

def is_ignored_directory(dir_path):
    """Проверяет, нужно ли игнорировать директорию."""
    ignored_dirs = {'.git', '__pycache__', '.venv', 'venv', 'node_modules', '.vscode', '.idea'}
    dir_parts = [part for part in dir_path.split(os.sep) if part]
    return any(part in ignored_dirs for part in dir_parts)

def main():
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
            for root, dirs, files in os.walk('.'):
                # Пропускаем игнорируемые директории
                if is_ignored_directory(root):
                    continue
                
                for file in files:
                    if should_include_file(file):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as infile:
                                content = infile.read()
                                outfile.write(f"=== {file_path} ===\n")
                                outfile.write(content)
                                outfile.write("\n\n")
                                print(f"Добавлен файл: {file_path}")
                        except Exception as e:
                            print(f"Не удалось прочитать файл {file_path}: {e}")
                            # Записываем информацию об ошибке в output файл
                            outfile.write(f"=== {file_path} ===\n")
                            outfile.write(f"ОШИБКА ЧТЕНИЯ: {str(e)}\n\n")
    except Exception as e:
        print(f"Ошибка при создании файла {OUTPUT_FILE}: {e}")

if __name__ == '__main__':
    main()
    print(f"Сбор файлов завершен. Результат сохранен в {OUTPUT_FILE}")

