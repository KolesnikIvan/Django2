import requests
from social_core.exceptions import AuthForbidden
from django.db import transaction

@transaction.atomic
def get_user_location_and_bio(backend, user, response, *args, **kwargs):
# def get_repos_list(backend, user, response, *args, **kwargs):
    resp = requests.get(
        # "https://api.github.com/repositories/",
        "https://api.github.com/user",
        headers={"Authorization": "token %s" % response["access_token"]},
    )
    json = resp.json()
    
    # if not json['location']:
    #     raise AuthForbidden('social_core.backends.github.GithubOAuth2')
    if json['age'] >= 100:
        raise AuthForbidden('social_core.backends.github.GithubOAuth2')
    
    # repos = [r["name"] for r in json]
    # repos = [r["name"] for r in json]
    # user.profile.tagline = ",".join(repos)
    location = json['location']
    user.city = location
    user.ptofile.about = json['bio']
    user.save()

    # if len(repos) < 3:
    #     raise AuthForbidden("social_core.backends.github.GithubOAuth2")
        