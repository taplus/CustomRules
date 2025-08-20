import requests,re,os
from datetime import datetime

def download_file(filename):
    file_path = '{}/rulesets/sukka/{}.list'.format(os.getcwd(),filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
    url = 'https://ruleset.skk.moe/Clash/domainset/{}.txt'.format(filename)
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        if response.status_code == 200 and response.content:
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
    except requests.RequestException as e:
        raise TimeoutError('Download Error')

def rewrite_file(filename):
    # 定义文件路径
    file_path = '{}/rulesets/sukka/{}.list'.format(os.getcwd(),filename)
    temp_file = '{}/rulesets/sukka/{}.txt'.format(os.getcwd(),filename)
    # 创建临时文件
    with open(file_path, 'r',encoding='utf-8') as file, open(temp_file,'w',encoding='utf-8') as outfile:
        # 读取原始文件内容
        lines = file.readlines()
        # 在内存中对内容进行修改
        for line in lines:
            # 跳过包含 `#` 的行
            if re.search(r'#', line):
                continue  # 跳过此行
            # 跳过包含 'this_ruleset_is_made_by_sukkaw' 的行
            if re.search(r'this_ruleset_is_made_by_sukkaw', line):
                continue  # 跳过此行
            if re.search(r'7h1s_rul35et_i5_mad3_by_5ukk4w-ruleset.skk.moe', line):
                continue  # 跳过此行
            # 删除每行 '+.' ，并在每一行的开头添加 "Domain-suffix"
            line = re.sub(r'^\+\.', '', line.strip())
            if re.search(r'\w', line):
                line = "DOMAIN-SUFFIX," + line + '\n'
            outfile.write(line)

    os.replace(temp_file,file_path)
 
def time_label():
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    time_file = '{}/rulesets/sukka/ActionTime.txt'.format(os.getcwd())
    with open(time_file,'a+',encoding='utf-8') as file:
        file.write(formatted_time + '\n')


def main():
    for filename in ['apple_cdn','cdn','download']:
        download_file(filename)
        rewrite_file(filename)
    time_label()

if __name__=='__main__':
    main()
