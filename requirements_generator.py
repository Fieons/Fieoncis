# 根据当前虚拟环境所装的依赖包，生成requirements.txt文件

import pkg_resources
from pathlib import Path

def generate_requirements_file(venv_path: str):
    site_packages_path = Path(venv_path) / 'lib' / 'python3.10' / 'site-packages'
    dists = pkg_resources.find_distributions(str(site_packages_path))
    with open('requirements.txt', 'w') as f:
        for d in dists:
            f.write(f'{d.project_name}=={d.version}\n')

generate_requirements_file('/Users/smart_boy/Desktop/githubsss/Jenieons/venv')
