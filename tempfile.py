def save_to_lakehouse(file_content, lakehouse_path, file_path, extention):
    try:
        full_file_path = f"{lakehouse_path}/{file_path}"
        os.makedirs(os.path.dirname(lakehouse_path), exist_ok=True)
        with tempfile.NamedTemporaryFile(delete=False, suffix=extention) as temp_file:
            temp_path = temp_file.name
            temp_file.write(file_content)
        fs.cp(temp_path, full_file_path)
        os.remove(temp_path)    
        print(f"File saved to lakehouse: {full_file_path}")
        return True
    except Exception as e:
        print(f"Error saving file to lakehouse: {e}")
        return False

import os

log_path = "/home/trusted-service-user/.azcopy/87d79623-f1af-7c46-629e-4381e6ceb027.log"
if os.path.exists(log_path):
    with open(log_path, 'r') as log_file:
        print(log_file.read())
else:
    print("Log file not found.")

from notebookutils import mssparkutils
destination = "abfss://<workspace-id>@onelake.dfs.fabric.microsoft.com/<lakehouse-id>/Files/reference_codes/window_protection_covering_types_code/affd4711-1713-4afc-98f6-32870353b2fg/Ref_Window Protection Covering Types_v1.xlsx"
try:
    mssparkutils.fs.ls(os.path.dirname(destination))
    print("Directory exists and is accessible.")
except Exception as e:
    print(f"Error accessing directory: {e}")

file_path = "reference_codes/window_protection_covering_types_code/affd4711-1713-4afc-98f6-32870353b2fg/Ref_Window_Protection_Covering_Types_v1.xlsx"

import os

# After writing to temp file
with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
    temp_path = temp_file.name
    temp_file.write(file_content)
    print(f"Temporary file created at: {temp_path}")
    print(f"File exists: {os.path.exists(temp_path)}")
    print(f"File size: {os.path.getsize(temp_path)} bytes")

!azcopy copy '/tmp/tmpe282k15r.xlsx' 'https://onelake.blob.fabric.microsoft.com/a72bf9c2-7aab-42ab-b2c7-42833f3ca89e/b66e51f1-4687-4a21-ac17-9f609ec41cc2/Files/reference_codes/window_protection_covering_types_code/affd4711-1713-4afc-98f6-32870353b2fg/Ref_Window_Protection_Covering_Types_v1.xlsx' --trusted-microsoft-suffixes="*.pbidedicated.windows.net;*.pbidedicated.windows-int.net;*.fabric.microsoft.com" --skip-version-check

from notebookutils import mssparkutils

def save_to_lakehouse(file_content: Union[str, bytes], lakehouse_path: str, file_path: str, extension: str) -> bool:
    try:
        if not extension.startswith('.'):
            extension = f'.{extension}'
        full_file_path = os.path.join(lakehouse_path, file_path).replace('\\', '/')
        
        # Create directory structure in OneLake
        one_lake_dir = os.path.dirname(full_file_path)
        mssparkutils.fs.mkdirs(one_lake_dir)
        print(f"Created OneLake directory: {one_lake_dir}")

        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as temp_file:
            temp_path = temp_file.name
            if isinstance(file_content, str):
                temp_file.write(file_content.encode('utf-8'))
            else:
                temp_file.write(file_content)

        # Copy to lakehouse
        mssparkutils.fs.cp(temp_path, full_file_path)
        os.remove(temp_path)

        print(f"File saved to lakehouse: {full_file_path}")
        return True

    except Exception as e:
        print(f"Error saving file to lakehouse: {e}")
        # Check for azcopy log file
        import glob
        log_files = glob.glob("/home/trusted-service-user/.azcopy/*.log")
        if log_files:
            with open(log_files[-1], 'r') as log_file:
                print(f"azcopy log: {log_file.read()}")
        return False
    finally:
        if 'temp_path' in locals() and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass
