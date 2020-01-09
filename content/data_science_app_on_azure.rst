Notes on setting up a Data Science app on Azure
###############################################
:date: 2020-01-09 08:30
:author: Chris Stucchio
:tags: data science, programming, azure

I have recently been working on setting up a trading strategy and running it in the cloud. Although I haven't used Azure before, I wanted to try it out - some of the data science features that Microsoft advertises look pretty nice. This post is not of general interest, and most readers should stop reading now. This is merely my working notes - placed here to help people who are googling for it - and only useful to you if you want to run an app on `Azure Functions <https://azure.microsoft.com/en-us/services/functions/>`_ and don't yet know how.

Structure of the strategy
=========================

The trading strategy I'm using is pretty straightforward. To begin with, I periodically query the REST API of a certain marketplace. The API returns a list of trading opportunities - securities :math:`S_i, i=1 \ldots N` and their prices :math:`p_i`, along with characteristics :math:`\vec{x}^i` of the security.

As a concrete example of systems like this, think of trading cryptocurrencies on an exchange (e.g. `Coinbase Exchange API <https://developers.coinbase.com/docs/exchange/>`_).

The price in question is an implicit market-based assessment of risk - i.e. there is a function :math:`r(p_i)` which implicitly assigns each price to a corresponding risk level. Higher prices imply more risk.

My mental model for the market is as follows. The market is a machine learning model :math:`L(\vec{x}_i)` which predicts risk, and then chooses a corresponding price for that risk. I do not know this model, however a very simple application of isotonic regression has enabled me to determine that the market prices are highly predictive (`ROC_AUC <https://en.wikipedia.org/wiki/Receiver_operating_characteristic>`_ is in the 70-80% ballpark).

I have additional data :math:`\vec{y}^i` that I do not believe the market incorporates. So the way I'm attacking the problem is the following:

1. Query the REST API to get the standard market data, :math:`(p_i, \vec{x}^i)`.
2. Compute an inner join between my data set to enrich the data set, :math:`(p_i, \vec{x}^i) \mapsto (p_i, \vec{x}^i, \vec{y}^i)`.
3. Run a machine learning model on the enriched data set and generate improved risk scores :math:`q(p_i, \vec{x}^i, \vec{y}^i)`. In backtesting, these improved risk scores are more accurate than the risk scores :math:`r(p_i)` generated from prices alone.
4. Purchase securities which have :math:`q(p_i, \vec{x}^i, \vec{y}^i) - r(p_i) < -T` for some threshold :math:`T`. In simple terms, I'm purchasing securities when my assessment of their risk is significantly lower than the market's assessment of their risk.

The ML model used to predict prices is a relatively standard `sklearn.pipeline.Pipeline <https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html>`_ - it's trained offline, saved as a pickle, and loaded periodically to execute step (4) above.

Azure Functions seemed like a simple and low cost way to run this strategy - no server deployment to worry about.

Setting up Azure Functions
==========================

The general structure of my application is as follows::

  requirements.txt
  trading_library/data/... # Data access methods
  trading_library/models/... # Code to actually train/run the ML models
  trading_library/config/__init__.py
  trading_library/config/_fileconfig.py  # Config when running things locally. This has secrets!
  trading_library/jobs/...  # Functions that do things

  az_func/host.json
  az_func/local.settings.json
  az_func/get_data/function.json  # Each subfolder corresponds to a single Azure function.
  az_func/get_data/__init__.py
  az_func/...other_job.../{function.json, __init__.py}

  deploy_az_functions.ps1

The first directory, :code:`trading_library` is just ordinary python code. It's a library with assorted functions that are helpful for running my trading strategy. Some are intended to run in production, others I use locally when doing analysis and development. This directory is at the top level because I frequently run a Jupyter notebook here for development.

The directory :code:`az_func` corresponds to the Azure Functions application. It was created as follows::

  PS ..> func init az_func --python

The notation :code:`PS ..>` means that this line represents a PowerShell command. Tangentially, as a long time Linux command line user, I must say that PowerShell is the most exciting innovation in command line UI that I've seen since zsh. If you haven't tried it yet, go check it out.

This is the command to initialize an Azure Functions project as described in `Microsoft's docs <https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python>`_. Each subfolder in :code:`az_func` corresponds to a single function - think of each of these as a cron job. (In other setups, they can correspond to an HTTP endpoint or something similar.)

The contents are quite simple. Here is :code:`function.json`::

  {
    "scriptFile": "__init__.py",
    "bindings": [
        {
            "name": "my_function_argument",
            "type": "timerTrigger",
            "direction": "in",
            "schedule": "3 25 15 * * *",
            "runOnStartup": false
        }
    ]
  }

The :code:`schedule` parameter is in ordinary 6 option CRON format - the example above runs on the 3'rd second of the 25'th minute of the 15'th hour of every day.

The python code in :code:`__init__.py` is also quite simple::

  import logging
  import azure.functions as azfunc
  from __app__.trading_library.jobs import get_the_data

  def main(my_function_argument):
      logging.info('Running get_data at time %s.', timer)
      get_the_data()  # Real work happens here
      logging.info("Finished get_data.")

Note how the parameter :code:`"name": "my_function_argument"` in :code:`function_json` corresponds to the argument :code:`main(my_function_argument)` in python itself. The function won't work if you don't get this right.

As far as local code structure, that's basically everything you need to create an Azure function.

Deploying it
------------

To deploy, one must first create the Azure Functions app on Azure. Microsoft's `instructions <https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python>`_ are quite good so I will not repeat them here.

Here, I'll focus on the practicalities of this - specifically, the contents of my :code:`deploy_az_functions.ps1` Powershell script. To start with, Azure Functions requires us to make the :code:`trading_library` path accessible inside the :code:`az_func` folder::

  $shared_code_path = "az_func\trading_library"

  if (Test-Path $shared_code_path){
      Remove-Item -Recurse -Force $shared_code_path
  }

It is also useful to save space by not uploading assorted crud files::

  # Cleanup crud
  Get-ChildItem .\trading_library\ -recurse -include __pycache__ | Remove-Item -recurse
  Get-ChildItem .\trading_library\ -recurse -include *.pyc | Remove-Item
  Get-ChildItem .\trading_library\ -recurse -include *.py~ | Remove-Item

Finally, we copy the library folder into :code:`az_func`::

  # Copy shared code
  Copy-Item -Recurse .\trading_library\ $shared_code_path\

Then we remove our secret-filled local use only config file ::

  Remove-Item .\az_func\trading_library\config\_fileconfig.py

Finally we deploy the Azure Functions app::

  # Publish the function
  cd az_func
  func azure functionapp publish trading_library
  cd ..

  if (Test-Path $shared_code_path){
      Remove-Item -Recurse -Force $shared_code_path
  }

The job will now be running daily on a timer.

Handling Secrets
----------------

The more difficult piece for me was the handling of secrets. Azure has a service called `Key Vault <https://azure.microsoft.com/en-us/services/key-vault/>`_ which provides encrypted storage of application secrets. Keyvault has two different modes of operation:

1. Exposing values from keyvault to the application as an environment variable. This is very easy to do, but it requires explicitly enumerating every secret needed.
2. Programmatically accessing keyvault with the python library. This requires python having access to keyvault credentials, which must somehow be safely transmitted to python itself.

I chose a hybrid approach - I store the keyvault credentials *in keyvault itself* and expose them via the method in (1). Then in Python I use them to access the other secrets programmatically.

Setting up keyvault and a client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a keyvault. This step is done only once, and should not be part of the powershell script::

  PS..> az keyvault create -n tradinglibrarykeyvault -g $resourceGroup

Next I created a *service principal*::

  $service_principal = az ad sp create-for-rbac -n "http://mySP" --sdk-auth | ConvertFrom-Json

The :code:`$service_principal` variable will have the fields :code:`clientId` and :code:`clientSecret` - we must put these into keyvault::

  PS..> az keyvault secret set -n "keyvault-client-id" --vault-name $keyvaultname --value $($service_principal.clientId)
  PS..> az keyvault secret set -n "keyvault-client-secret" --vault-name $keyvaultname --value $($service_principal.clientSecret)

This is all done *once*, at the command line.

Giving the application access to keyvault credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We first create a managed identity. This operation is idempotent and goes in the same powershell script I use to deploy::

  # Grant keyvault access
  $kv_identity = az functionapp identity assign -n trading_library -g trading_library_resource_group | ConvertFrom-Json # First create identity

After the identity has been created, repeated calls to create it will simply return the existing one. We must also put these variables into keyvault::

  az keyvault secret set -n "keyvault-tenant-id" --vault-name $keyvaultname --value $kv_identity.tenantId
  az keyvault secret set -n "keyvault-name" --vault-name $keyvaultname --value $keyvaultname

Next we must grant that identity permission to access keyvault::

  az keyvault set-policy -n trading_library_keyvault -g $resourceGroup --object-id "$($kv_identity.principalId)" --secret-permissions get  # Assign the policy

Finally, I put the keyvault access parameters into the keyvault itself::

  foreach ($keyname in "keyvault-tenant-id","keyvault-name","keyvault-client-id","keyvault-client-secret") {  # Then provide the keyvault variables.
      $secretId = az keyvault secret show -n $keyname --vault-name lendingclubstratkeyvault --query "id"
      $keyname_var= $keyname.replace('-', '_')
      az functionapp config appsettings set -n lendingclubstrat -g lendingclubstrat --settings "$keyname_var=@Microsoft.KeyVault(SecretUri=$secretId^^)"
  }

The last line :code:`az functionapp config appsettings...` is what provides access to the keyvault variables as environment variables.

Inside python, you can now access the :code:`clientId` via :code:`os.environ['keyvault_client_id']`.

Programmatic access
~~~~~~~~~~~~~~~~~~~

I manage my configuration via the `tr11/python-configuration <https://github.com/tr11/python-configuration>`_ library. When doing development on my local machine, my configuration is stored in a simple python dictionary.

The :code:`configuration` library does not have an Azure Keyvault backend native. For this reason, I wrote `my own backend <https://gist.github.com/stucchio/8a0c6c57cea7452eed8e7001877ae2fd>`_ for it. **Update: The author of python-configuration was kind enough to merge my backend into master. Use that one.**

All my code access configuration as follows::

  from trading_library.config import cfg

  do_a_thing(cfg['trading_api_key'])

The file :code:`trading_library/config/__init__.py` looks like the following::

  import config
  import os

  __all__=['cfg']

  try:
      from ._fileconfig import _fileconfig
      filecfg = config.config_from_dict(_fileconfig)
  except ImportError:
      filecfg = config.config_from_dict({})

  if 'keyvault_name' in os.environ:  # On azure, we will have access to keyvault.
      from config.contrib.azure import AzureKeyVaultConfiguration

      azure_cfg = AzureKeyVaultConfiguration(
          az_client_id=os.environ['keyvault_client_id'],
          az_client_secret=os.environ['keyvault_client_secret'],
          az_tenant_id=os.environ['keyvault_tenant_id'],
          az_vault_name=os.environ['keyvault_name']
          )
      cfg = config.ConfigurationSet(filecfg, azure_cfg)  # Config looks to
  else:
      cfg = filecfg

Thus, in local development, secrets are read from the :code:`_fileconfig` variable. In production they come from Key Vault.

Other problems I ran into
=========================

Handling pickled models - :code:`No module named trading_library.models.alpha_model'`
-------------------------------------------------------------------------------------


My workflow is the following. I do model training on my laptop - a beefy 64GB machine. It takes over an hour to run there. Then I save a pickled version of the model to Azure Blobstore.

However, model prediction runs in Azure Functions. Inside Azure I download the blob containing the model and unpickle it. Unfortunately, my first attempt at doing this didn't work - I ran into the error :code:`ModuleNotFoundError: No module named 'trading_library.models.alpha_model'`.

The reason for this is that inside Azure Functions, the module name isn't :code:`trading_library`, it's :code:`__app__.trading_library`. This breaks pickle.

To resolve this, we need to hack into Python's module system. In Python, a module is an ordinary object. The first time a module is imported it gets *loaded*; after this it is placed in the :code:`sys.modules` hash table. If you import it again, it will simply return the object from :code:`sys.modules`. Simple code example::

  import sys
  import logging
  sys.modules['my_copy_of_logging'] = logging
  import my_copy_of_logging

  assert (my_copy_of_logging == logging)  # returns True

We have essentially taken an existing module and tricked python into thinking it has a different module name.

We can use the same hack to resolve the issue with pickles. We put this at the top of our Azure function's :code:`__init__.py`::

  import __app__.trading_library
  import sys
  sys.modules['trading_library'] = __app__.trading_library

After this is done the pickle can be loaded normally.

Resetting API keys
------------------

Each Function App creates a corresponding Azure Storage instance. I am also using this storage instance to store data used by the app, as opposed to merely configuration of the app.

However, at some point I decided to reset the storage keys. When I did this my function app stopped working. I couldn't even deploy a new version of the app, and ran into this error::

  Uploading built content /home/site/deployments/functionappartifact.squashfs -> https://trading_strategy.blob.core.windows.net/scm-releases/scm-latest-trading_strategy.zip?...
  Remote build failed!

The app didn't run either. The culprit is that Azure Functions was unable to access storage.

This can be fixed by copying the new :code:`Connection String` (from the Storage instance) into the :code:`AzureWebJobsStorage` field in the "Application Settings" part of Azure Functions.
