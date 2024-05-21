import requests,re,os

def download_file(filename):
    file_path = '{}/rulesets/sukka/{}.list'.format(os.getcwd(),filename)
    print(file_path)
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
    temp_file = 'temp.txt'
    # 创建临时文件
    with open(file_path, 'r',encoding='utf-8') as file, open(temp_file,'w') as outfile:
        # 读取原始文件内容
        lines = file.readlines()
        # 在内存中对内容进行修改
        for i, line in enumerate(lines):
            # 删除行中以 '.+' 开头的部分，并在每一行的开头添加 "Domain-suffix"
            lines[i] = re.sub(r'^\+\.', '', line.strip())
            lines[i] = "DOMAIN-SUFFIX," + lines[i] + '\n'
            if not re.match(r'.*#+.*', lines[i]):
                outfile.write(lines[i])
            outfile
        
        os.replace(temp_file,file_path)
 

def main():
    for filename in ['apple_cdn','icloud_private_relay','cdn','download','steam']:
        download_file(filename)
        rewrite_file(filename)

if __name__=='__main__':
    main()