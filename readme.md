# DIP mungers!

We created these at SFU Archives in order to support ad-hoc DIP upload and metadata updates from Archivematica to AtoM at points in our workflow not supported by the existing [https://www.archivematica.org/en/docs/archivematica-1.10/user-manual/access/access/#upload-atom](AtoM DIP upload functionality).

If you plan to use these scripts, I encourage you to compile them for your local environment with `pyinstaller`, so that their dependencies are packaged in and they can be run like command line programs rather than Python scripts. This needs to be done separately for Windows, Mac, and Linux environments. Many of the server *names* are currently hardcoded to SFU Archives' environment but the paths themselves are all as generic as possible.

## Retrieval

There are three scripts in this repository. `dip-retrieve` is used to fetch DIPs that have been stored by Archivematica as a first step; this workflow always assumes that you are storing your DIPs Archivematica-side. It also connects over ssh, and therefore requires that you have a bash-enabled user account on the server(s) running Archivematica, that passwordless (key-based) ssh authentication is in place, that this user is a *member* of the Archivematica group on the server, and that globstars are enabled in your .bashrc for advanced path comprehensions. You can make these last two changes to your server environment by logging in and running:

```
echo 'shopt -s globstar' >> ~/.bashrc
usermod -a -G archivematica $(whoami)
```

The script is configured to check in multiple places for DIPs, assuming a relatively standard Archivematica configuration with a single storage service and one or more pipelines each on their own VPS. It takes three arguments: the name of the Archivematica pipeline server associated with the DIP, your username on that server, and the transfer name, e.g. `dip-retrieve larch garnett RD_2017-08-04_test1`. It will look in multiple places for DIPs, on both the storage service and the pipeline server, and will check default directories from both past and present releases of Archivematica. If a DIP is found, it will be replicated down to your desktop, in a directory named for the transfer, and a CSV file will be created in that directory with two columns. The first column will be a list of filenames from within the DIP; the second will be labeled 'slug' and be empty.


## Upload

From here, you can either upload an entire DIP, or -- in cases where you do not want to make objects available via AtoM but wish to provide metadata stubs for users browsing your repository -- just its metadata. In either case, you'll want to manually populate the 'slug' column of the spreadsheet consistent with [https://www.accesstomemory.org/en/docs/2.5/admin-manual/maintenance/cli-tools/#manually-upload-archivematica-dip-objects](the AtoM documentation for manually uploading DIP objects). The dip-upload script otherwise follows this workflow exactly by performing the scp transfer step as the `nginx` user on the server for you and cleaning up afterwards; you'll need to be able to log in as the nginx user on the AtoM server (by again setting up an ssh key), and will want to run it as `dip-upload atomservername /path/to/dip/on/your/desktop`.

The dip-metadata script uses the same syntax and the same input but instead of adding entire objects to AtoM, it only sends new metadata to AtoM's API based on the METS files packaged in with the DIP, using Artefactual's (agentarchives)[https://github.com/artefactual-labs/agentarchives] API library. Rather than configuring ssh authentication, it requires you to (configure an AtoM API key)[https://www.accesstomemory.org/en/docs/2.5/dev-manual/api/api-intro/#authentication] and store it locally in `~/.atomapi`. It currently supports adding filenames, filesizes, object types, and UUIDs for every child of a DIP object to a parent record in AtoM; no other metadata is supported due to API limitations.