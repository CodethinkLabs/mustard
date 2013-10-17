Mustard README
==============

This is the official repository for the development of Mustard,
the Mapped Uniform System for Tracking Architecture, Requirements
and Design.

Contents
--------

1. Screenshots
2. Mustard data format
3. Creating UML diagrams
4. Installing Mustard
5. Deploying Mustard Using Apache2
6. Hacking Mustard
7. Contributing
8. Copyright and License


1. Screenshots
--------------

### Requirements

![Requirements](https://github.com/CodethinkLabs/mustard/raw/master/data/screenshots/requirements.png "Requirements")

### Architecture

![Architecture](https://github.com/CodethinkLabs/mustard/raw/master/data/screenshots/architecture.png "Architecture")

### Work items

![Work Items](https://github.com/CodethinkLabs/mustard/raw/master/data/screenshots/work-items.png "Work Items")

### History

![History](https://github.com/CodethinkLabs/mustard/raw/master/data/screenshots/history.png "History")

![Diffs](https://github.com/CodethinkLabs/mustard/raw/master/data/screenshots/diff.png "Diffs")


2. Mustard data format
----------------------

### General concepts

Mustard allows you to manage the following information about a project:

  * Requirements
  * Components / Architectures
  * Interfaces
  * Integration strategies
  * Verification criteria
  * Work Items

Mustard reads these elements from YAML files stored in a Git repository.
Every commit in the repository represents a different state of the
overall architecture.

Each element is specified as dictionary with a special key called `kind`
that identifies the type of the element.

Two examples:

    kind: requirement
    title: The software needs to do XYZ

And:

    kind: component
    title: Web application
    description: Some Markdown-formatted text to describe the component.
    parent: components/software

Every element in the project is associated with a unique identifier that
is very similar to a path in a file system. The identifiers allow to
link elements together and thereby establish a bidirectional mapping
from requirements all the way down to work items and back.

How the YAML files are organised in the repository tree is up to the
architects. The element paths are specified as follows:

### Element identifiers

One possible way to store elements in the YAML repository is to use
one file per element. In this case the path to the file, relative to
the repository directory and without the .yaml extension, becomes the
identifier of the element.

For example, a file called

    $repo/requirements/software/feature-xyz.yaml

with the contents

    kind: requirements
    title: Feature XYZ

would result in a requirement element with the identifier
`requirements/software/feature-xyz`.

In addition to this, nested dictionaries in a YAML file can be used as
an effective way to group elements. In this case, the path to the YAML
file plus the hierarchy of dictionary keys leading to the elements
become the element identifiers.

First example: a file called

    $repo/components/software.yaml

with the contents

    webapp:
      kind: component
      title: Web application
      parent: components/software

    phoneapp:
      kind: component
      title: Phone app
      parent: components/software

results in two component elements with the identifiers
`components/software/webapp` and `components/software/phoneapp`.

A file called

    $repo/requirements.yaml

with nested dictionaries

    system:
      software:
        rails:
          kind: requirement
          title: Web application written in Ruby on Rails
      infrastructure:
        heroku:
          kind: requirement
          title: Web app deployment via Heroku

will generate two requirement elements with the identifiers
`requirements/system/software/rails` and
`requirements/system/infrastructure/heroku`.

It is also possible to nest elements like this:

    requirements.yaml:

    system:
      software:
        webapp:
          kind: requirement
          title: There needs to be a web application

          heroku:
            kind: requirement
            title: Web app deployment via Heroku
            parent: requirements/system/software/webapp

The above results in two elements with the identifiers
`requirements/system/software/webapp` and
`requirements/system/software/webapp/heroku`.

### Uniqueness

NOTE: Mustard requires that all identifiers in the project be unique.
It will raise an error whenever there are duplicates in the system and
will try to help you resolve them.

### Supported elements and keys

Project (kind: project):

  Used to state core project configuration.  Entirely optional, but no more
  than one may exist.

  Supported keys:

    - title       (optional)
    - description (optional)
    - copyright   (optional)
    - sort-by     (optional)

  Example:

    kind: project
    title: The FooBar project
    copyright: 2013 Badger Corporation
    sort-by: location
    description: A string in Markdown format.

Requirements (kind: requirement, req, r):

  Used to specify requirements.

  Supported keys:

    - title       (optional)
    - description (optional)
    - tags        (optional)
    - parent      (optional)

  Example:

    kind: requirement
    title: Any string
    description: A string in Markdown format.
    tags:
      - tags/required
      - tags/high-priority
    parent: identifier/of/parent/requirement

Components (kind: component, comp, c):

  Used to specify any components in the system. The result is a
  hierarchy of components also called the "architecture".

  Supported keys:

    - title       (optional)
    - description (optional)
    - tags        (optional)
    - parent      (optional)
    - mapped-here (optional)

  Example:

    kind: component
    title: Any string
    description: A string in Markdown format.
    tags:
      - tags/foo
      - tags/bar
    parent: identifier/of/parent/component
    mapped-here:
      - identifier/of/a/requirement
      - identifier/of/another/requirement

Interfaces (kind: interface, iface, i):

  Used to specify interfaces of components.

  Supported keys:

    - title       (optional)
    - description (optional)
    - tags        (optional)
    - parent      (optional)
    - mapped-here (optional)

  Example:

    kind: interface
    title: Any string
    description: A string in Markdown format.
    tags:
      - tags/foo
      - tags/bar
    parent: identifier/of/parent/component
    mapped-here:
      - identifier/of/a/requirement
      - identifier/of/another/requirement

Integration strategies (kind: integration-strategy, istrat, s):

  Used to specify integration strategies for components.

  Supported keys:

    - title       (optional)
    - description (optional)
    - tags        (optional)
    - parent      (optional)
    - mapped-here (optional)

  Example:

    kind: integration-strategy
    title: Any string
    description: A string in Markdown format.
    tags:
      - tags/foo
      - tags/bar
    parent: identifier/of/parent/component
    mapped-here:
      - identifier/of/a/requirement
      - identifier/of/another/requirement

Verification Criterion (kind: verification-criterion, vcrit, v):

  Used to describe how to verify that an an integration strategy, a component
  or an interface is performed or implemented properly; or how to know if a
  requirement has been met.

  Supported keys:

    - title       (optional)
    - description (optional)
    - tags        (optional)
    - parent      (optional)
    - mapped-here (optional)

  Example:

    kind: verification-criterion
    title: Any string
    description: A string in Markdown format.
    tags:
      - tags/foo
      - tags/bar
    parent: identifier/of/an/integration-strategy
    mapped-here:
      - identifier/of/a/requirement
      - identifier/of/another/requirement

Work Items (kind: work-item, work, w):

  Used to specify work items required to implement/realise components,
  interfaces, tests etc., all in order to satisfy the system
  requirements.

  Supported keys:

    - title       (optional)
    - description (optional)
    - tags        (optional)
    - parents     (optional)
    - mapped-here (optional)

  Example:

    kind: work-item
    title: Any string
    description: A string in Markdown format.
    tags:
      - tags/foo
      - tags/bar
    parents:
      - identifier/of/an/component
      - identifier/of/a/component
      - identifier/of/an/interface
      - identifier/of/an/integration-strategy
      - identifier/of/a/verification-criterion
    mapped-here:
      - identifier/of/a/requirement
      - identifier/of/another/requirement

Tags (kind: tag, t)

  Used to provide generic tagging of other nodes in the Mustard.

  Supported keys:

    - title       (optional)
    - description (optional)

  Example:

    kind: tag
    title: "Attention: Architect"
    description: |
      The architect needs to think here, it's not ready.


3. Creating UML diagrams
------------------------

All elements in a Mustard repository can include UML diagrams in their
`description` field. Mustard is using PlantUML to parse the descriptions
of these diagrams and generate images that can be embedded in the web
interface or printed output.

### Defining a UML diagram in an element

Descriptions of Mustard elements are Markdown. Mustard, however, extends
the Markdown format by UML blocks opened with `@startuml` and closed with
`@enduml`. The content inside these blocks has to be PlantUML syntax.

An example interface with a simple sequence diagram could look as
follows:

    kind: interface
    title: Public service interface
    description: |
      The public interface of the `Foo` service.

      @startuml
      Client -> Service : subscribe()
      Service -> Client : subscribed()
      @enduml

### The PlantUML syntax

For the syntax and supported variants of UML diagrams, please refer to
the PlantUML website, which provides an extensive list of examples:

  http://plantuml.sourceforge.net/


4. Installing Mustard
---------------------

### Dependencies

In order to use Mustard, you'll need the following components:

  * Python >= 2.6
  * PyYAML
  * python-markdown
  * python-bottle
  * pygit2 (and libgit2)
  * cliapp

Most of the dependencies should be available in your distro, apart from
libgit2 and pygit2. The section below explains how to install these two
easily.

### Installing pygit2

If you lack pygit2 in your distribution, the safest way to get it is to
prepare a statically built libgit2 in a temporary installation location
and then link pygit2 against that.  Since libgit2 is not API/ABI stable
yet, this will innoculate you against others installing different
versions of libgit2 at other times.  It won't save you from incompatible
pygit2 installs, but you can fiddle with python paths if you care about
that.

To build libgit2 statically and pygit2 with that, do the following:

    $ mkdir pygit-building
    $ cd pygit-building
    $ git clone git://github.com/libgit2/libgit2.git
    $ git clone git://github.com/libgit2/pygit2.git
    $ cd libgit2
    $ git checkout v0.16.0-1553-g5a36f12
    $ mkdir build
    $ cd build
    $ cmake -DBUILD_SHARED_LIBS:BOOLEAN=OFF \
        -DCMAKE_INSTALL_PREFIX=$(pwd)/install ..
    $ make
    $ make install DESTDIR=""
    $ cd ../../pygit2
    $ git checkout v0.17.3-51-g81078e2
    $ LIBGIT2="$(pwd)/../libgit2/build/install" LIBGIT2="$(pwd)/../libgit2/build/install"  python setup.py build
    $ python setup.py install --user

This will install pygit2 into $HOME/.local -- obviously you can tweak the
`setup.py` invocations if you wish to alter where it installs to.

### Installing Mustard itself

Mustard cannot currently be installed into the system. It can, however,
be run directly from the source directory:

    ./mustard-render -b -r -j /path/to/plantuml.jar \
      -p /path/to/mustard/to/render

The usual way to run it is to clone the source code repository
somehwere and then integrate it with Apache or any WSGI-compatible
web server. See the following section for more details on how to
deploy Mustard using Apache.


5. Deploying Mustard using Apache2
----------------------------------

Mustard can be set up as an Apache site easily using mod_wsgi. It ships
an `adapter.wsgi` file that can be set up to handle HTTP requests as
follows:

  <VirtualHost *:80>
      ServerName someserver.org
      ServerAdmin root
      DocumentRoot /var/www/someserver.org

      WSGIPassAuthorization On
      WSGIDaemonProcess mustard user=www-data group=www-data \
        processes=1 threads=5
      WSGIProcessGroup mustard
      WSGIScriptAlias / /var/www/someserver.com/adapter.wsgi
      WSGIApplicationGroup %{GLOBAL}

      <Directory /var/www/someserver.com>
        SetEnv MUSTARD_CONFIG_FILE /path/to/mustard.conf
        SetEnv MUSTARD_AUTH none
        SetEnv MUSTARD_SERVER_PATH /var/www/someserver.com/
        SetEnv MUSTARD_PROJECT_PATH /path/to/the/mustard-repo.git
        SetEnv MUSTARD_PLANTUML_JAR /path/to/plantuml.jar

        Order deny,allow
        Allow from all
      </Directory>
  </VirtualHost>

For the above to work, Mustard, or at least its `adapter.wsgi` must be
located in `/var/www/someserver.com`. The source tree with
`adapter.wsgi` may also be located somewhere outside `DocumentRoot`.


6. Hacking Mustard
------------------

To hack on mustard and have your changed immediately testable in a web
browser, you can use

    ./mustard-render -b -r -j /path/to/plantuml.jar \
      -p /path/to/mustard/to/render

Replacing /path/to/plantuml.jar and /path/to/mustard/to/render as
appropriate

This method should NOT be used for deployment.

You will need to install cliapp to use the commandline tooling.
See http://liw.fi/cliapp/.


7. Contributing
---------------

Mustard is a Codethink Labs project. As such, its development takes
place within the Codethink Labs project on GitHub:

  http://github.com/CodethinkLabs/mustard

Anyone interested in improving Mustard is welcome to clone the project
repository and send pull requests.


8. Copyright & License
----------------------

Copyright (C) 2012-2013 Codethink Ltd.

Mustard is licensed under the GNU Affero General Public License
Version 3, (AGPLv3). The full text of the license can be found
in the COPYING file distributed along with this README.

Mustard ships a copy of jQuery in views/public/, which is licensed
under the MIT license (see COPYING.jquery for more information about
the license).
