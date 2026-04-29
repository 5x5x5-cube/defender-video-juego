# Arquitectura del Proyecto

## Visión General

Motor de videojuegos 2D basado en el patrón **Entity-Component-System (ECS)** con soporte de **escenas**. Utiliza **pygame-ce** para renderizado, entrada y audio, y **esper** como framework ECS.

## Estructura de Carpetas

```
team_project/
├── main.py                          # Punto de entrada
├── assets/cfg/                      # Configuración del juego en JSON
├── src/
│   ├── create/                      # Funciones fábrica de entidades (prefabs)
│   │   └── prefab_creator.py
│   ├── ecs/
│   │   ├── components/              # Componentes (datos puros, sin lógica)
│   │   │   └── tags/                # Componentes marcadores (sin datos)
│   │   ├── systems/                 # Sistemas (funciones puras que operan sobre componentes)
│   │   └── load/
│   │       └── load_world.py        # Carga de configuración desde JSON
│   ├── engine/
│   │   ├── game_engine.py           # Motor principal y ciclo de juego
│   │   ├── service_locator.py       # Localizador de servicios (imágenes, sonidos, fuentes)
│   │   ├── services/                # Servicios con caché (imágenes, sonidos, fuentes)
│   │   └── scenes/
│   │       └── scene.py             # Clase base de escenas
│   └── game/                        # Escenas concretas del juego
```

## Patrón ECS

El patrón Entity-Component-System separa los datos del comportamiento:

- **Entidades**: Identificadores enteros gestionados por `esper.World`. No contienen datos ni lógica.
- **Componentes**: Clases de datos puros (sin métodos de lógica). Representan propiedades como posición, velocidad, superficie, etc.
- **Sistemas**: Funciones puras que consultan componentes y ejecutan la lógica del juego (movimiento, colisiones, renderizado, etc.).

### Convenciones de Nombres

| Tipo | Archivo | Clase/Función |
|------|---------|---------------|
| Componente | `c_<nombre>.py` | `C<Nombre>` |
| Tag (marcador) | `c_tag_<nombre>.py` | `CTag<Nombre>` |
| Sistema | `s_<nombre>.py` | `system_<nombre>` |

## Ciclo de Juego y Escenas

El `GameEngine` ejecuta el ciclo principal y delega en la escena activa:

```
GameEngine.run(start_scene)
│
├── _create()              → scene.do_create()
│
└── while is_running:
    ├── _calculate_time()  → delta_time
    ├── _process_events()  → scene.do_process_events(event)
    ├── _update()          → scene.simulate(delta_time)
    │                         └── scene.do_update(delta_time)
    ├── _draw()            → screen.fill() + scene.do_draw(screen) + flip()
    └── _handle_switch_scene()
```

### Clase Scene

Cada escena posee su propio `esper.World` y gestiona sus propias entidades. Para crear una escena nueva, se hereda de `Scene` y se sobreescriben los métodos necesarios:

| Método | Propósito |
|--------|-----------|
| `do_create()` | Crear entidades iniciales de la escena |
| `do_process_events(event)` | Manejar eventos de entrada |
| `do_update(delta_time)` | Ejecutar sistemas cada frame |
| `do_draw(screen)` | Renderizar la escena |
| `do_action(action)` | Manejar acciones de juego |
| `do_clean()` | Limpieza al salir de la escena |

Para cambiar de escena: `self.switch_scene("NOMBRE_ESCENA")`

## Service Locator

Patrón de localización de servicios para acceder a recursos con caché:

- `ServiceLocator.images_service` — carga y cachea imágenes
- `ServiceLocator.sounds_service` — carga y cachea sonidos
- `ServiceLocator.fonts_service` — carga y cachea fuentes

Nunca instanciar servicios directamente. Siempre acceder a través de `ServiceLocator`.

## Carga de Configuración

Toda la configuración del juego se almacena en archivos JSON bajo `assets/cfg/`. Las funciones de carga en `load_world.py` siguen el patrón `load_<nombre>_config()` y retornan tipos `TypedDict`. Se usa `pygame.Vector2` para posiciones/tamaños y `pygame.Color` para colores.

## Prefab Creator

Las funciones fábrica en `prefab_creator.py` crean entidades completas (con todos sus componentes) y retornan el ID de la entidad. Cada función recibe `world: esper.World` como primer argumento.

## Dependencias

- **pygame-ce** — renderizado, entrada, audio (no confundir con pygame clásico)
- **esper** — framework ECS
- **Poetry** — gestión de dependencias
