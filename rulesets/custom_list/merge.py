import requests
import os,yaml
from datetime import datetime

def get_path(filename):
    if filename in ['clash']:
        file_path = '{}/templates/{}.yml'.format(os.getcwd(),filename)
    else:
        file_path =  '{}/rulesets/custom_list/{}'.format(os.getcwd(),filename)
    return file_path
    
def download_file(filename):
    # 检查是否存在旧文件，如有则删除并下载最新文件
    file_path = get_path(filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
    url = 'https://raw.githubusercontent.com/vernesong/OpenClash/master/luci-app-openclash/root/etc/openclash/custom/{}'.format(filename)
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

# 合并两个list文件写到下载 list 中
def merge_list(filename):
    file = get_path(filename)
    custom_file = '{}/rulesets/custom_list/custom_{}'.format(os.getcwd(),filename)
    with open(custom_file,'r',encoding='utf-8') as custom:
        content_custom = custom.read()
    with open(file,'a',encoding='utf-8') as download:
        download.write(content_custom)

# list文件转换为替换文件
def list2newdata(filename):
    list_file = get_path(filename)
    merge_list(filename)
    # 读 list,删除注释行，创建 content 列表
    with open(list_file,'r',encoding='utf-8') as list:
        content = list.read().splitlines()
        content = [line.strip() for line in content]  # 删除每行中的前后空格
        content = [line.strip('\'"') for line in content]  # 删除每行中的引号
        content = [line for line in content if "#" not in line] # 删除注释内容元素
    return content

# yaml文件转换为字典
def yal2dic(filename):
    yaml_file = get_path(filename)
    with open(yaml_file,'r',encoding='utf-8') as file:
        content = yaml.safe_load(file)
    return content

# 更新 yaml 文件
def update_yaml(filename):
    clash_file = get_path('clash')
    
    # 读 clash.yaml 并转为字典
    with open(clash_file,'r',encoding='utf-8') as file:
        data = yaml.safe_load(file)
    
    
    # 更新 yaml 部分内容
    if filename.endswith(".list"):
        keys = ['dns','fake-ip-filter']
        content = list2newdata(filename)
        replace_section(data, keys, content)
    if filename.endswith('.yaml'):
        content = yal2dic(filename)
        data['dns']['fallback-filter'] = content['fallback-filter']

    # 写回 yaml 文件
    with open(clash_file,'w',encoding='utf-8') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)


# 替换 yaml 键值对
def replace_section(data, keys, new_data):
    if len(keys) == 1:
        data[keys[0]] = new_data
    else:
        replace_section(data[keys[0]], keys[1:], new_data)
 
def time_label():
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    time_file = '{}/rulesets/custom_list/ActionTime.txt'.format(os.getcwd())
    with open(time_file,'a+',encoding='utf-8') as file:
        file.write(formatted_time + '\n')


def main():
    # 下载并修改文件
    for filename in ['openclash_custom_fake_filter.list','openclash_custom_fallback_filter.yaml']: 
        download_file(filename)
        update_yaml(filename)
    time_label()

if __name__=='__main__':
    main()