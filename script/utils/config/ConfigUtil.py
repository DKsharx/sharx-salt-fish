import logging

import yaml

from script.utils.config import ConfigConstants

run_time_data_path = "assets/config.yaml"


def get_value(key):
    keys = key.split('.')
    with open(run_time_data_path, 'r', encoding="utf-8") as file:
        yamlData = yaml.safe_load(file)
        for k in keys:
            yamlData = yamlData[k]
        return yamlData


def set_value(key, value):
    with open(run_time_data_path, 'r', encoding="utf-8") as file:
        data = yaml.safe_load(file)
    keys = key.split('.')
    nested_dict = data
    for key in keys[:-1]:
        nested_dict = nested_dict[key]

    # 设置新的值
    nested_dict[keys[-1]] = value
    with open(run_time_data_path, 'w', encoding="utf-8") as file:
        yaml.safe_dump(data, file, default_flow_style=False)

def get_app_version():
    with open('assets/app/version.txt', 'r', encoding='utf-8') as file:
        return file.read()
app_version = get_app_version()


def check_config():
    if not get_value(ConfigConstants.app_path_key):
        raise Exception('未配置启动路径,请前往设置配置！')

def get_useragent():
    return {
        "User-Agent": f"March7thAssistant/{app_version}"
    }
