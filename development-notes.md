### Contributing ###

I'm happy to receive patches to Pysolar. Please make sure that your patch does not break the test suite before you send a pull request. If that's confusing, please feel free to send me an email.

### Release procedure ###

(These notes are just to remind Brandon how releases worked the last time he released a new version of Pysolar.)

1. Patch, test, patch, test, until it works right. Test includes running test/testsolar.py and the validation suite.
2. To run the validation suite, install Jupyter Notebook, Matplotlib, and Pandas. Then run each cell of `test/validation.ipynb`.
3. Commit and push to Github.
4. Update the version number in setup.py.
5. Update contributors.markdown if needed.
6. Add a release on Github that matches the new version number: https://github.com/pingswept/pysolar/releases
7. Put PyPI credentials in `~/.pypirc`.
8. Install Twine.
9. `sudo python3 setup.py bdist_wheel`
10. `sudo python3 setup.py sdist`?
11. Check that the right stuff exists in `dist`. There should be just a `tar.gz` and a `.whl`.
12. `twine upload dist/*`
