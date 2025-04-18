import re

def save_to_file(path:str, content:str) -> None:
    with open(path, 'w') as file:
        file.write(str(content))

def get_cookies_data(path:str) -> str:
    data = ''
    with open(path) as file:
        data = '; '.join(['='.join(line.strip().split()) for line in file.readlines()])
    # print(data)
    return data

def generate_filename_and_save_content(path:str, result:str, url) -> None:
    segments = re.findall(r'(https)?:\/\/(www\.)?(\w*)\..*\/(\w*)', url)
    if not segments or len(segments) < 1:
        file_path = f'{path}/{url.replace("/", "").replace(".", "").replace(":", "")}.md'
    else:
        file_path = f'{path}/{segments[0][2]}-{segments[0][3]}.md'
    save_to_file(file_path, result or 'Not found')

if __name__ == "__main__":
    get_cookies_data('./cookies.txt')
