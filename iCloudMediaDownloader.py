import os
from pyicloud import PyiCloudService
from tqdm import tqdm


def icloud_download():
    # Prompt for iCloud account credentials
    APPLE_ID = input("Enter your Apple ID: ")
    PASSWORD = input("Enter your password: ")

    # Local directory to download photos to
    LOCAL_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "Phone Media")

    if not os.path.exists(LOCAL_DIR):
        os.makedirs(LOCAL_DIR)

    # Connect to iCloud
    try:
        api = PyiCloudService(APPLE_ID, PASSWORD)
    except Exception as e:
        print(f"Error connecting to iCloud: {e}")
        exit()

    # Prompt for two-factor authentication code, if necessary
    if api.requires_2fa:
        code = input("Enter two-factor authentication code: ")
        try:
            api.validate_2fa_code(code)
        except Exception as e:
            print(f"Error: {e}")
            exit()
    elif api.requires_2sa:
        code = input("Enter two-step authentication code: ")
        try:
            api.validate_2sa_code(code)
        except Exception as e:
            print(f"Error: {e}")
            exit()
    else:
        print("Successfully logged in to iCloud.")

    # Get all photos and videos
    try:
        photos = api.photos.all
    except Exception as e:
        print(f"Could not retrieve media from the iCloud services.")
        print(e)
        exit()

    # Download each photo and video to the local directory
    errors = []
    with tqdm(total=len(photos)) as pbar:
        for photo in photos:
            filename = photo.filename
            filepath = os.path.join(LOCAL_DIR, filename)
            if os.path.exists(filepath):
                pbar.write(f"File {filename} already exists, skipping download.")
                continue
            try:
                with open(filepath, "wb") as f:
                    for chunk in photo.download().iter_content(chunk_size=1024):
                        f.write(chunk)
                pbar.update(1)
            except Exception as e:
                errors.append(filename)
                pbar.write(f"Error: Failed to download {filename}")
                pbar.write(str(e))
            # Delete photos from iCloud
            try:
                photo.delete()
            except Exception as e:
                pbar.write(f"Error: Failed to delete {filename} from iCloud.")
                pbar.write(str(e))

    if len(errors) > 0:
        pbar.write(f"{len(errors)} files failed to download:")
        for error in errors:
            pbar.write(error)
    else:
        pbar.write("All files downloaded successfully.")

    pbar.write("Done!")


if __name__ == "__main__":
    icloud_download()
