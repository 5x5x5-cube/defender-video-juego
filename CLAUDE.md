# Team Project - ECS Game Engine

## Architecture

This project uses the **Entity-Component-System (ECS)** pattern with **esper** as the ECS library and **pygame-ce** for rendering/input.

### ECS Pattern
- **Entities** are integer IDs managed by `esper.World`
- **Components** are pure data classes (no logic). Stored in `src/ecs/components/`
- **Tag components** (marker components with no data) go in `src/ecs/components/tags/`
- **Systems** are pure functions that query and operate on components. Stored in `src/ecs/systems/`

### Naming Conventions
- Components: `c_<name>.py` → class `C<Name>` (e.g., `c_velocity.py` → `CVelocity`)
- Tag components: `c_tag_<name>.py` → class `CTag<Name>` (e.g., `c_tag_enemy.py` → `CTagEnemy`)
- Systems: `s_<name>.py` → function `system_<name>` (e.g., `s_movement.py` → `system_movement`)

### Service Locator
Access images, sounds, and fonts through `ServiceLocator` (`src/engine/service_locator.py`).
Never instantiate services directly — use `ServiceLocator.images_service`, `.sounds_service`, `.fonts_service`.

### Config Loading
- All game configuration lives in JSON files under `assets/cfg/`
- Load functions go in `src/ecs/load/load_world.py` following the pattern `load_<name>_config()` returning `TypedDict` types
- Use `pygame.Vector2` for positions/sizes, `pygame.Color` for colors when parsing JSON

### Prefab Creator
- Entity factory functions go in `src/create/prefab_creator.py`
- Each function takes `world: esper.World` as first argument, creates an entity with components, and returns the entity ID

### Game Engine
- `GameEngine` (`src/engine/game_engine.py`) owns the main game loop
- `_create()`: initial entity creation
- `_process_events()`: input handling
- `_update()`: call systems each frame
- `_draw()`: rendering systems + `pygame.display.flip()`
- `_clean()`: cleanup on exit

## Dependencies
- **pygame-ce** (not pygame) — rendering, input, audio
- **esper** — ECS framework
- Managed with **Poetry**
