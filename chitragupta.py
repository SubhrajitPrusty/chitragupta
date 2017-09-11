""" Chitragupta - The guy who tracks your contributions to the MetaKGP Github organisation!

Author : Rameshwar Bhaskaran
"""

import requests
import json
import pywikibot

ignored_repos = set({'git-exercise'})

def get_all_repos():
    # get a list of all repositories in the MetaKGP org
    r = requests.get("https://api.github.com/orgs/metakgp/repos")

    if not r.ok:
        print "Looks like something is wrong"
        print r.status_code
        exit(0)
    else:
        repos = json.loads(r.text)
        contributor_urls = {}
        for repo in repos:
            if repo['name'] not in ignored_repos:
                contributor_urls[repo['name']] = repo['contributors_url']
        contributors = {}
        for repo, url in contributor_urls.items():
            try:
                print "Getting ", repo
                # ignore the sandbox
                contributor_response = requests.get(url)
                contributors[repo] = set()
                repo_contributors = json.loads(contributor_response.text)
                for contributor in repo_contributors:
                    contributors[repo].add(contributor['login'])
            except Exception as e:
                print "Failed due to ", str(e)
                pass

    consolidated_list = set()
    for repo in contributors:
        print repo, contributors[repo]
        consolidated_list = consolidated_list.union(contributors[repo])
    return contributors, consolidated_list

def main():
    contributors, consolidated_list = get_all_repos()

    # Build the markup for the page
    text = "<b>List of contributors on Github:</b><br/><br/>"

    consolidated_list = list(consolidated_list)
    consolidated_list.sort()

    for iter, github_username in enumerate(consolidated_list):
        url = "https://github.com/%s" % github_username
        text += "%s. [%s %s] <br>" % (iter + 1, url, github_username)

    # Update the page with this markup

    site = pywikibot.Site()
    page = pywikibot.Page(site, u'MetaKGP_Github_Contributors')
    page.text = text
    page.save(u'Update list of contributors')

if __name__ == "__main__":
    main()
