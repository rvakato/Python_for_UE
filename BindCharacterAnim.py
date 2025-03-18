import unreal

# Define the Level Sequence asset path
level_sequence_path = "/Game/Stage/Sequences/People/SEQ_AnimaPeople.SEQ_AnimaPeople"

# Load the Level Sequence
level_sequence = unreal.load_asset(level_sequence_path)
if not level_sequence:
    unreal.log_error(f"Failed to load Level Sequence: {level_sequence_path}")
    raise Exception("Level Sequence not found.")

# Get the Movie Scene from the Level Sequence
movie_scene = level_sequence.get_movie_scene()

# Get the world context
world = unreal.EditorLevelLibrary.get_editor_world()

# Get all skeletal mesh actors in the scene
all_actors = unreal.EditorLevelLibrary.get_all_level_actors()
skeletal_mesh_actors = [actor for actor in all_actors if isinstance(actor, unreal.SkeletalMeshActor)]

# Process each skeletal mesh actor
for skeletal_mesh_actor in skeletal_mesh_actors:
    actor_name = skeletal_mesh_actor.get_name()

    # Get the SkeletalMeshComponent inside the actor
    skeletal_mesh_component = skeletal_mesh_actor.get_component_by_class(unreal.SkeletalMeshComponent)

    if not skeletal_mesh_component:
        unreal.log_warning(f"❌ No SkeletalMeshComponent found for {actor_name}, skipping...")
        continue

    # Get the "Anim to Play" from SingleAnimationPlayData
    animation_data = skeletal_mesh_component.get_editor_property("animation_data")
    
    if not animation_data:
        unreal.log_warning(f"❌ No animation data found for {actor_name}, skipping...")
        continue

    anim_sequence = animation_data.get_editor_property("anim_to_play")

    if not anim_sequence:
        unreal.log_warning(f"❌ No 'Anim to Play' found for {actor_name}, skipping...")
        continue

    unreal.log(f"🎬 Found Anim to Play for {actor_name}: {anim_sequence.get_name()}")

    # Find or create a binding in the Level Sequence
    bindings = level_sequence.get_bindings()
    binding = None

    for poss in bindings:
        if poss.get_display_name() == actor_name:
            binding = poss
            break

    if not binding:
        binding = level_sequence.add_possessable(skeletal_mesh_actor)

    if not binding:
        unreal.log_error(f"❌ Failed to add binding for {actor_name}")
        continue

    # Get or create an animation track
    animation_track = binding.add_track(unreal.MovieSceneSkeletalAnimationTrack)
    animation_section = animation_track.add_section()

    if not animation_section:
        unreal.log_error(f"❌ Failed to create animation section for {actor_name}")
        continue

    # Assign the animation and force 1800 frames duration
    start_frame = 0
    end_frame = 1800

    animation_section.set_range(start_frame, end_frame)
    animation_section.params.animation = anim_sequence
    animation_section.params.start_frame_offset = unreal.FrameNumber(0)

    unreal.log(f"✅ Successfully assigned '{anim_sequence.get_name()}' to {actor_name} with duration 1800 frames.")

# ✅ Set playback range of the whole Level Sequence to 1800 frames
start_frame = 0
end_frame = 1800
unreal.MovieSceneExtensions.set_playback_range(movie_scene, start_frame, end_frame)

# Save the Level Sequence
level_sequence.modify()
unreal.log("✅ Level Sequence updated successfully! Now plays for 1800 frames.")
