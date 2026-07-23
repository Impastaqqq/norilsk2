# Norilsk Scavenging System Design Document

**Document Version:** 1.0.0  
**Source Feature Notes:** `norilsk fight .md`  
**Target Engine:** Ren'Py 8.3+ (Python 3.11+)  
**Related Specs:** `norilsk_fight_design_doc.md`

---

## 1. Executive Summary & Design Philosophy

The **Norilsk Scavenging System** is a timed, point-and-click exploration mini-game where players search environments ("Where's Waldo" style) for survival resources (Food and Water) and weapons. 

Resources gathered during scavenging feed directly into the game's resource management and combat systems (e.g., consuming food in combat to heal player HP).

---

## 2. Exploration Rules & Mechanics

### 2.1 Timed Mini-Game Mechanics
- **Countdown Timer:** Global timer of **15 to 20 seconds** starts as soon as the player enters a scavenging event.
- **HUD Counters:** On-screen counters in the top corner display current quantities of **Food** and **Water**.
- **Multi-Room Navigation:** Players switch between 3 room viewport images using side navigation buttons/arrows.

### 2.2 Interactive Objects
1. **Resource Items (Food & Water Cans):**
   - Clickable cans hidden within the room viewports.
   - **Interaction:** Clicking plays a pickup audio effect and immediately increments the player's resource inventory (e.g., Food +1). No popup window appears, keeping the action fast.
2. **Weapons:**
   - Clickable weapon icons hidden within the room.
   - **Interaction:** Clicking opens an item preview modal showing weapon image, typing (Slashing/Blunt/Regular), and damage stats.
   - **Player Choices:**
     - **[ Equip ]**: Equips the weapon as the player's active weapon.
     - **[ Leave ]**: Leaves the weapon in the room. The weapon remains interactable if the player returns to that room later before time expires.
   - *Design Note:* Opening the weapon modal can either pause or continue ticking the timer to adjust difficulty.

### 2.3 Scavenge Completion
- When the timer expires, a summary screen pops up: *"Congrats! You gathered: [Food Count], [Water Count], [Equipped Weapon]"*.
- Control returns to the main narrative flow.

---

## 3. Narrative & Scavenging Schedule

| Story Day | Phase | Environment / Activity | Key Loot & Mechanics |
| :--- | :--- | :--- | :--- |
| **Day 1** | Intro | Gas Station interior | Intro scavenge learning mechanics -> Followed by Intro Fight. |
| **Day 2** | Evening | Abandoned shelter | Standard food & water scavenging. |
| **Day 3** | Mid-day | Dockyard / Boat wreckage | **Boat Parts Scavenge:** Must find boat parts + food. *Penalty:* Missing boat parts results in -2 Food & -1 Water penalty. Leads to 1st Boss Fight (Behemoth). |
| **Day 4** | Post-Girl | Girl's outpost & travel | Travel through dialogue to scavenge weapons/food, or receive resources directly from the girl. Leads to Parasitic Tendril fight. |
| **Day 5** | Evening | Cultist Camp | Lake encounter (2nd Boss Fight: Leviathan) -> Steal food, water, and weapons from cultist camp. |
| **Day 6** | Mid-day | Theorist Base | Scavenge & steal supplies from the Theorists' camp before meeting them. |
| **Day 7** | Pre-Boss | Research Science Facility | High-tech facility scavenge for late-game weapons and supplies -> 3rd Boss Fight. |
| **Day 8** | Final | Research Core | Final preparation scavenge prior to Final Boss Fight. |
