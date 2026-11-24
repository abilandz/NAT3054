# Homework 4: Git (2/2)

**Last update:** 20261124-1

**Challenge #1:** As a starting point for this challenge, consider the following situation in the project development:

```mermaid
%%{init: {
  'theme': 'neutral'
}}%%
gitGraph
   commit id: "change 1"
   commit id: "change 2"
   branch devel
   commit id: "exp. change 1"
   checkout main
   commit id: "change 3"
   checkout devel
   commit id: "exp. change 2"
   checkout main
   commit id: "change 4"
```

Before continuing with development on the 'main' branch, the developer realizes that the commit 'exp. change 1' on the 'devel' branch is validated and ready to be integrated into the 'main' branch, and in fact it's desperately needed on the 'main' branch before further development can continue. On the other hand, the commit 'exp. change 2' on the 'devel' branch is still under scrutiny and is not yet ready to be integrated into the 'main' branch.  

Write the Git commands required to achieve the following:

1. Incorporate only the commit 'exp. change 1' from the 'devel' branch into the 'main' branch;
2. By mistake, the developer repeats Step 1 also for the still-erroneous commit 'exp. change 2', only to realize that after that the version of the project on the 'main' branch can no longer be compiled. How to revert this step entirely, i.e. how to bring the status of the Git repository to the state it was in before this mistake was made; 
3. At some point later, after further development on both 'main' and 'devel' branches, all commits from the 'devel' branch are validated and ready to be incorporated into the 'main' branch, but without duplicating the ones already incorporated in Step 1. How to achieve that?
4. After all commits from the 'devel' branch are incorporated into the 'main' branch, how would you delete the 'devel' branch? In general, is such deletion of the 'devel' branch recommended at that point (+ can you briefly elaborate on your answer)?







**Challenge #2:** **Recovery from deletion.** In this challenge, various recovery scenarios are presented when one intentionally or accidentally deletes something in the Git repository, and needs it later. Outline the procedure and write the concrete Git commands to recover from the following situations: 

1. A file was mistakenly deleted in the current working tree — how to recover its content to the content when that file was last:
    - staged?
    - committed?

2. A file was intentionally deleted, and that deletion was committed. A few weeks later, after several new commits, it suddenly became clear that the file is actually still needed. How to recover its content as it was just before it was deleted?

3. An entire branch was deleted by mistake &mdash; how can it be recovered?
4. The hard disk that hosted the local Git repository is broken beyond repair. Fortunately and prudently, the project is also hosted online (e.g. on [GitHub](https://github.com/) or [GitLab](https://about.gitlab.com/)) and you have regularly pushed your commits. How do you resume local development on a new hard disk?

