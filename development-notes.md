### Contributing ###

I'm happy to receive patches to Pysolar. Please make sure that your patch does not break the test suite before you send a pull request. If that's confusing, please feel free to send me an email.

### Release procedure ###

(These notes are just to remind Brandon how releases worked the last time he released a new version of Pysolar.)

1. Patch, test, patch, test, until it works right. Test includes running test/testsolar.py and the validation suite.
2. To run the validation suite, install Jupyter Notebook, Matplotlib, and Pandas. Then run each cell of `test/validation.ipynb`.
3. Realize that the code in `query_usno.py` to pull from the US Naval Observatory is broken; decide the basic test code is good enough.
4. Commit and push to Github.
5. Update the version number in setup.py.
6. Update contributors.markdown if needed.
7. Add a release on Github that matches the new version number: https://github.com/pingswept/pysolar/releases
8. Put PyPI credentials in `~/.pypirc`.
9. Install Twine and Wheel.
10. `sudo python3 setup.py bdist_wheel`
11. `sudo python3 setup.py sdist`?
12. Check that the right stuff exists in `dist`. There should be just a `tar.gz` and a `.whl`.
13. `twine upload dist/*`
14. Figure out how to get a DOI from Zenodo.
