================================
CLI Restricted Endpoint Examples
================================

The DataBiosphere CLI provides several ways for users of the data store to access and download data sets from the
data store. This page covers how to access the data store using the ``dbio`` command line utility.

The CLI calls listed here are restricted to those with upload or ingest permissions.

In the document that follows, *privileged user* refers to a user with proper credentials and
permission to upload/ingest data into the DSS.

*NOTE:* The Data Biosphere CLI utility is compatible with Python 3.5+.


``dbio delete-bundle``
----------------------

Deletes an existing bundle given a UUID, version, and replica.

Example call to ``dbio delete-bundle``:

.. literalinclude:: ../../test/tutorial/scripts/cli/delete_bundle_cli.sh


``dbio put-bundle``
-------------------

Creates a bundle. A bundle can contain multiple files of arbitrary type.

Inputs:

* ``uuid`` - a unique, user-created UUID.

* ``creator-uid`` - a unique user ID (uid) for the bundle creator uid. This accepts integer values.

* ``version`` - a unique, user-created version number. Use the ``create_verson()`` API function to generate a ``DSS_VERSION``.

* ``replica`` - which replica to use (corresponds to cloud providers; choices: ``aws`` or ``gcp``)

* ``files`` - a valid list of file objects, separated by commas (e.g., ``[{<first_file>}, {<second_file>}, ...  ]``). Each file object must include the following details:
    * Valid UUID of the file
    * Valid version number of the file
    * Name of the file
    * Boolean value - is this file indexed

Example call to ``dbio put-bundle``:

.. literalinclude:: ../../test/tutorial/scripts/cli/put_bundle_cli.sh

``dbio patch-bundle``
---------------------

Allows user to pass in an optional list of files to add or remove from an exisiting bundle. 

``add_files``/``remove_files`` follow this format:
::

    [
      {
        "path": "string",
        "type": "string",
        "uuid": "string",
        "version": "string"
      }
    ]

Example call to ``dbio patch-bundle``:

.. literalinclude:: ../../test/tutorial/scripts/cli/patch_bundle_cli.sh


``dbio put-file``
-----------------

Creates a new version of a file, given an existing UUID, version, creator uid, and source URL.

Example call to ``dbio put-file``:

.. literalinclude:: ../../test/tutorial/scripts/cli/put_file_cli.sh


``dbio get-collection(s), dbio put-collection, dbio patch-collection, dbio delete-collection``
----------------------------------------------------------------------------------------------

* ``dbio get-collection`` - Given a collection UUID, get the collection.

* ``dbio get-collections`` - Get a list of collections for a given user.

* ``dbio delete-collection`` - Given a collection UUID and replica, delete the collection from the replica.

* ``dbio put-collection`` - Create a collection.

* ``dbio patch-collection`` - Add or remove a given list of files from an existing collection.

To add or remove files with the CLI actions above, specify each file in the following format:
::

    [
      {
        "path": "string",
        "type": "string",
        "uuid": "string",
        "version": "string"
      }
    ]

Example CLI calls:

.. literalinclude:: ../../test/tutorial/scripts/cli/put_delete_get_patch_collection_cli.sh

``dbio upload``
---------------

Uploads a directory of files from the local filesystem and creates a bundle containing the uploaded files.

Example call to ``dbio upload``:

.. literalinclude:: ../../test/tutorial/scripts/cli/upload_cli.sh
