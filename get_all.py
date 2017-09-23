from git import Repo, exc
from git.exc import GitCommandError
from github import Github
import logging

ROUTE_DIR = 'localpath'
ORGANIZATION = 'companyname'
LOGIN = 'gitlogin'
PASS = 'gitpass'

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')
log = logging.getLogger(__name__)
logging.getLogger('git').setLevel(logging.INFO)
logging.getLogger('github').setLevel(logging.INFO)

g = Github(login_or_token=LOGIN, password=PASS)

org = g.get_organization(ORGANIZATION)
repos = org.get_repos()

for repo in repos:
    try:
        Repo.clone_from('git@github.com:{}/{}'.format(ORGANIZATION, repo.name), '{}{}'.format(ROUTE_DIR, repo.name))
        print('Cloned - {}'.format(repo.name))
    except GitCommandError as e:
        try:
            local_repo = Repo(path='{}{}'.format(ROUTE_DIR, repo.name))
            local_repo.remotes.origin.pull()
            print('Pulled - {}'.format(repo.name))
        except Exception as e2:
            logging.info("Error with repo - {}".format(repo.name))
            logging.exception(e2.message)
