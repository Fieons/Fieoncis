# 根据当前虚拟环境所装的依赖包，生成requirements.txt文件

import pkg_resources
from pathlib import Path
import os

def generate_requirements_file(venv_path: str):
    # 注意windows系统和macos系统的斜杠是不同的，shit！！！
    #site_packages_path = Path(venv_path) / 'lib' / 'python3.10' / 'site-packages'
    site_packages_path = Path(os.path.join(venv_path, 'Lib', 'site-packages'))
    print(site_packages_path)
    dists = pkg_resources.find_distributions(site_packages_path)
    with open('requirements.txt', 'w') as f:
        for d in dists:
            print(d)
            f.write(f'{d.project_name}=={d.version}\n')

generate_requirements_file('E:/githubsss/Jenieons/venv')
