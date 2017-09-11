""" Chitragupta - The guy who tracks your contributions to the MetaKGP Github organisation!

Author : Rameshwar Bhaskaran
"""

import requests
import json
import pywikibot
import grequests

ignored_repos = set({'git-exercise'})

def get_all_repos():
    # get a list of all repositories in the MetaKGP org
    r = requests.get("https://api.github.com/orgs/metakgp/repos")

    all_contribs = set()

    if not r.ok:
        print "Looks like something is wrong"
        print r.status_code
        exit(0)
    else:
        repos = json.loads(r.text)

        contrib_urls = [repo['contributors_url'] for repo in repos if repo['name'] not in ignored_repos]

        all_reqs = (grequests.get(u) for u in contrib_urls)

        all_resps = grequests.map(all_reqs)

        for resp in all_resps:
            if resp:
                repo_contribs = json.loads(resp.text)
                all_contribs = all_contribs.union([person['login'] for person in repo_contribs])

        print all_contribs

    return all_contribs

def main():
    consolidated_list = get_all_repos()

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
