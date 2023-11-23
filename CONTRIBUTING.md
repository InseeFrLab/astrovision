# Contributing guidelines

The `astrovision` project welcomes contributions. If you have found a bug or would like to suggest a new feature, you can open an issue. You can also directly submit a pull request to suggest a change. To do so, fork the repository and clone the forked repository:

```bash
git clone https://github.com/<your-username>/astrovision.git
```

From there, you can make any changes you want. Once you are satisfied with your changes, you can commit them and push them back to your fork. If you want to make multiple changes, it's best to create separate branches and pull requests for each change:

```bash
git checkout main
git branch <descriptive-branch-name>
git checkout <descriptive-branch-name>
git add <files-you-changed...>
git commit -m "descriptive commit message"
git push
```

For changes to Python code, you need to ensure that your code is well-tested and all linters pass before the pull request is reviewed. All pull requests should be made against the main branch.
