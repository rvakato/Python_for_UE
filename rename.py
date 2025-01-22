import unreal

# Source path in your Unreal Engine project
folder_name = "Brick_Ibstock_Thorn_Black"
source_instance_path = f"/Game/Stage/Materials/Brick/{folder_name}/"

# Asset Tools helper
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()


# Get the material instances in the specified directory
def get_assets_in_path(path):
    return unreal.EditorAssetLibrary.list_assets(path, recursive=False, include_folder=False)


# Pad numbers in material instance names
def rename_material_instances(path):
    assets = get_assets_in_path(path)
    for asset in assets:
        # Only process material instances
        if f"MI_{folder_name}_" in asset:
            # Extract the current name
            asset_name = asset.split("/")[-1]
            parts = asset_name.split("_")
            number_part = parts[-1]

            # Check if the last part of the name is a number between 1 and 9
            if number_part.isdigit() and 1 <= int(number_part) <= 9:
                # Pad the number with a leading zero
                new_number = f"{int(number_part):02d}"
                new_name = asset_name.replace(f"_{number_part}", f"_{new_number}")

                # Rename the asset
                new_asset_path = f"{path}{new_name}"
                unreal.EditorAssetLibrary.rename_asset(asset, new_asset_path)
                print(f"Renamed: {asset} -> {new_asset_path}")


# Execute the rename process
rename_material_instances(source_instance_path)
