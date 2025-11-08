Usage Guide
===========

This guide will help you get started with margie and understand how to use it for genome annotation.

Installation
------------

Installing Pixi
~~~~~~~~~~~~~~~

First, install pixi (a fast package manager for conda environments):

**macOS/Linux:**

.. code-block:: bash

   curl -fsSL https://pixi.sh/install.sh | bash

**Or with Homebrew on macOS:**

.. code-block:: bash

   brew install pixi

**Windows:**

.. code-block:: powershell

   iwr -useb https://pixi.sh/install.ps1 | iex

Setting Up the Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Clone this repository and navigate to the project directory

2. Clone the `GeneralTools repository <https://github.com/Diet-Microbiome-Interactions-Lab/GeneralTools>`_:

   * Make sure the ``margie/`` folder is in the same parent folder as ``GeneralTools/``
   * i.e., ``/path/to/folders/margie`` and ``/path/to/folders/GeneralTools``
   * This is important because in our ``pixi.toml``, one of our dependencies is the development/editable version of GeneralTools

3. Install dependencies with pixi:

   .. code-block:: bash

      pixi install

4. Activate the environment:

   .. code-block:: bash

      pixi shell

Testing the Installation
~~~~~~~~~~~~~~~~~~~~~~~~~

Test to determine bioinformatics_tools imports properly:

.. code-block:: bash

   # Basic usage
   python tests/test.py
   # Should see output: ✅ Tests passed successfully!

Running margie
--------------

Basic Usage
~~~~~~~~~~~

.. code-block:: bash

   margie annotate-all -i raw-fastas/*.fasta -o annotation-output/  # Raw output
   margie annotate --sources kegg,tigr,pfam -i raw-fastas/*.fasta -o annotation-output/
   margie report -i annotation-output/ -o report-output/
   margie interactive -i report-output -p 8000  # Report you can explore in browser
   # Should see output: ✅ Margie pipeline completed successfully!
   # This will also create: margie-tools/output/from-default2/example.db & example2.db

Advanced Usage
~~~~~~~~~~~~~~

.. note::
   Additional usage examples and advanced features will be documented here as the tool develops.

Input Files
-----------

Below is a list of the following formats margie accepts

**fasta**

- They must start with *>* and spaces/other characters in the header don't matter

.. note::
   Currently, fastq files are not accepted until we are able to provide the neccessary assembly steps.

Output Files
------------

The pipeline generates:

- SQLite database with annotation results
- Additional output files in the specified ``output`` directory

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Issue: Pixi installation fails**

- Ensure you have the necessary permissions to install software
- Try using sudo (Linux/macOS) or running as administrator (Windows)

**Issue: GeneralTools not found**

- Verify that GeneralTools is cloned in the correct location (same parent directory as margie)
- Check that the path in ``pixi.toml`` is correct. This should only be for development purposes

**Issue: Import errors**

- Make sure you've run ``pixi install`` successfully
- Activate the environment with ``pixi shell``
- Verify that all dependencies were installed

Getting Help
~~~~~~~~~~~~

If you encounter issues not covered here:

1. Check the :doc:`technical` documentation
2. Review the project's GitHub issues
3. Contact the development team
