# Code with AGI
import os
import urllib.request
from urllib.parse import urlparse
import ssl
from datetime import datetime

def time_label():
    now_time = datetime.now()
    formatted_now_time = '# ' + 'Update Time ' + now_time.strftime("%Y-%m-%d %H:%M:%S") + '\n'
    return formatted_now_time

def get_url():
    sukka_base_url = "https://ruleset.skk.moe/Clash/"
    
    sukka_extend_url = {
        "domainset": ["apple_cdn","cdn","clash_fake_ip_filter","download","game-download",
                      "icloud_private_relay","reject","reject_extra","reject_phishing","reject_sukka","speedtest"],
        "non_ip": ["ai","apple_cdn","apple_cn","apple_intelligence","apple_services",
                   "cdn","cloudmounter","direct","domestic","download","gitlab","global",
                   "global_plus","lan","microsoft","microsoft_cdn","my_direct","my_git","my_plus",
                   "my_proxy","my_reject","my_tw","my_us","neteasemusic","reject-drop","reject-no-drop",
                   "reject-url-regex","reject","sogouinput","stream","stream_biliintl","stream_eu","stream_hk",
                   "stream_jp","stream_kr","stream_tw","stream_us","telegram"],
        "ip": ["apple_services","cdn","china_ip","china_ip_ipv6","domestic",
               "download","lan","neteasemusic","reject","stream","stream_biliintl",
               "stream_eu","stream_hk","stream_jp","stream_kr","stream_tw","stream_us","telegram","telegram_asn"]
    }
 
    extra_url = ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Google/Google.list"]

    full_url = [f"{sukka_base_url}{k}/{v}.txt" for k, vs in sukka_extend_url.items() for v in vs]
    full_url.extend(extra_url)
    return full_url

def clean_content(content, exclude_list):
    # 按行分割并处理
    clean_rules={}
    for line in content.splitlines():
        clean_line = line.strip()
        # 过滤掉空行和以 # 开头的注释行
        if not clean_line or clean_line.startswith('#'):
            continue
        if any(x in clean_line for x in exclude_list):
            continue
        # 去掉重复
        if clean_line not in clean_rules:
            clean_rules[clean_line] = None
    return clean_rules

def download_and_transform():
    # SSL 配置
    ctx = ssl.create_default_context()
    # ctx.check_hostname = False
    # ctx.verify_mode = ssl.CERT_NONE
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    for url in get_url():
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx) as response:
                content = response.read().decode('utf-8')
        except Exception as e:
            print(f"[ERROR] Failed to fetch {url}: {e}")
            continue       
 
        # 创建文件目录
        # URL 子字符串转换为如["domainset",applecdn.txt"]的列表
        path_parts = urlparse(url).path.strip('/').split('/')
        # extend_url 的文件放到 non_ip 目录
        category = path_parts[-2] if path_parts[-2] in ["domainset","non_ip","ip"] else "non_ip"
        # 创建目录
        output_dir = os.path.join(os.getcwd(),"rulesets","sukka",category)
        os.makedirs(output_dir, exist_ok=True)
        
        # 清洗数据
        # 排除的规则列表
        exclude_list = [
            "this_ruleset_is_made_by_sukkaw.ruleset.skk.moe",
            "7h1s_rul35et_i5_mad3_by_5ukk4w-ruleset.skk.moe"
        ]        
        clean_rules = clean_content(content, exclude_list)

        # 写入 YAML 文件       
        filename = os.path.splitext(path_parts[-1])[0].lower()
        output_path = os.path.join(output_dir, f"{filename}.yaml")
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(time_label())
                f.write("# Cited from https://ruleset.skk.moe/ with Thanks\n")
                f.write("payload:\n")
                for rule in clean_rules.keys():
                    safe_rule = rule.replace("'", "''")
                    f.write(f"  - '{safe_rule}'\n")
        except Exception as e:
            print(f"[ERROR] Failed to write file: {e}")
            continue

if __name__ == "__main__":
    download_and_transform()
