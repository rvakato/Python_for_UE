import unreal

# Define paths based on the new folder structure
source_instance_path = '/Game/Stage/Materials/Bricks/Bricks_TaylorMaxwell_AllWhiteMirato/Bricks_Base.Bricks_Base'  # Path to the source material instance
output_instance_folder = '/Game/Stage/Materials/Bricks/Bricks_TaylorMaxwell_AllWhiteMirato/'  # Folder to save the duplicated instances
texture_folder = '/Game/Stage/Materials/Bricks/Bricks_TaylorMaxwell_AllWhiteMirato/'  # Folder containing the textures
texture_name_prefix = 'Bricks_TaylorMaxwell_AllWhiteMirato'  # Prefix for textures

# Updated parameter names for Virtual Textures
parameters = {
    "BaseColor": "Diffuse Map VT",
    "Normal": "Normal Map VT",
    "Roughness": "Roughness Map VT"
}

# Load the source material instance
source_instance = unreal.EditorAssetLibrary.load_asset(source_instance_path)
if not source_instance:
    print(f"Source material instance not found at {source_instance_path}")
    quit()

# Duplicate the material instance and apply textures
for i in range(1, 31):  # Loop through 1 to 30
    # Define the new instance name and path
    new_instance_name = f"MI_{texture_name_prefix}{i}"
    new_instance_path = f"{output_instance_folder}{new_instance_name}"

    # Duplicate the material instance
    duplicated_instance = unreal.EditorAssetLibrary.duplicate_asset(source_instance_path, new_instance_path)
    if not duplicated_instance:
        print(f"Failed to duplicate material instance: {new_instance_name}")
        continue

    print(f"Duplicated material instance: {new_instance_path}")

    # Load the duplicated material instance
    material_instance = unreal.EditorAssetLibrary.load_asset(new_instance_path)
    if not material_instance:
        print(f"Failed to load duplicated material instance: {new_instance_name}")
        continue

    # Apply textures to the duplicated material instance
    base_color_texture_path = f"{texture_folder}{texture_name_prefix}_{i}_color"
    normal_texture_path = f"{texture_folder}{texture_name_prefix}_{i}_normal"
    roughness_texture_path = f"{texture_folder}{texture_name_prefix}_{i}_roughness"

    # Load the virtual textures
    base_color_texture = unreal.EditorAssetLibrary.load_asset(base_color_texture_path)
    normal_texture = unreal.EditorAssetLibrary.load_asset(normal_texture_path)
    roughness_texture = unreal.EditorAssetLibrary.load_asset(roughness_texture_path)

    if not base_color_texture or not normal_texture or not roughness_texture:
        print(f"Missing texture(s) for Material Instance {i}:")
        print(f"  BaseColor: {base_color_texture_path}")
        print(f"  Normal: {normal_texture_path}")
        print(f"  Roughness: {roughness_texture_path}")
        continue

    # Assign the virtual textures
    unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(
        material_instance, parameters["BaseColor"], base_color_texture
    )
    unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(
        material_instance, parameters["Normal"], normal_texture
    )
    unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(
        material_instance, parameters["Roughness"], roughness_texture
    )

    # Save the updated material instance
    unreal.EditorAssetLibrary.save_asset(new_instance_path)
    print(f"Updated and saved material instance: {new_instance_path}")
