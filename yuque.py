import re
from typing import List


def title():
    print('+------------------------------------------')
    print('[+]  \033[34mGithub : https://github.com/li-yibing/AI-Blog                       \033[0m')
    print('[+]  \033[34m作者: AI Blog                                                        \033[0m')
    print('[+]  \033[34m功能: 语雀文档导出md文件后图片修复                                        \033[0m')
    print('[+]  \033[36m使用格式:  python3 yuque.py                                           \033[0m')
    print('+------------------------------------------')


def deal_yuque(input_path: str, output_path: str):
    new_md = []
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f.readlines():
            line = re.sub(r'png#(.*)+', 'png)', line)
            new_md.append(line)

    with open(output_path, 'w', encoding='utf-8', errors='ignore') as f:
        for new_md in new_md:
            f.write(str(new_md))


if __name__ == '__main__':
    title()
    print('[+]  \033[36m请输入您的文件路径, 如：乌鸦安全.md\033[0m')
    old_path = input('[+]  \033[35m路径：\033[0m')
    new_path = 'new_' + old_path
    deal_yuque(old_path, new_path)
    print('[+]  \033[36m修复完成，图片修复后文件路径:\033[0m', new_path)
