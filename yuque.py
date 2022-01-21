# -*- coding: utf-8 -*-
import re
import os


def title():
    print('+------------------------------------------')
    print('[+]  \033[34mGithub : https://github.com/li-yibing/AI-Blog                       \033[0m')
    print('[+]  \033[34m作者: AI Blog                                                        \033[0m')
    print('[+]  \033[34m功能: 语雀文档导出md文件后图片修复                                        \033[0m')
    print('[+]  \033[34m使用格式:  python3 yuque.py                                           \033[0m')
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


def find_all_file(base):
    """遍历文件夹，查找结尾为Markdown的文件"""
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('.md'):
                fullname = os.path.join(root, f)
                yield fullname


if __name__ == '__main__':
    title()
    print('[+]  \033[36m请输入您的文件路径\033[0m')
    md_path = input('[+]  \033[35m路径：\033[0m')
    print(f"markdown path:{md_path}")
    deal_yuque(md_path, md_path)
    print('[+]  \033[36m修复完成，图片修复后文件路径:\033[0m', md_path)
    input('[+]  \033[36m按任意键退出程序\033[0m')
