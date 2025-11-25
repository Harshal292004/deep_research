"""GitHub tool implementation"""

from typing import Optional

from github import Github

from src.config import settings
from src.helpers.logger import log
from src.models.tools import (
    GitHubLanguageItem,
    GitHubLanguageOutput,
    GitHubLanguageQuery,
    GitHubOrgOutput,
    GitHubOrgQuery,
    GitHubRepoOutput,
    GitHubRepoQuery,
    GitHubUserOutput,
    GitHubUserQuery,
)


class GitHubInspector:
    def __init__(self, token: Optional[str] = None):
        self.g = Github(token or settings.GITHUB_ACCESS_TOKEN)

    async def get_user_by_name(self, input: GitHubUserQuery) -> GitHubUserOutput:
        try:
            log.info(f"GitHub user lookup: {input.username}")
            user = self.g.get_user(input.username)
            log.info(f"GitHub user found: {user.login}")
            return GitHubUserOutput(
                login=user.login,
                name=user.name,
                public_repos=user.public_repos,
                followers=user.followers,
                bio=user.bio,
                location=user.location,
            )
        except Exception as e:
            log.error(f"GitHub user lookup failed: {e}")
            return GitHubUserOutput(
                login="", name="", public_repos=0, followers=0, bio="", location=""
            )

    async def get_repo_by_name(self, input: GitHubRepoQuery) -> GitHubRepoOutput:
        try:
            log.info(f"GitHub repo lookup: {input.full_name}")
            repo = self.g.get_repo(input.full_name)
            log.info(f"GitHub repo found: {repo.name}")
            return GitHubRepoOutput(
                name=repo.name,
                full_name=repo.full_name,
                description=repo.description,
                stars=repo.stargazers_count,
                forks=repo.forks_count,
                language=repo.language,
                topics=repo.get_topics(),
            )
        except Exception as e:
            log.error(f"GitHub repo lookup failed: {e}")
            return GitHubRepoOutput(
                name="",
                full_name="",
                description="",
                stars=0,
                forks=0,
                language="",
                topics=[],
            )

    async def get_org_by_name(self, input: GitHubOrgQuery) -> GitHubOrgOutput:
        try:
            log.info(f"GitHub org lookup: {input.org_name}")
            org = self.g.get_organization(input.org_name)
            members = [member.login for member in org.get_members()][
                : input.member_limit
            ]
            log.info(f"GitHub org found: {org.name}, members: {len(members)}")
            return GitHubOrgOutput(
                login=org.login,
                name=org.name,
                description=org.description,
                public_repos=org.public_repos,
                members=members,
            )
        except Exception as e:
            log.error(f"GitHub org lookup failed: {e}")
            return GitHubOrgOutput(
                login="", name="", description="", public_repos=0, members=[]
            )

    async def search_repos_by_language(
        self, input: GitHubLanguageQuery
    ) -> GitHubLanguageOutput:
        try:
            log.info(f"GitHub language search: {input.language}")
            result = self.g.search_repositories(query=f"language:{input.language}")
            repos = []
            repo = result.get_page(0)
            for r in repo:
                repos.append(
                    GitHubLanguageItem(
                        name=r.name,
                        full_name=r.full_name,
                        stars=r.stargazers_count,
                        url=r.html_url,
                    )
                )
                if len(repos) == input.limit:
                    break
            log.info(f"GitHub language search completed: {len(repos)} repos")
            return GitHubLanguageOutput(results=repos)
        except Exception as e:
            log.error(f"GitHub language search failed: {e}")
            return GitHubLanguageOutput(results=[])


# Note: GitHubInspector should be instantiated per request with appropriate token
