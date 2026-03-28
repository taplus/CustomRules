# Code with AGI
import os
import urllib.request
import ssl
from datetime import datetime

def time_label():
    now_time = datetime.now()
    formatted_now_time = '# ' + 'Update Time ' + now_time.strftime("%Y-%m-%d %H:%M:%S") + '\n'
    return formatted_now_time

def get_url():
    files = {
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
    return [f"{k}/{v}.txt" for k, vs in files.items() for v in vs]

def download_and_transform():
    base_url = "https://ruleset.skk.moe/Clash/"
    exclude_list = [
        "this_ruleset_is_made_by_sukkaw.ruleset.skk.moe",
        "7h1s_rul35et_i5_mad3_by_5ukk4w-ruleset.skk.moe"
    ]

    # SSL 配置
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    for file in get_url():
        url = f"{base_url}{file}"
        output_path = f"{os.getcwd()}/rulesets/sukka/{os.path.splitext(file)[0]}.yaml"
        # 创建目录
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx) as response:
                content = response.read().decode('utf-8')
        except Exception as e:
            continue
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
        # 写入 YAML 文件
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(time_label())
                f.write("# Cited from Sukka's Rulesets with Thanks\n")
                f.write("payload:\n")
                for rule in clean_rules.keys():
                    f.write(f"  - '{rule}'\n")
        except Exception as e:
            continue

def extrafile_transform():
    # 堆成屎了，不要看~~~
    extra_url = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Google/Google.list"
    # SSL 配置
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    output_path = f"{os.getcwd()}/rulesets/sukka/non_ip/{os.path.splitext(os.path.basename(extra_url))[0].lower()}.yaml"
    # 创建目录
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        req = urllib.request.Request(extra_url, headers=headers)
        with urllib.request.urlopen(req, context=ctx) as response:
            content = response.read().decode('utf-8')
    except Exception as e:
        raise ConnectionError
    # 按行分割并处理
    clean_rules={}
    for line in content.splitlines():
        clean_line = line.strip()
        # 过滤掉空行和以 # 开头的注释行
        if not clean_line or clean_line.startswith('#'):
            continue
        # 去掉重复
        if clean_line not in clean_rules:
            clean_rules[clean_line] = None
    # 写入 YAML 文件
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(time_label())
            f.write("# Cited from Blackmatrix7 Rulesets with Thanks\n")
            f.write("payload:\n")
            for rule in clean_rules.keys():
                f.write(f"  - '{rule}'\n")
    except Exception as e:
        raise SyntaxError

if __name__ == "__main__":
    download_and_transform()
    extrafile_transform()
