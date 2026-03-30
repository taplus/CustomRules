# Code with AGI
import os
import urllib.request
import ssl
from datetime import datetime

def time_label():
    now_time = datetime.now()
    formatted_now_time = '# ' + 'Update Time ' + now_time.strftime("%Y-%m-%d %H:%M:%S") + '\n'
    return formatted_now_time

def merge_rules():
    urls = [
        "https://ruleset.skk.moe/Clash/domainset/clash_fake_ip_filter.txt",
        "https://raw.githubusercontent.com/vernesong/OpenClash/refs/heads/master/luci-app-openclash/root/etc/openclash/custom/openclash_custom_fake_filter.list",
        "https://raw.githubusercontent.com/taplus/CustomRules/refs/heads/main/rulesets/custom_list/custom_openclash_custom_fake_filter.list"
    ]

    exclude_list = [
        "+.lan",
        "+.localdomain",
        "+.home.arpa",
        "this_ruleset_is_made_by_sukkaw.ruleset.skk.moe"
    ]
    # 去掉重复行
    merged_rules = {}

    ctx = ssl.create_default_context()
    # 创建一个未验证的 SSL 上下文，防止某些网络环境下报 SSL 证书错误
    # ctx.check_hostname = False
    # ctx.verify_mode = ssl.CERT_NONE

    for url in urls:
        try:
            # 伪装请求头，防止被服务器拒绝
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
                content = response.read().decode('utf-8')
                
                # 按行分割并处理
                for line in content.splitlines():
                    clean_line = line.strip()
                    # 过滤掉空行和以 # 开头的注释行
                    if not clean_line or clean_line.startswith('#'):
                        continue
                    if clean_line in exclude_list:
                        continue
                    if clean_line not in merged_rules:
                        merged_rules[clean_line] = None
        except Exception as e:
            print(f"[ERROR] Failed to fetch {url}: {e}")
            continue

    # 将去重后的规则进行字母排序，方便查阅
    # merged_rules = list(merged_rules)
    
    output_filename = f"{os.getcwd()}/rulesets/custom_list/my_fake_ip_filter.yaml"
    # 创建目录
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    # 写入 YAML 文件
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(time_label())
            f.write("payload:\n")
            for rule in merged_rules.keys():                
                safe_rule = rule.replace("'", "''")
                f.write(f"  - '{safe_rule}'\n")
        
    except Exception as e:
        print(f"[ERROR] Failed to write file: {e}")
        raise FileExistsError

if __name__ == "__main__":
    merge_rules()
