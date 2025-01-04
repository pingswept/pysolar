### Contributing ###

I'm happy to receive patches to Pysolar. Please make sure that your patch does not break the test suite before you send a pull request. If that's confusing, please feel free to send me an email.

### Release procedure ###

(These notes are just to remind Brandon how releases worked the last time he released a new version of Pysolar.)

1. Install pip: python3 -m ensurepip --upgrade
2. Install Twine, Wheel, Jupyter Notebook, Matplotlib and Pandas: `pip3 install twine wheel jupyter matplotlib pandas`
3. Clone the latest version of Pysolar.
4. Install: `sudo python3 ./setup.py install`
5. Patch, test, patch, test, until it works right. Test includes running test/testsolar.py and the validation suite.
6. To run the validation suite, use the previously installed Jupyter Notebook, Matplotlib, and Pandas. Start the notebook server with `python3 -m notebook`
7. Run each cell of `test/validation.ipynb`.
8. Realize that the code in `query_usno.py` to pull from the US Naval Observatory is broken; decide the basic test code is good enough.
9. Update the version number in setup.py.
10. Update contributors.markdown if needed.
11. Commit and push to Github.
12. Add a release on Github that matches the new version number: https://github.com/pingswept/pysolar/releases
13. Put PyPI credentials in `~/.pypirc`. Example file below.
10. `sudo python3 setup.py bdist_wheel`
11. `sudo python3 setup.py sdist`?
12. Check that the right stuff exists in `dist`. There should be just a `tar.gz` and a `.whl`. We don't want `egg` files any more.
13. `python3 -m twine upload --repository pysolar dist/*`
14. Figure out how to get a DOI from Zenodo.

### .pypirc file ###

```
[distutils]
  index-servers =
    pypi
    pysolar

[pypi]
  username = __token__
  password = # either a user-scoped token or a project-scoped token you want to set as the default
[pysolar]
  repository = https://upload.pypi.org/legacy/
  username = __token__
  password = # API token goes here
```
