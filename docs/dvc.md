# Data Version Control (DVC)

 - Why is DVC useful in this context: tracks data well (also models)

## Initiating DVC
 - `dvc init`

## Setting up gdrive remote
 - Advantages to Google Drive
 - Set up a public DVC repository.
 - Adding the remote to the DVC repository (where is this seen?).
 - See [here](https://dvc.org/doc/user-guide/data-management/remote-storage/google-drive) for more information and 
   options.

### Steps

1. Go to [`https://drive.google.com/drive/home`](https://drive.google.com/drive/home).
2. Create a new directory using the `+ New` button.
3. Go to the drive and select the downward arrow, &#9660;, next to the folder name.
4. Select `Share` &#x2192; `Share`.
5. In the new window, make sure `General access` is selected as `Anyone with the link` and that role is set to `Viewer`.
6. Make a note of the _Folder ID_. This is usually available from the URL in the browser address bar.  For example, if
   if the URL is `https://drive.google.com/drive/folders/1ZduSGJSCuTF4WmhP1bGoXxSRmCQWnJvI`, then the ID is
   `1ZduSGJSCuTF4WmhP1bGoXxSRmCQWnJvI`.
7. In your repository, add the Google drive as the default remote using
   `dvc remote add --default gdrive gdrive://{folder_id}`, where `{folder_id}` is the ID obtained from step 6. The 
   first `gdrive` is an arbitrary name that can be changed if needed.
8. Use `dvc remote modify gdrive gdrive_acknowledge_abuse true`

You can see the details of this remote in the `.dvc/config` file within the repository.

## Adding tracked data
 - File or directory?

### Steps

From root of repo:
1. `dvc add ./path/to/data`