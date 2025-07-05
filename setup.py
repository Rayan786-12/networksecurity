from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    '''
    This function will return list of requirements

    '''
    requirement_lst:List[str]=[]
    # print(requirement_lst)
    try:
        with open('requirements.txt','r') as file:
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
                if requirement and requirement !='-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")
    
    return requirement_lst
# print(get_requirements())
setup(
    name="NetworkSecurity",
    version='0.0.1',
    author='Rayan786-1212',
    author_email='rayanriaz1212@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()

)