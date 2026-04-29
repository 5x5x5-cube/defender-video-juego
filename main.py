#!/usr/bin/python3
"""Función Main"""

import asyncio
import pygame  # noqa: F401
import esper  # noqa: F401

from src.engine.game_engine import GameEngine

engine = GameEngine()

async def main():
    await engine.run()

asyncio.run(main())
