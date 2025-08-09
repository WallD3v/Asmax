Asmax
========
.. epigraph::

  my telegram: @wdp_closed

Description
-----------------
**asmax** is a framework for Max Messanger UserAPI written in Python 3.8+ using asyncio and websockets.

Features
-----------------
This project replicates the core functionalities of Max Messanger, including:

*   **Authorization**: You can log in to your account using the sms code and use it.
*   **Messages**: Receive and reply to messages.

This project provides an opportunity to create userbots and helps with automation.

Installing
-----------------
.. code-block:: shell

    pip install asmax

Currently, the module is not available on pypi, so use the alternative installation method

Alt method
-----------------
.. code-block:: shell

    git clone https://github.com/WallD3v/Asmax
    mv Asmax-main/Asmax ./
    rm -r Asmax-main


Creating client
-----------------
.. code-block:: python

    from Asmax.Max.Client import MaxClient

    max_client = MaxClient("session_name")
    max_client.start()

Next steps
----------

Do you like how Asmax looks? Check out `Read The Docs`_ for a more
in-depth explanation, with examples, troubleshooting issues, and more
useful information.

.. _Read The Docs: https://example.com
