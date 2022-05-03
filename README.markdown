## Pysolar ##

[![Test Python package](https://github.com/pingswept/pysolar/actions/workflows/testpackage.yml/badge.svg)](https://github.com/pingswept/pysolar/actions/workflows/testpackage.yml)

Pysolar is a collection of Python libraries for simulating the irradiation of any point on earth by the sun. It includes code for extremely precise ephemeris calculations, and more.

# Note: right now, the latest commits of Pysolar don't work with Python 2.x #

* Release 0.6 works with 2.x: https://github.com/pingswept/pysolar/releases/tag/0.6 but 0.7 and later have a bunch of changes. They have been validated for Python 3.4, but releases 3.2 or earlier are missing features that the changes require. *

Also, the API has changed slightly:

  * Pysolar now expects you to supply a **timezone-aware datetime**, rather than a naive datetime in UTC. If your results seem crazy, this is probably why.
  * Function names are now `lowercase_separated_by_underscores`, in compliance with [PEP8](https://www.python.org/dev/peps/pep-0008/#function-names).

## Installation ##

Assuming you have Python 3.4 or higher installed, you can install Pysolar with `pip`:

    sudo pip install pysolar

Documentation now appears at [docs.pysolar.org](http://docs.pysolar.org).

## Contributions ##

All contributions go through pull requests on Github.

Editing [the documentation](http://docs.pysolar.org) is particularly easy-- just click the "Edit on Github" link at the top of any page.

Code contributions are welcome under the terms of the GPLv3 license. If you're unfamiliar with Github, you could start with [this guide to working on open source projects](https://guides.github.com/activities/contributing-to-open-source/).

## Support ##

Your first move should be to read the [documentation](http://docs.pysolar.org) and think. But you've probably already tried that.

Your second move is to ask a question on the [pysolar-discuss](http://lists.pysolar.org) mailing list. The original author of Pysolar, [Brandon Stafford](http://rascalmicro.com), monitors the mailing list. Please understand that I wrote (most of) Pysolar around a decade ago when I worked in the solar industry. Now, I'm an electrical engineer who just maintains Pysolar as a fun hobby. The other people on the list are other users like you-- some are experts; some are amateurs. None of them are getting paid for this.

To subscribe to the mailing list, send a blank email to pysolar-discuss+subscribe@pysolar.org. After a few minutes, you'll get a confirmation message; reply to the confirmation to complete the subscription.

In order to post to the list, you have to subscribe. You also have to pass a threshold of civil discourse regulated by me.

The archive of the list is publicly available here: http://lists.pysolar.org/.

If you ever want to unsubscribe, send an email to pysolar-discuss+unsubscribe@pysolar.org and reply to the confirmation message. If you run into trouble, just send me an email at brandon@pingswept.org, and I'll remove your address manually.

Please report bugs to [the issue tracker on Github](https://github.com/pingswept/pysolar/issues); I am automatically notified when a new issue is opened.

## License ##

Pysolar is licensed under [the GPLv3](https://www.gnu.org/licenses/gpl-3.0.html).
