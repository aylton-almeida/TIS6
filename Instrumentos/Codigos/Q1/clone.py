import os
import urllib.request
import pandas
from github import Github
import subprocess

# from dotenv import load_dotenv
# load_dotenv()


repos = []


def getRepoNames():
    data = pandas.read_csv("repos.csv")
    repoNames = data['name_with_owner'].tolist()
    return repoNames

def getUiRepoNames():
    data = pandas.read_csv('uiRepos.csv')
    uiRepoNames = data["name"].tolist()
    return uiRepoNames

def hasDesignRepo(designRepoNames, repositoriesList):

    cloner = Github("25842f387cfa45632f587a50d4c9c5b70ff9e815")

    hasDesignRepoList = []
    hasNoDesignRepoList = []

    for repoName in repositoriesList:
        # print(repoName)
        try:
            repoOne = cloner.get_repo(repoName)
            packageJson = repoOne.get_contents("package.json")
            decodedPackageJson = packageJson.decoded_content.decode("utf-8")
            for designName in designRepoNames:
                if (decodedPackageJson.find(designName) > 0):
                    hasDesignRepoList.append(repoName)
                    break
                else:
                    continue
            hasNoDesignRepoList.append(repoName)
        except:
            hasNoDesignRepoList.append(repoName)
            pass
    print('WITH DESIGN REPO')
    print(len(hasDesignRepoList))
    print('WITHOUT DESIGN REPO')
    print(len(hasNoDesignRepoList))
    # df_has_design_repo = pandas.DataFrame(hasDesignRepoList, columns=["name"])
    # df_has_design_repo.to_csv('test.csv', index=False)


def main():
    hasDesignRepo(getUiRepoNames(), getRepoNames())


main()