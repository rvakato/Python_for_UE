import unreal

# Define paths
master_material_path = "/Game/Texture/M_BrickMaster"  # Path to the master material
output_instance_folder = "/Game/Stage/Materials/Brick/Brick_Test/"  # Folder to save material instances
texture_folder = "/Game/Stage/Materials/Brick/Brick_Test/"  # Folder containing textures

# Load the master material
master_material = unreal.EditorAssetLibrary.load_asset(master_material_path)
if not master_material:
    print(f"Master material not found at {master_material_path}")
    quit()

# Generate 20 material instance names
instance_names = [f"MI_Brick_Thorn_Black_{i}" for i in range(1, 21)]

# Define dummy texture names (modify to match actual textures in your project)
texture_sets = {
    f"MI_Brick_Test_{i}": {
        "BaseColor": f"{texture_folder}Brick_Ibstock_Thorn_Black_{i}_color",
        "Normal": f"{texture_folder}Brick_Ibstock_Thorn_Black_{i}_normal",
        "Roughness": f"{texture_folder}Brick_Ibstock_Thorn_Black_{i}_roughness",
    }
    for i in range(1, 21)
}

# Create material instances
for name in instance_names:
    instance_path = f"{output_instance_folder}{name}"
    instance = unreal.MaterialEditingLibrary.create_material_instance(master_material, instance_path)

    # Get texture set for the current instance
    texture_key = name.split("_", 1)[-1]  # Extract "Thorn_Black_X"
    textures = texture_sets.get(texture_key)

    # Assign textures if available
    if textures:
        base_color = unreal.EditorAssetLibrary.load_asset(textures["BaseColor"])
        normal = unreal.EditorAssetLibrary.load_asset(textures["Normal"])
        roughness = unreal.EditorAssetLibrary.load_asset(textures["Roughness"])

        if base_color:
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(instance, "BaseColor",
                                                                                        base_color)
        if normal:
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(instance, "Normal", normal)
        if roughness:
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(instance, "Roughness",
                                                                                        roughness)

    # Save the instance
    unreal.EditorAssetLibrary.save_asset(instance_path)
    print(f"Created and saved material instance: {instance_path}")
